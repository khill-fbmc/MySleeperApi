import streamlit as st
import requests
import pandas as pd

@st.cache_data
 def load_rosters(league_id: str) -> pd.DataFrame:
    """
    Fetch rosters from the Sleeper API and return a flattened DataFrame.
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"
    response = requests.get(url)
    response.raise_for_status()
    rosters = response.json()

    # Normalize JSON into a flat table
    df = pd.json_normalize(rosters)

    # Explode the 'players' list into separate rows, if present
    if 'players' in df.columns:
        df = df.explode('players')
        df.rename(columns={'players': 'player'}, inplace=True)

    # Drop columns that aren't needed
    cols_to_drop = [col for col in ['starters', 'taxi', 'reserve'] if col in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)

    return df

# Streamlit UI
st.title("Sleeper League Rosters Viewer")
st.write("Enter a Sleeper league ID to fetch and display its rosters.")

league_id = st.text_input("League ID", "1182054079525027840")

if st.button("Load Rosters"):
    with st.spinner("Fetching data..."):
        roster_df = load_rosters(league_id)
    if not roster_df.empty:
        st.dataframe(roster_df)
    else:
        st.write("No roster data found for this league ID.")
