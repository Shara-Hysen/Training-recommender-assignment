"""Streamlit-app som matchar användarens träningspreferenser med träningsformer."""

import altair as alt
import pandas as pd
import streamlit as st

from recommender import get_recommendations
from data_handler import load_users, load_workouts, save_user
from user_statistics import get_top_match_counts

# Konfigurerar Streamlit-sidans titel, ikon och layout.
st.set_page_config(
    page_title="Hitta din träningsform",
    page_icon="🏃",
    layout="centered"
)

# Läser in träningsdatan och cachelagrar den för att undvika onödig omläsning.
@st.cache_data
def get_workouts() -> pd.DataFrame:
    """Hämtar träningsdata och cachelagrar resultatet."""
    return load_workouts()


workouts = get_workouts()

users = load_users()

# Visar appens titel, introduktion och information om matchningsmodellen.
st.title("✨ Hitta din träningsform")

st.write(
    "Få personliga träningsförslag utifrån dina mål och preferenser. "
    "Svara på några korta frågor så matchar appen dig med träningsformer som kan passa dig."
)

st.info(
    "Appen använder en förenklad matchningsmodell baserad på bland annat "
    "träningsmål, tid, intensitet, socialt upplägg och miljö."
)


# Skapar formuläret där användaren anger sina träningsmål och preferenser.
st.subheader("Berätta lite om hur du vill träna")

if "name" not in st.session_state:
    with st.form("name_form"):
        name = st.text_input(
            "Vad heter du?",
            placeholder="Skriv ditt namn"
        )

        name_submitted = st.form_submit_button("Fortsätt")

    if name_submitted and name:
        st.session_state["name"] = name
        st.rerun()

if "name" in st.session_state:
    st.write(f"👋 Hej {st.session_state['name']}!")   

    with st.form("workout_form"):

        goal = st.selectbox(
            "Vad är ditt främsta mål med träningen?",
            [
                "Bli starkare",
                "Förbättra konditionen",
                "Öka rörligheten",
                "Må bättre"
            ]
        )

        time = st.select_slider(
            "Hur mycket tid vill du lägga på ett träningspass?",
            options=[
                "30 minuter eller mindre",
                "30–60 minuter",
                "Mer än 60 minuter"
            ]
        )

        intensity = st.select_slider(
            "Vilken intensitet föredrar du?",
            options=["Låg", "Medel", "Hög"]
        )

        col1, col2 = st.columns(2)

        with col1:
            social = st.radio(
                "Hur vill du helst träna?",
                [
                    "Själv",
                    "Spelar ingen roll",
                    "Tillsammans med andra"
                ]
            )

        with col2:
            environment = st.radio(
                "Var tränar du helst?",
                [
                    "Inomhus",
                    "Spelar ingen roll",
                    "Utomhus"
                ]
            )

        
        # Formuläret skickas först när användaren klickar på knappen.
        submitted = st.form_submit_button("Hitta min träningsform")

    # Omvandlar användarens val till de värden som används i matchningsmodellen.
    time_map = {
        "30 minuter eller mindre": 1,
        "30–60 minuter": 2,
        "Mer än 60 minuter": 3
    }

    intensity_map = {
        "Låg": 1,
        "Medel": 2,
        "Hög": 3
    }

    social_map = {
        "Själv": 1,
        "Tillsammans med andra": 3
    }

    goal_map = {
        "Bli starkare": "strength",
        "Förbättra konditionen": "cardio",
        "Öka rörligheten": "mobility",
        "Må bättre": "wellbeing"
    }

    if submitted:

        # Samlar användarens val i det format som matchningsmodellen använder.
        user_preferences = {
            "goal": goal_map[goal],
            "time": time_map[time],
            "intensity": intensity_map[intensity],
            "social": None if social == "Spelar ingen roll" else social_map[social],
            "environment": None if environment == "Spelar ingen roll" else (
                1 if environment == "Inomhus" else 2
            )
        }

        # Hämtar de fem träningsformer som har högst matchningspoäng.
        recommendations = get_recommendations(
            workouts,
            user_preferences,
            top_n=5
            )   

        st.session_state["recommendations"] = recommendations
        st.session_state["user_preferences"] = user_preferences

    if "recommendations" in st.session_state:
        recommendations = st.session_state["recommendations"]
        user_preferences = st.session_state["user_preferences"]

        # Visar användarens bästa matchning och omvandlar poängen till procent.
        st.subheader("💗 Dina bästa matchningar")

        best_match = recommendations.iloc[0]
        best_percent = round(best_match["match_score"] * 100)

        user_data = {
            "name": st.session_state["name"],
            "goal": user_preferences["goal"],
            "time": user_preferences["time"],
            "intensity": user_preferences["intensity"],
            "social": user_preferences["social"],
            "environment": user_preferences["environment"],
            "top_match": best_match["name"]
        }

        st.session_state["user_data"] = user_data

        # Visar den bästa matchningen i ett eget resultatkort.
        with st.container(border=True):
            st.markdown("#### 🏆 BÄSTA MATCHNING")
            st.markdown(f"## {best_match['name']}")

            st.metric(
                label="Matchningspoäng",
                value=f"{best_percent} %"
                )

            st.write(best_match["description"])
            st.progress(best_percent / 100)

        # Visar den näst bästa och tredje bästa matchningen sida vid sida.
        col1, col2 = st.columns(2)

        for column, position in zip([col1, col2], [1, 2]):
            workout = recommendations.iloc[position]
            match_percent = round(workout["match_score"] * 100)

            with column:
                with st.container(border=True):
                    st.markdown(f"### {position + 1}. {workout['name']}")

                    st.metric(
                        label="Matchningspoäng",
                        value=f"{match_percent} %"
                    )

                    st.write(workout["description"])
                    st.progress(match_percent / 100)


        # Förbereder de fem bästa matchningarna för visualisering i diagrammet.
        st.subheader("Jämför dina bästa matchningar")

        chart_data = recommendations[["name", "match_score"]].copy()
        chart_data["match_percent"] = chart_data["match_score"] * 100

        # Skapar ett horisontellt stapeldiagram med matchningspoängen i procent.
        bars = alt.Chart(chart_data).mark_bar(
            color="#16B8C4",
            cornerRadiusEnd=4
        ).encode(
            x=alt.X(
                "match_percent:Q",
                title="Matchningspoäng (%)",
                scale=alt.Scale(domain=[0, 100])
            ),
            y=alt.Y(
                "name:N",
                title=None,
                sort=None
            )
        )

        # Skapar procentetiketter som ska visas i staplarna.
        chart_data["label"] = (
            chart_data["match_percent"].round().astype(int).astype(str) + " %"
    )
        # Placerar de vita procentetiketterna inuti staplarna.
        text = alt.Chart(chart_data).mark_text(
            align="right",
            baseline="middle",
            dx=-6,
            fontSize=13,
            color="white"
        ).encode(
            x=alt.X("match_percent:Q"),
            y=alt.Y("name:N", sort=None),
            text="label:N"
        )

        # Kombinerar staplarna med procentetiketterna och visar diagrammet i appen.
        chart = bars + text

        st.altair_chart(chart, use_container_width=True)
        

        st.caption(
            "Resultatet bygger på en förenklad matchning av dina val mot "
            "träningsformernas egenskaper och ska ses som inspiration."
        )

    if "user_data" in st.session_state:
        if st.button("💾 Spara mina inställningar"):
            save_user(st.session_state["user_data"])
            st.success("Dina inställningar har sparats!")


users = load_users()
top_match_stats = get_top_match_counts(users)

