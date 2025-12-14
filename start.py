import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.header(":green[Spotify] Dashboard :headphones:", divider=True)

    st.markdown(
        """
        <style>
        .big-font {
            font-size:20px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="big-font"> This dashboard explores global Spotify music trends using a curated dataset of tracks, artists, and albums. You can analyze how song popularity, genres, and artist reach evolve over time, compare artists and albums, and discover patterns in track length, explicit content, and listener preferences across years.</p>',
        unsafe_allow_html=True
    )

    st.markdown(":blue[Resources from Kaggle Dataset : ]")
    st.link_button(
        "Dataset",
        "https://www.kaggle.com/datasets/wardabilal/spotify-global-music-dataset-20092025"
    )

pg = st.navigation(
    [
        st.Page(main, title="Home", icon="🏠"),
        st.Page("pages/overview.py", title="Overview", icon="📈"),
        st.Page("pages/genre.py", title="Genre", icon="🎵"),
        st.Page("pages/Artist.py",title="Artist",icon='⭐')
    ]
)

pg.run()
