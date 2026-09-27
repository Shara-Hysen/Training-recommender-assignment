
# Training Recommender – Streamlit

## Beskrivning

Detta projekt är en interaktiv träningsapp som jag har utvecklat i Python med hjälp av Streamlit.

Användaren svarar på frågor om sina träningsmål och preferenser. Appen jämför svaren med information om olika träningsformer och presenterar träningsförslag som kan passa användaren.

Målet med uppgiften är att fördjupa mig i Streamlit och undersöka hur Pythonkod och data kan presenteras i ett interaktivt gränssnitt som även personer utan programmeringskunskaper kan använda.

`workouts.csv` innehåller ett mindre dataset med tio träningsformer som jag själv har sammanställt för projektet. `users.csv` innehåller demodata som används för att demonstrera appens statistikfunktion.

## Funktionalitet

Appen:

- läser in information om träningsformer från en CSV-fil
- samlar in användarens träningsmål och preferenser genom ett formulär
- beräknar en matchningspoäng för varje träningsform
- visar de tre bästa matchningarna och ett diagram över de fem högsta matchningspoängen
- låter användaren spara sina svar och sin bästa matchning
- sammanställer sparade svar och visar statistik på en separat sida

## Filstruktur

```text
.streamlit/
    config.toml

data/
    workouts.csv
    users.csv

pages/
    1_Statistik.py

app.py
data_handler.py
recommender.py
user_statistics.py
README.md
requirements.txt
```

Koden är uppdelad efter ansvar:

- `app.py` – appens startsida, formulär och presentation av träningsförslag
- `data_handler.py` – inläsning och sparande av CSV-filer
- `recommender.py` – beräkning av matchningspoäng och träningsrekommendationer
- `user_statistics.py` – sammanställning av statistik från sparad användardata
- `pages/1_Statistik.py` – appens statistiksida
- `.streamlit/config.toml` – inställningar för appens färgtema

## Miljö

Python 3.13

Projektet använder Streamlit, Pandas och Altair. Samtliga beroenden finns i `requirements.txt`.

## Installation och körning

**1. Klona repositoryt:**

```bash
git clone https://github.com/Shara-Hysen/Training-recommender-assignment.git
cd Training-recommender-assignment
```

**2. Skapa en virtuell miljö:**

```bash
python -m venv .venv
```

Aktivera miljön i Git Bash på Windows:

```bash
source .venv/Scripts/activate
```

**3. Installera beroenden:**

```bash
python -m pip install -r requirements.txt
```

**4. Starta appen:**

```bash
streamlit run app.py
```

Appen öppnas i webbläsaren. Där kan användaren få träningsförslag, spara sina inställningar och se sammanställd statistik.

## Testa appen online

Appen finns publicerad på Streamlit Community Cloud:

https://training-match.streamlit.app/

## Källor

Projektet är utvecklat som en individuell examinationsuppgift med utgångspunkt i Streamlits officiella dokumentation och Altairs dokumentation, med stöd av AI-verktyg för kodgranskning, felsökning och utveckling av appen.

- [Streamlit – officiell dokumentation](https://docs.streamlit.io/)
- [Altair – officiell dokumentation](https://altair-viz.github.io/)