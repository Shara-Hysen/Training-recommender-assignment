"""Streamlit-sida för statistik över sparade användare."""

import altair as alt
import streamlit as st

from data_handler import load_users
from user_statistics import get_top_match_counts


st.title("📊 Statistik")

users = load_users()
top_match_stats = get_top_match_counts(users)

st.metric(
    label="Antal sparade användare",
    value=len(users)
)   

st.subheader("🏆 Populäraste toppmatchningar")

st.dataframe(
    top_match_stats,
    hide_index=True
)

chart = alt.Chart(top_match_stats).mark_arc(
    innerRadius=50
).encode(
    theta=alt.Theta("Andel (%):Q"),
    color=alt.Color(
        "Träningsform:N",
        title="Träningsform",
        scale=alt.Scale(
            range=[
                "#16B8C4",  # turkos
                "#B39DDB",  # ljus lila
                "#4F6FAE",  # blå
                "#81C784",  # mjuk grön
                "#5BC0EB",  # ljusblå
                "#9575CD",  # lila
                "#4DB6AC",  # blågrön
                "#7986CB",  # lavendelblå
                "#66BB6A",  # grön
                "#80CBC4",  # ljus turkos
            ]
        )
    ),

    tooltip=[
        "Träningsform:N",
        "Antal:Q",
        "Andel (%):Q"
    ]
)

st.altair_chart(chart, width="stretch")