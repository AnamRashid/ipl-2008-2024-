import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
import seaborn as sns 
import base64
import openpyxl
# from PIL import Image as PILImage
from io import BytesIO
import os


st.set_page_config(
    page_icon='🏏',
    page_title='IPL Information'
)
st.title('IPL Information')

st.markdown("""
            This application uses simple web scraping of IPL stats data.
            * **Data Source:** [kaggle.com](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020?select=matches.csv).
            """)

st.sidebar.header('User Input Features')

@st.cache_data
def load_data():
    df = pd.read_csv('matches.csv')
    return df

df = load_data()

st.write(f"Full Data Shape: {df.shape}")

# Sidebar - Year selection
sorted_year = sorted(df['season'].unique())
selec_year = st.sidebar.selectbox('Year', list(reversed(sorted_year)))

# Sidebar - Team selection
sorted_uni_team1 = sorted(df['team1'].unique())
selec_team1 = st.sidebar.multiselect('Team 1', sorted_uni_team1, default=sorted_uni_team1)

sorted_uni_team2 = sorted(df['team2'].unique())
selec_team2 = st.sidebar.multiselect('Team 2', sorted_uni_team2, default=sorted_uni_team2)

# Sidebar - Venue selection
uni_venue = sorted(df['venue'].unique())
selec_ven = st.sidebar.multiselect('Venue', uni_venue, default=uni_venue)

# Apply filters to IPL matches data
df_filtered = df[
    (df['season'] == selec_year) &
    (df['team1'].isin(selec_team1)) & 
    (df['team2'].isin(selec_team2)) & 
    (df['venue'].isin(selec_ven))
]

st.header('Winner of the Season')
final_matches = df[df['season'] == selec_year][df['match_type'] == 'Final']
if not final_matches.empty:
    final_winner = final_matches.iloc[0]['winner']
    st.write(f"The winner of the final match for the season {selec_year} is **{final_winner}.**")
else:
    st.write(f"No final match data available for the season {selec_year}.")
    
st.write(f"Filtered Data Shape: {df_filtered.shape}")

# Display the filtered data or a message if empty
if df_filtered.empty:
    st.write("No data available for the selected filters.")
else:
    st.header('Display match stats of selected teams and venue')
    st.write(f'Data Dimension: {df_filtered.shape[0]} rows and {df_filtered.shape[1]} columns')
    st.dataframe(df_filtered)

def file_ud(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="filtered_data.csv">Download it </a>'
    return href

st.markdown(file_ud(df_filtered), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorelation Heatmap'):
    st.header('Intercorelation Matrix Heatmap')
    
    # Filter out non-numeric columns
    df_filtered_numeric = df_filtered.select_dtypes(include=[np.number])

    corr = df_filtered_numeric.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
        st.pyplot(f)

# Score Distribution
if st.button('Score Distribution'):
    st.header('Score Distribution')
    
    fig, ax = plt.subplots()
    sns.histplot(df_filtered['target_runs'], kde=True, ax=ax)
    st.pyplot(fig)

if st.button('Winning Teams Across Seasons'):
    st.header('Winning Teams Across Seasons')
    team_wins = df_filtered['winner'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(y=team_wins.index, x=team_wins.values, ax=ax)
    ax.set_xlabel('Number of Wins')
    ax.set_ylabel('Team')
    st.pyplot(fig)

if st.button('Top Players of the Match'):
    st.header('Top Players of the Match')
    player_of_match_counts = df_filtered['player_of_match'].value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(y=player_of_match_counts.index, x=player_of_match_counts.values, ax=ax)
    ax.set_xlabel('Number of Awards')
    ax.set_ylabel('Player')
    st.pyplot(fig)


if st.button('Venue Analysis'):
    st.header('Venue Analysis')
    venue_counts = df_filtered['venue'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(y=venue_counts.index, x=venue_counts.values, ax=ax)
    ax.set_xlabel('Number of Matches')
    ax.set_ylabel('Venue')
    st.pyplot(fig)


if st.button('City-Wise Match Distribution'):
    st.header('City-Wise Match Distribution')
    city_counts = df_filtered['city'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(y=city_counts.index, x=city_counts.values, ax=ax)
    ax.set_xlabel('Number of Matches')
    ax.set_ylabel('City')
    st.pyplot(fig)


