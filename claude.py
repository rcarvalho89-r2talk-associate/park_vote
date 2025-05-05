import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime
import time

# Set page configuration
st.set_page_config(
    page_title="National Parks Ranking",
    page_icon="🏞️",
    layout="wide"
)

# Constants
DATA_FILE = "national_parks_data.json"
DEFAULT_ELO = 1200
K_FACTOR = 32  # ELO K-factor (determines how much ratings change after each match)

# List of National Parks with their states
NATIONAL_PARKS = [
    {"name": "Lençóis Maranhenses", "state": "Maranhão"},
    {"name": "Chapada dos Veadeiros", "state": "Goiás"},
    {"name": "Iguaçu", "state": "Paraná"},
    {"name": "Fernando de Noronha", "state": "Pernambuco"},
    {"name": "Chapada Diamantina", "state": "Bahia"},
    {"name": "Pantanal Matogrossense", "state": "Mato Grosso/Mato Grosso do Sul"},
    {"name": "Amazônia", "state": "Vários"},
    {"name": "Serra dos Órgãos", "state": "Rio de Janeiro"},
    {"name": "Aparados da Serra", "state": "Rio Grande do Sul/Santa Catarina"},
    {"name": "Jericoacoara", "state": "Ceará"},
    {"name": "Abrolhos", "state": "Bahia"},
    {"name": "Serra da Capivara", "state": "Piauí"},
    {"name": "Cavernas do Peruaçu", "state": "Minas Gerais"},
    {"name": "Cristalino", "state": "Mato Grosso"},
    {"name": "Jaú", "state": "Amazonas"},
    {"name": "Anavilhanas", "state": "Amazonas"},
    {"name": "Pico da Neblina", "state": "Amazonas"},
    {"name": "Roraima", "state": "Roraima"},
    {"name": "Catimbau", "state": "Pernambuco/Piauí"},
    {"name": "Emas", "state": "Goiás/Mato Grosso do Sul"},
    {"name": "Grande Sertão Veredas", "state": "Minas Gerais/Bahia"},
    {"name": "São Joaquim", "state": "Santa Catarina"},
    {"name": "Ubajara", "state": "Ceará"},
    {"name": "Sete Cidades", "state": "Piauí"},
    {"name": "Tijuca", "state": "Rio de Janeiro"},
    {"name": "Brasília", "state": "Distrito Federal"},
    {"name": "Chapada dos Guimarães", "state": "Mato Grosso"},
    {"name": "Araguaia", "state": "Tocantins"},
    {"name": "Nascentes do Rio Parnaíba", "state": "Maranhão/Piauí/Bahia/Tocantins"},
    {"name": "Campos Gerais", "state": "Paraná"},
    {"name": "Ilha Grande", "state": "Rio de Janeiro"},
    {"name": "Restinga de Jurubatiba", "state": "Rio de Janeiro"},
    {"name": "Superagui", "state": "Paraná"},
    {"name": "Viruá", "state": "Roraima"},
    {"name": "Cabo Orange", "state": "Amapá"},
    {"name": "Montanhas do Tumucumaque", "state": "Pará/Amapá"},
    {"name": "Mapinguari", "state": "Amazonas/Rondônia"},
    {"name": "Juruena", "state": "Amazonas/Mato Grosso"},
    {"name": "Rio Novo", "state": "Mato Grosso"},
    {"name": "Xingu", "state": "Mato Grosso/Pará"}
]

# Function to initialize or load data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # Make sure all parks are in the data
            park_names = [park["name"] for park in data["parks"]]
            for park in NATIONAL_PARKS:
                if park["name"] not in park_names:
                    data["parks"].append({
                        "name": park["name"],
                        "state": park["state"],
                        "elo": DEFAULT_ELO,
                        "wins": 0,
                        "losses": 0,
                        "matches": 0
                    })
            return data
    else:
        # Initialize with default data
        parks_data = [{"name": park["name"], "state": park["state"], "elo": DEFAULT_ELO, "wins": 0, "losses": 0, "matches": 0} for park in NATIONAL_PARKS]
        data = {
            "parks": parks_data,
            "matches": [],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_data(data)
        return data

# Function to save data
def save_data(data):
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Function to calculate new ELO ratings
def calculate_elo(rating_a, rating_b, result_a):
    # Expected score for player A
    expected_a = 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / 400))
    
    # Update ratings
    new_rating_a = rating_a + K_FACTOR * (result_a - expected_a)
    new_rating_b = rating_b + K_FACTOR * ((1 - result_a) - (1 - expected_a))
    
    return new_rating_a, new_rating_b

# Function to select two parks for voting
def select_matchup(parks_data):
    # Select two different parks weighted by how few matches they've had
    weights = [1.0 / (park["matches"] + 1) for park in parks_data]
    total_weight = sum(weights)
    probabilities = [w / total_weight for w in weights]
    
    indices = list(range(len(parks_data)))
    park1_idx = random.choices(indices, weights=probabilities, k=1)[0]
    
    # Remove park1 from choices for park2
    indices.remove(park1_idx)
    weights.pop(park1_idx)
    total_weight = sum(weights)
    probabilities = [w / total_weight for w in weights]
    
    park2_idx = random.choices(indices, weights=probabilities, k=1)[0]
    
    if park2_idx >= park1_idx:
        park2_idx += 1  # Adjust index since we removed park1
    
    return parks_data[park1_idx], parks_data[park2_idx]

