
# PROMPT USED FOR AI CODE GENERATION:

Você é um assistente prestativo. Sua missão é criar um programa com base na solicitação de um usuário. Pense passo a passo, primeiro criando um plano e só depois criando a estrutura e os arquivos do programa. Ajude-me a criar um aplicativo Streamlit interativo para votar e classificar os melhores Parques Nacionais do Brasil. O aplicativo deve permitir que os usuários votem nos parques frente a frente e, em seguida, calculem uma classificação para os parques com base no sistema ELO de xadrez. O aplicativo deve exibir em destaque o confronto, juntamente com a classificação geral e os votos recentes.

---

# National Parks ELO Ranking System 🏞️

## Overview

This project implements a web application using Streamlit to rank National Parks based on user preferences through pairwise comparisons. It utilizes the ELO rating system, commonly used in chess and other competitive games, to dynamically update the ranking of each park based on head-to-head "matchups".

Users are presented with two National Parks at a time and vote for their preferred one. Each vote updates the ELO ratings of the two parks involved, leading to a continuously refined ranking reflecting collective user preference.

## Features

*   **Pairwise Voting:** Users vote between two randomly selected National Parks.
*   **ELO Rating System:** Implements the ELO algorithm to calculate and update park rankings based on vote outcomes.
*   **Dynamic Rankings:** Displays a ranked list of National Parks based on their current ELO scores.
*   **Match History:** Shows a log of recent votes/matchups.
*   **Data Persistence (in some versions):** Saves park ratings and match history to a JSON file (`national_parks_data.json`) so rankings persist across sessions.
*   **Interactive Web Interface:** Built with Streamlit for an easy-to-use web application.
*   **(Optional) Weighted Matchup Selection:** Prioritizes parks with fewer votes/matches for selection to ensure broader participation.
*   **(Optional) Visualization:** Includes charts to visualize the top-ranked parks.

## ELO Ranking System

The ELO rating system is a method for calculating the relative skill levels of players in zero-sum games. In this application:

1.  Each National Park starts with a default ELO rating (e.g., 1000 or 1200).
2.  When a user votes, it's treated as a match where the chosen park "wins" and the other "loses".
3.  The expected outcome of the match is calculated based on the current ELO ratings of the two parks.
4.  The actual outcome (the user's vote) is compared to the expected outcome.
5.  ELO ratings are adjusted based on whether the outcome was expected or an "upset". The magnitude of the change depends on the K-factor (a constant determining rating sensitivity) and the difference in ratings.

This system allows the rankings to evolve dynamically as more votes are cast.

## Getting Started

### Prerequisites

*   Python 3.7+
*   pip (Python package installer)

### Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```
2.  **Install required Python packages:**
    ```bash
    pip install streamlit pandas
    ```
    *(Ensure you have a `requirements.txt` file for easier installation if needed)*

### Running the App

1.  Navigate to the directory containing the Python script (e.g., `gemini.py` or `claude.py`).
2.  Run the Streamlit application from your terminal:
    ```bash
    streamlit run your_script_name.py
    ```
    (Replace `your_script_name.py` with the actual filename, e.g., `claude.py`)
3.  Streamlit will start the application and open it in your default web browser.

## Usage

1.  **Vote:** On the main page (or "Vote" tab), you will see two National Parks. Click the "Vote" button under the park you prefer.
2.  **New Matchup:** After voting, the ELO ratings will be updated, and a new pair of parks will be presented.
3.  **(Optional) Skip:** If available, you can click "Skip this matchup" to get a different pair without voting.
4.  **View Rankings:** Check the sidebar or the "Rankings" tab to see the current list of parks sorted by their ELO rating, along with other statistics like total votes/matches, wins, and losses.
5.  **View History:** Navigate to the "Match History" tab or section to see a log of the most recent votes cast.

## Data

*   **Park List:** The initial list of National Parks is defined within the Python script(s). Different versions might use different lists (e.g., US National Parks, Brazilian National Parks).
*   **Persistence:**
    *   One version (`claude.py`) saves the current ELO ratings, vote counts, and match history to a `national_parks_data.json` file in the same directory as the script. This allows the rankings to persist even if the application is stopped and restarted.
    *   Another version (`gemini.py`) stores data in memory, meaning rankings and history are reset each time the script is run.

---




