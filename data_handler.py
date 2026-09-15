"""Funktioner för att läsa och spara appens data."""

import pandas as pd

def load_workouts() -> pd.DataFrame:
    """Läser in träningsdata från CSV-filen."""
    return pd.read_csv("data/workouts.csv")

def load_users() -> pd.DataFrame:
    """Läser in sparad användardata från CSV-filen."""
    return pd.read_csv("data/users.csv")


def save_user(user_data: dict) -> None:
    """Sparar eller uppdaterar användarens träningspreferenser i CSV-filen."""
    users = load_users()

    existing_user = users["name"].str.lower() == user_data["name"].lower()

    if existing_user.any():
        for column, value in user_data.items():
            users.loc[existing_user, column] = value
    else:
        users = pd.concat(
            [users, pd.DataFrame([user_data])],
            ignore_index=True
        )

    users.to_csv("data/users.csv", index=False)


def get_top_matches() -> pd.DataFrame:
    """Sammanställer hur många användare som fått varje träningsform som bästa matchning."""
    users = load_users()

    top_matches = (
        users["top_match"]
        .value_counts()
        .reset_index()
    )

    return top_matches