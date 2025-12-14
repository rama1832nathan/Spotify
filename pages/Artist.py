import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
@st.cache_data
def load_data():
    df = pd.read_csv("data/spotify_data.csv")
    df["album_release_date"] = pd.to_datetime(df["album_release_date"], errors="coerce")
    df["year"] = df["album_release_date"].dt.year
    return df

def main():
    st.title(":green[Artist]")
    df = load_data()

    mask = df['artist_name'].str.match(r'^[A-Za-z ]+$', na=False)
    st.caption(
        "**Data Filter Applied** - Regex `^[A-Za-z ]+$` keeps only artist names with letters/spaces. Removes names with numbers/special chars like 'J 2', '7Kk581xmaj...'")

    col1, col2 = st.columns(2)
    col1.metric(":green[Total No. Unique Artist]",f"{len(df[mask]['artist_name'].drop_duplicates())}")
    st.caption("**Clean Artist Count** - Number of artists with valid names (alphabets + spaces only) after filtering.")
    col2.metric(":orange[Unique albums]", f"{df['album_id'].nunique():,}")
    st.caption("**Dataset Context** - Total unique albums across entire dataset (unfiltered).")


    with st.expander("Expand to view the unique artist name"):
        st.caption(
            "**Complete Clean Artist Roster** - Alphabetical list of all filtered artists. Verify data quality here.")
        st.dataframe(df[mask]['artist_name'].drop_duplicates().sort_values(),hide_index=True)
################################################################################################################\

    artist_df = (
        df[mask]
        .groupby("artist_name", as_index=False)["artist_popularity"]
        .max()
        .sort_values("artist_popularity", ascending=False)
    )
    st.caption(
        "**Artist Popularity Table** - Max artist_popularity score per artist. Higher = more popular on Spotify.")
    st.subheader("Top 20 Artists by Popularity")
    st.caption(
        "**Popularity Leaders** - Bar chart shows top 20 clean-named artists ranked by Spotify artist_popularity score. Expect Sabrina Carpenter (~91), Arcane (~76).")
    st.bar_chart(artist_df.head(20).set_index("artist_name"))
################################################################################################################

    track_counts = (
        df[mask]['artist_name']
        .value_counts()
        .head(10)
        .reset_index()
        .rename(columns={'count': 'track_count'})
    )
    st.caption(
        "**Artist Activity Table** - Top 10 artists by number of tracks in dataset. Shows most active/prolific artists.")
    st.dataframe(track_counts)

    st.subheader("📊 Artists with Most Tracks")
    st.caption(
        "**Artist Productivity** - Bar chart shows top 10 artists by track count. Reveals high-output artists vs. popularity leaders.")
    st.bar_chart(track_counts.set_index('artist_name')['track_count'])

################################################################################################################


if __name__ == "__main__":
    main()