"""Funktioner för att sammanställa statistik från användardata."""

import pandas as pd

def get_top_match_counts(users: pd.DataFrame) -> pd.DataFrame:
    """Räknar hur många användare som fått varje träningsform som bästa matchning."""
    counts = (
        users["top_match"]
        .value_counts()
        .reset_index()
    )

    counts["percent"] = counts["count"] / counts["count"].sum() * 100

    counts = counts.rename(
    columns={
        "top_match": "Träningsform",
        "count": "Antal",
        "percent": "Andel (%)"
    }
)

    return counts