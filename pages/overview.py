import plotly.express as plt
import pandas as pd
import streamlit as st
import altair as alt

@st.cache_data
def load_data():
    df = pd.read_csv("data/spotify_data.csv")
    df["album_release_date"] = pd.to_datetime(df["album_release_date"], errors="coerce")
    df["year"] = df["album_release_date"].dt.year
    return df

def main():
    st.subheader(":violet[Overview]",divider=True)
    st.markdown("""
    <style>
    .yellow{
        color : #FFE52A;
    }
    h3 {
        font-size:30px !important;
    }
    </style>
    """
    ,unsafe_allow_html=True)

    df = load_data()
    with st.expander("Expand to see the full data"):
        st.caption(
            "**Complete Spotify dataset** - Contains all tracks with columns: track_id, artist_name, track_popularity, album_id, release dates, etc.")
        st.write(df)

    col1,col2,col3 = st.columns(3)

    col1.metric(":green[Total Tracks]   ",f"{len(df)}")
    col2.metric(":red[Unique artists]", f"{df['artist_name'].nunique():,}")
    col3.metric(":orange[Unique albums]", f"{df['album_id'].nunique():,}")



####################################################################################################
    st.subheader("Track Popularity Over Time",divider='red')
    yearly = (
                df.dropna(subset=['year','track_popularity'])
                    .groupby("year",as_index=False)["track_popularity"].mean()
    )
    st.caption("**Yearly Summary Table** - Shows average track popularity for each release year across ALL artists")


    with st.expander("Expand to view the data"):
        st.write(yearly)

    fig = plt.line(
        yearly,
        x="year",
        y="track_popularity",
        title="Average Track Popularity by Year"
    )
    st.caption(
        "**Trend Analysis** - Line chart showing how track popularity evolved year-over-year. Expect higher scores in recent years (2024-2025).")
    st.plotly_chart(fig,use_container_width=True)

#################################################################################################
    st.subheader("Track Popularity by artist name",divider='green')
    artist_year = (df.dropna(subset=["year","track_popularity","artist_name"]).
                   groupby(["year","artist_name"],as_index = False).
                   agg(avg_pop = ("track_popularity","mean"),
                       track_count = ("track_id","count"))
                   )
    st.caption(
        "**Artist Performance Matrix** - Each row = 1 artist in 1 year. Columns: avg_pop (average track popularity), track_count (songs released that year)")
    years = sorted(artist_year['year'].dropna().unique())[::-1]
    year_selected = st.selectbox('Select Year',years,index=0)

    top_artists = (
        artist_year[artist_year["year"] == year_selected]
        .sort_values("avg_pop", ascending=False)
        .head(20)
    )
    st.caption(
        f"**Top 20 Artists in {year_selected}** - Ranked by average track popularity. Higher = more popular tracks that year.")
    st.write(f"Top 20 artists in {year_selected}")
    with st.expander("Expand to see the data"):
        st.dataframe(top_artists)


    st.subheader('Artist popularity over years',divider='orange')

    artists = sorted(artist_year["artist_name"].unique())

    st.subheader('🎨 Individual Artist Trend', divider='orange')
    artist_selected = st.selectbox("Select artist", artists)
    artist_trend = (
        artist_year[artist_year["artist_name"] == artist_selected]
        .sort_values("year")
    )
    st.caption(
        f"**{artist_selected}'s Career Data** - Shows their average track popularity and track count for every year they appear in dataset")
    line = (
        alt.Chart(artist_trend)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("avg_pop:Q", title="Average track popularity"),
            tooltip=["year", "avg_pop", "track_count"]
        )
    )
    st.caption(
        "**Career Trajectory Chart** - Line shows how this artist's track popularity changed over time. Hover for year-specific details.")
    st.altair_chart(line, use_container_width=True)


if __name__ == "__main__":
    main()