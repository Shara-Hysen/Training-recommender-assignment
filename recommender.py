"""Funktioner för att beräkna och skapa träningsrekommendationer."""

def calculate_similarity(user_value: int, workout_value: int) -> float:
    """Beräknar likhet mellan två värden på skalan 1-3."""
    difference = abs(user_value - workout_value)
    # Ger 1.0 vid exakt matchning, 0.5 vid ett stegs skillnad och 0.0 vid två.
    similarity = 1 - difference / 2

    return similarity


def calculate_match_score(workout, preferences: dict) -> float:
    """Beräknar en viktad matchningspoäng för en träningsform."""

    # Viktningen styr hur mycket varje faktor påverkar den totala poängen.
    weights = {
        "goal": 0.40,
        "time": 0.15,
        "intensity": 0.25,
        "social": 0.10,
        "environment": 0.10
    }

    # Hämtar träningsformens värde för användarens valda mål och skalar det.
    goal_score = workout[preferences["goal"]] / 3

    time_score = calculate_similarity(
        preferences["time"],
        workout["time"]
    )

    intensity_score = calculate_similarity(
        preferences["intensity"],
        workout["intensity"]
    )

    # "Spelar ingen roll" markeras med None och tas inte med i poängen.
    if preferences["social"] is None:
        social_score = None
    else:
        social_score = calculate_similarity(
            preferences["social"],
            workout["social"]
        )

    if preferences["environment"] is None:
        environment_score = None
    else:
        environment_score = (
            1.0 if preferences["environment"] == workout["environment"] else 0.0
        )

    # Räknar ihop de faktorer som alltid ingår i matchningen.
    weighted_score = (
        goal_score * weights["goal"]
        + time_score * weights["time"]
        + intensity_score * weights["intensity"]
    )

    active_weights = (
        weights["goal"]
        + weights["time"]
        + weights["intensity"]
    )

    if social_score is not None:
        weighted_score += social_score * weights["social"]
        active_weights += weights["social"]

    if environment_score is not None:
        weighted_score += environment_score * weights["environment"]
        active_weights += weights["environment"]

    # Normaliserar poängen utifrån de faktorer som faktiskt används.
    score = weighted_score / active_weights

    return score


def get_recommendations(workouts, preferences: dict, top_n: int = 3):
    """Beräknar och returnerar de träningsformer som matchar bäst."""
    results = workouts.copy()

    # Beräknar en matchningspoäng för varje träningsform.
    results["match_score"] = results.apply(
        lambda workout: calculate_match_score(workout, preferences),
        axis=1
    )

    # Sorterar så att den högsta matchningspoängen kommer först.
    results = results.sort_values(
        by="match_score",
        ascending=False
    )

    return results.head(top_n)
    