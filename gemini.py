import streamlit as st
import pandas as pd
import random
import math
from datetime import datetime

# --- Data Initialization ---
NATIONAL_PARKS = {
    "Yellowstone": {"elo": 1000, "votes": 0},
    "Yosemite": {"elo": 1000, "votes": 0},
    "Grand Canyon": {"elo": 1000, "votes": 0},
    "Zion": {"elo": 1000, "votes": 0},
    "Rocky Mountain": {"elo": 1000, "votes": 0},
    "Acadia": {"elo": 1000, "votes": 0},
    "Glacier": {"elo": 1000, "votes": 0},
    "Olympic": {"elo": 1000, "votes": 0},
    "Bryce Canyon": {"elo": 1000, "votes": 0},
    "Arches": {"elo": 1000, "votes": 0},
}
K_FACTOR = 32
VOTE_HISTORY = []

def calculate_expected_score(rating_a, rating_b):
    """Calculates the expected score of player A in a match against player B."""
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

def update_elo(rating_a, rating_b, score_a, k=K_FACTOR):
    """Updates the ELO ratings of two players after a match."""
    expected_a = calculate_expected_score(rating_a, rating_b)
    expected_b = 1 - expected_a
    new_rating_a = rating_a + k * (score_a - expected_a)
    new_rating_b = rating_b + k * ((1 - score_a) - expected_b)
    return new_rating_a, new_rating_b

def get_ranked_parks(parks_data):
    """Returns a Pandas DataFrame of parks ranked by their ELO score."""
    ranked_parks = pd.DataFrame.from_dict(parks_data, orient='index')
    ranked_parks = ranked_parks.sort_values(by='elo', ascending=False).reset_index()
    ranked_parks.rename(columns={'index': 'Park', 'elo': 'ELO Rating', 'votes': 'Total Votes'}, inplace=True)
    ranked_parks['Rank'] = ranked_parks.index + 1
    return ranked_parks[['Rank', 'Park', 'ELO Rating', 'Total Votes']]

def display_vote_history(history, num_recent=5):
    """Displays the most recent vote history."""
    st.subheader("Recent Votes")
    if not history:
        st.info("No votes yet!")
        return
    recent_votes = history[-num_recent:]
    for vote in reversed(recent_votes):
        st.markdown(f"{vote['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}: **{vote['winner']}** defeated {vote['loser']}")

# --- Streamlit App ---
st.title("National Parks Voting and Ranking")

if 'park1' not in st.session_state:
    park_names = list(NATIONAL_PARKS.keys())
    st.session_state['park1'], st.session_state['park2'] = random.sample(park_names, 2)

park1_name = st.session_state['park1']
park2_name = st.session_state['park2']

st.subheader("Vote for your favorite!")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {park1_name}")
    # You could add an image here if you have URLs for park images
    if st.button(f"Vote for {park1_name}"):
        NATIONAL_PARKS[park1_name]['votes'] += 1
        NATIONAL_PARKS[park2_name]['votes'] += 1
        new_elo1, new_elo2 = update_elo(NATIONAL_PARKS[park1_name]['elo'], NATIONAL_PARKS[park2_name]['elo'], 1)
        NATIONAL_PARKS[park1_name]['elo'] = new_elo1
        NATIONAL_PARKS[park2_name]['elo'] = new_elo2
        VOTE_HISTORY.append({"timestamp": datetime.now(), "winner": park1_name, "loser": park2_name})
        park_names = list(NATIONAL_PARKS.keys())
        st.session_state['park1'], st.session_state['park2'] = random.sample(park_names, 2)
        st.rerun()

with col2:
    st.markdown(f"### {park2_name}")
    # You could add an image here if you have URLs for park images
    if st.button(f"Vote for {park2_name}"):
        NATIONAL_PARKS[park1_name]['votes'] += 1
        NATIONAL_PARKS[park2_name]['votes'] += 1
        new_elo1, new_elo2 = update_elo(NATIONAL_PARKS[park1_name]['elo'], NATIONAL_PARKS[park2_name]['elo'], 0)
        NATIONAL_PARKS[park1_name]['elo'] = new_elo1
        NATIONAL_PARKS[park2_name]['elo'] = new_elo2
        VOTE_HISTORY.append({"timestamp": datetime.now(), "winner": park2_name, "loser": park1_name})
        park_names = list(NATIONAL_PARKS.keys())
        st.session_state['park1'], st.session_state['park2'] = random.sample(park_names, 2)
        st.rerun()

# --- Sidebar for Rankings ---
with st.sidebar:
    st.header("Overall Ranking")
    ranked_df = get_ranked_parks(NATIONAL_PARKS)
    st.dataframe(ranked_df)

# --- Display Vote History ---
display_vote_history(VOTE_HISTORY)