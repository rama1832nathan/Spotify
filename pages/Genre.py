import pandas as pd
import streamlit as st
import plotly.express as plt

@st.cache_data
def load_data():
    df = pd.read_csv("data/spotify_data.csv")
    df["album_release_date"] = pd.to_datetime(df["album_release_date"], errors="coerce")
    df["year"] = df["album_release_date"].dt.year
    return df

def main():
    st.title(":orange[Genre : ]")

    df = load_data()


    st.header("Trends in Top 10 Artist Genres Across Years",divider=True)
    st.markdown(
        "_View the most common artist genres for a given year based on track counts in this dataset. Select "
        "the year and go through this page all will be modified_"
    )

    genre = (df.dropna(subset=["artist_genres","year"]).
             groupby(["year","artist_genres"],as_index=False).
             agg(count_genre = ("artist_genres","count")))

    st.caption(
        "**Genre Frequency Matrix** - Counts tracks per genre per year. Higher count = more tracks from that genre in dataset.")

    years = sorted(genre['year'].dropna().unique())[::-1]

    year_selected = st.selectbox('Select the Year',years,index=0)

    genre_selected = (
        genre[genre['year']==year_selected]
        .sort_values("count_genre",ascending=False)
        .head(10)
    )

    st.caption(
        f"**Top 10 Genres in {year_selected}** - Ranked by track count. Shows which genres dominated that year's releases.")
    with st.expander("Expand to see the data"):
        st.dataframe(genre_selected)
    fig1 = plt.bar(
        genre_selected,
        y="artist_genres",
        x="count_genre",
        color="count_genre",
        title=f"Top 10 genres in {year_selected}"
    )
    st.caption(
        f"**Genre Dominance Chart** - Horizontal bar shows top 10 genres by number of tracks released in {year_selected}. Longer bars = more representation.")
    st.plotly_chart(fig1,use_container_width=True)


###########################################################################
    st.header("Most listened duration by genre",divider=True)
    # st.markdown("_Listened over the years_")

    tot_genre_count = (df.dropna(subset=['year','artist_genres','track_duration_min'])
                       .groupby(['year'])
                       .agg(duration = ("track_duration_min","sum"))
                       )
    st.caption("**Yearly Total Duration** - Sum of all track durations (minutes) for selected year across ALL genres.")

    duration = tot_genre_count.loc[year_selected, "duration"]
    st.metric(
        label=f":orange[Total duration in {year_selected}]",
        value=f"{duration:.2f} min"
    )
    st.caption(
        f"**Total Listening Time** - Combined duration of ALL tracks released in {year_selected}. Indicates overall music consumption volume.")
    st.subheader("Month wise Genre",divider=True)
    df["month"] = df["album_release_date"].dt.month
    month_stats = (df.dropna(subset=['year','month','artist_genres','track_duration_min'])
                   .groupby(['year','month','artist_genres'],as_index=False)
                   .agg(month_dur = ("track_duration_min",'sum'))
    )
    month_stats_year = month_stats[month_stats['year'] == year_selected]
    st.caption(
        f"**Monthly Genre Breakdown for {year_selected}** - Shows total duration per genre per month. Reveals seasonal genre trends.")
    st.write(f"**Monthly Genre Duration Table - {year_selected}**")
    st.write(month_stats_year)

    fig2 = plt.bar(
        month_stats_year,
        x = "month",
        y = "month_dur",
        color = "artist_genres",
        pattern_shape="artist_genres",
        title = f"Month-wise genre duration in {year_selected}"
    )
    st.caption(
        f"**Seasonal Genre Trends** - Stacked bar chart shows how different genres contributed to listening time each month in {year_selected}. Patterns/colors reveal peak months for each genre.")
    st.plotly_chart(fig2,use_container_width=True)
if __name__ == "__main__":
    main()