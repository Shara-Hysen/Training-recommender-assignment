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

top_match_stats["Etikett"] = (
    top_match_stats["Andel (%)"].round().astype(int).astype(str) + " %"
)

chart = alt.Chart(top_match_stats).mark_arc(
    innerRadius=50
).encode(
    theta=alt.Theta("Andel (%):Q"),
    color=alt.Color(
        "Träningsform:N",
        title="Träningsform",
        scale=alt.Scale(
            range=["#16B8C4", "#B39DDB", "#4F6FAE", "#81C784"]
        )
    ),

    tooltip=[
        "Träningsform:N",
        "Antal:Q",
        "Andel (%):Q"
    ]
)

st.altair_chart(chart, width="stretch")