# Main app
def main():
    st.title("🏞️ National Parks ELO Ranking System")
    st.write("Vote for your favorite National Parks and see how they rank!")
    
    # Load data
    data = load_data()
    parks_data = data["parks"]
    matches_history = data["matches"]
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Vote", "Rankings", "Match History"])
    
    with tab1:
        st.header("Vote on National Parks")
        st.write("Which National Park do you prefer? Click on your favorite!")
        
        # Check if we have parks in session state
        if 'park1' not in st.session_state or 'park2' not in st.session_state:
            park1, park2 = select_matchup(parks_data)
            st.session_state.park1 = park1
            st.session_state.park2 = park2
        
        col1, col2 = st.columns(2)
        
        # Display park 1
        with col1:
            st.subheader(f"{st.session_state.park1['name']} National Park")
            st.caption(f"Located in {st.session_state.park1['state']}")
            default_image_path = os.path.join("images", "default_park1.png")
           
            
            if st.button(f"Vote for {st.session_state.park1['name']}", key="vote_park1", use_container_width=True):
                # Update ELO ratings
                park1_rating = st.session_state.park1['elo']
                park2_rating = st.session_state.park2['elo']
                new_park1_rating, new_park2_rating = calculate_elo(park1_rating, park2_rating, 1.0)
                
                # Find parks in the data and update
                for park in parks_data:
                    if park['name'] == st.session_state.park1['name']:
                        park['elo'] = new_park1_rating
                        park['wins'] += 1
                        park['matches'] += 1
                    elif park['name'] == st.session_state.park2['name']:
                        park['elo'] = new_park2_rating
                        park['losses'] += 1
                        park['matches'] += 1
                
                # Record the match
                matches_history.append({
                    "winner": st.session_state.park1['name'],
                    "loser": st.session_state.park2['name'],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                # Save data
                save_data(data)
                
                # Select new parks
                park1, park2 = select_matchup(parks_data)
                st.session_state.park1 = park1
                st.session_state.park2 = park2
                
                st.rerun()
                
        # Display park 2
        with col2:
            st.subheader(f"{st.session_state.park2['name']} National Park")
            st.caption(f"Located in {st.session_state.park2['state']}")
           
            
            if st.button(f"Vote for {st.session_state.park2['name']}", key="vote_park2", use_container_width=True):
                # Update ELO ratings
                park1_rating = st.session_state.park1['elo']
                park2_rating = st.session_state.park2['elo']
                new_park1_rating, new_park2_rating = calculate_elo(park1_rating, park2_rating, 0.0)
                
                # Find parks in the data and update
                for park in parks_data:
                    if park['name'] == st.session_state.park1['name']:
                        park['elo'] = new_park1_rating
                        park['losses'] += 1
                        park['matches'] += 1
                    elif park['name'] == st.session_state.park2['name']:
                        park['elo'] = new_park2_rating
                        park['wins'] += 1
                        park['matches'] += 1
                
                # Record the match
                matches_history.append({
                    "winner": st.session_state.park2['name'],
                    "loser": st.session_state.park1['name'],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                # Save data
                save_data(data)
                
                # Select new parks
                park1, park2 = select_matchup(parks_data)
                st.session_state.park1 = park1
                st.session_state.park2 = park2
                
                st.rerun()
                
        # Skip button
        if st.button("Skip this matchup", key="skip"):
            park1, park2 = select_matchup(parks_data)
            st.session_state.park1 = park1
            st.session_state.park2 = park2
            st.rerun()
    
    with tab2:
        st.header("National Parks Rankings")
        
        # Create DataFrame for display
        parks_df = pd.DataFrame(parks_data)
        parks_df = parks_df.sort_values(by="elo", ascending=False).reset_index(drop=True)
        parks_df.index = parks_df.index + 1  # Start index at 1
        
        # Format the DataFrame
        formatted_df = parks_df[["name", "state", "elo", "wins", "losses", "matches"]].copy()
        formatted_df.columns = ["Park Name", "State", "ELO Rating", "Wins", "Losses", "Total Matches"]
        formatted_df["ELO Rating"] = formatted_df["ELO Rating"].apply(lambda x: int(x))
        
        # Display rankings
        st.dataframe(formatted_df, use_container_width=True, height=400)
        
        # Top parks visualization
        st.subheader("Top 10 National Parks")
        top_10 = parks_df.head(10).copy()
        
        # Create horizontal bar chart
        chart_data = pd.DataFrame({
            "Park": top_10["name"],
            "ELO": top_10["elo"].apply(lambda x: int(x))
        })
        
        st.bar_chart(chart_data.set_index("Park"), use_container_width=True)
    
    with tab3:
        st.header("Recent Match History")
        
        # Show recent matches
        if matches_history:
            recent_matches = matches_history[-20:]  # Get last 20 matches
            recent_matches.reverse()  # Show newest first
            
            for i, match in enumerate(recent_matches):
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 2])
                    with col1:
                        st.write(f"**Winner: {match['winner']}**")
                    with col2:
                        st.write("vs")
                    with col3:
                        st.write(f"Loser: {match['loser']}")
                    st.caption(f"Voted on {match['timestamp']}")
                    if i < len(recent_matches) - 1:
                        st.divider()
        else:
            st.write("No matches have been recorded yet. Start voting!")

# Run the app
if __name__ == "__main__":
    main()