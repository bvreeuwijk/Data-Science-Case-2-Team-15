import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import zipfile
import subprocess

# Download of laad datasets
# Kaggle API - optioneel als de datasets nog niet zijn gedownload
command = "kaggle datasets download -d stefanoleone992/ea-sports-fc-24-complete-player-dataset"
result = subprocess.run(command, shell=True, capture_output=True, text=True)

# Laad FIFA 19 dataset
df_2019 = pd.read_csv('players_19.csv')

# Laad FIFA 24 dataset uit de zip map
zip_path = r'C:\Users\alexd\anaconda3\ea-sports-fc-24-complete-player-dataset.zip'
with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open('male_players.csv') as f:
        df_2024 = pd.read_csv(f, low_memory=False)

df_2024.rename(columns={'club_name': 'club'}, inplace=True)

# Filter de 2024 dataset om alleen de oudste versies van elke speler te behouden
df_2024_cleaned = df_2024.sort_values('age', ascending=False).drop_duplicates(subset=['short_name'], keep='first')

# Dropdown-menu voor datasetselectie
st.title("Kies Dataset")
dataset_keuze = st.selectbox('Kies een dataset om te bekijken', options=['2019', '2024'])

# Gebruik de geselecteerde dataset
if dataset_keuze == '2019':
    df = df_2019  # Gebruik de FIFA 19 dataset
    title = "FIFA 19 Spelerstatistieken"
else:
    df = df_2024_cleaned  # Gebruik de gefilterde FIFA 24 dataset met de hoogste leeftijd per speler
    title = "FIFA 24 Spelerstatistieken"

# Toon de titel van de geselecteerde dataset
st.title(title)

# Slider voor algemene beoordeling
overall = st.slider('Selecteer een minimale algemene beoordeling (Overall)', min_value=50, max_value=99, value=75)

# Filter de dataset op basis van de geselecteerde overall rating
filtered_df = df[df['overall'] >= overall]
# Categorieën voor posities
aanval_posities = ['ST', 'CF', 'LW', 'RW', 'LF', 'RF']
middenveld_posities = ['CAM', 'CM', 'LM', 'RM', 'CDM', 'LAM', 'RAM', 'LCM', 'RCM']
verdediging_posities = ['CB', 'LB', 'RB', 'LWB', 'RWB', 'LCB', 'RCB', 'LDM', 'RDM']
keeper_posities = ['GK']

# Voeg de optie voor alle posities toe
positie_categorieen = ['Alle posities', 'Aanval', 'Middenveld', 'Verdediging', 'Keeper']

# Dropdown-menu voor positie categorie
positie_categorie = st.selectbox('Kies een categorie', options=positie_categorieen)

# Filter de data op basis van de geselecteerde categorie
if positie_categorie == 'Aanval':
    filtered_df = filtered_df[filtered_df['player_positions'].apply(lambda x: any(pos in x for pos in aanval_posities))]
elif positie_categorie == 'Middenveld':
    filtered_df = filtered_df[filtered_df['player_positions'].apply(lambda x: any(pos in x for pos in middenveld_posities))]
elif positie_categorie == 'Verdediging':
    filtered_df = filtered_df[filtered_df['player_positions'].apply(lambda x: any(pos in x for pos in verdediging_posities))]
elif positie_categorie == 'Keeper':
    filtered_df = filtered_df[filtered_df['player_positions'].isin(keeper_posities)]
else:
    filtered_df = filtered_df  # Voor 'Alle posities', gebruik de volledige dataset



# Dropdown-menu voor clubs
club = st.selectbox('Selecteer een club om spelers te zien', options=['Alle clubs'] + list(df['club'].unique()))
if club != 'Alle clubs':
    filtered_df = filtered_df[filtered_df['club'] == club]

# Checkbox voor aanvallende statistieken
if st.checkbox('Toon aanvallende statistieken'):
    st.write(filtered_df[['short_name', 'shooting', 'pace', 'dribbling']])

# Checkbox voor verdedigende statistieken
if st.checkbox('Toon verdedigende statistieken'):
    st.write(filtered_df[['short_name', 'defending', 'physic']])




# Maak een kopie van de gefilterde DataFrame
filtered_df = filtered_df.copy()

# Toevoegen van de kolom voor waarde per leeftijd, afgerond op hele getallen
filtered_df['waarde_per_leeftijd'] = (filtered_df['value_eur'] / filtered_df['age']).round(0)

# Toevoegen van de kolom voor waarde per rating, afgerond op hele getallen
filtered_df['waarde_per_rating'] = (filtered_df['value_eur'] / filtered_df['overall']).round(0)



# Lijst met gefilterde spelers weergeven
st.dataframe(filtered_df[['short_name', 'club', 'overall', 'potential', 'age', 'value_eur','waarde_per_leeftijd','waarde_per_rating']])

# Histogram maken voor de gefilterde ratings
fig = go.Figure()

# Histogram toevoegen aan de figuur
fig.add_trace(go.Histogram(
    x=filtered_df['overall'],
    nbinsx=20,  # Aantal bins voor het histogram
    marker_color='blue',
    opacity=0.75
))

# Update layout voor het histogram
fig.update_layout(
    title=f'Frequentie van Ratings voor {dataset_keuze} (Minimale Rating: {overall})',
    xaxis_title='Overall Rating',
    yaxis_title='Aantal Spelers',
    bargap=0.2,
)

# Plot de figuur in Streamlit
st.plotly_chart(fig)





# Spelers Vergelijker
st.title("Spelers Vergelijker")

# Aanvallers en verdedigers filteren op basis van de gedefinieerde posities
attackers = df[df['player_positions'].apply(lambda x: any(pos in x for pos in aanval_posities))]
defenders = df[df['player_positions'].apply(lambda x: any(pos in x for pos in verdediging_posities))]


# Zoekbalk voor aanvaller
st.subheader("Zoek een aanvaller:")
attacker_search = st.text_input("Voer een naam van een aanvaller in:")
if attacker_search:
    attacker_filtered = attackers[attackers['short_name'].str.contains(attacker_search, case=False)]
    attacker_names = attacker_filtered['short_name'].tolist()
else:
    attacker_names = []

# Dropdown voor aanvaller
attacker_name = st.selectbox("Selecteer een aanvaller:", attacker_names)

# Zoekbalk voor verdediger
st.subheader("Zoek een verdediger:")
defender_search = st.text_input("Voer een naam van een verdediger in:")
if defender_search:
    defender_filtered = defenders[defenders['short_name'].str.contains(defender_search, case=False)]
    defender_names = defender_filtered['short_name'].tolist()
else:
    defender_names = []

# Dropdown voor verdediger
defender_name = st.selectbox("Selecteer een verdediger:", defender_names)

# Controleren of de spelers zijn geselecteerd
if attacker_name and defender_name:
    attacker = attacker_filtered[attacker_filtered['short_name'] == attacker_name].iloc[0]
    defender = defender_filtered[defender_filtered['short_name'] == defender_name].iloc[0]

    # Berekenen van scores
    attacker_final_score = (attacker['shooting'] + attacker['pace'] + attacker['dribbling']) / 3
    defender_final_score = (defender['defending'] + defender['physic']) / 2  # Fysieke waarde van de verdediger

    # Vergelijking tussen uiteindelijke scores
    if attacker_final_score > defender_final_score:
        overall_result = f"{attacker_name} wint met een uiteindelijke score van {attacker_final_score:.2f} tegen {defender_final_score:.2f}."
    else:
        overall_result = f"{defender_name} wint met een uiteindelijke score van {defender_final_score:.2f} tegen {attacker_final_score:.2f}."

    st.markdown(f"*Uiteindelijke Score Vergelijking:* {overall_result}")  

    # Creëren van de gestapelde barplot
    fig = go.Figure()

    # Voeg de aanvaller toe aan de figuur
    fig.add_trace(go.Bar(
        x=['Aanvaller'],
        y=[attacker_final_score],
        name=attacker_name,
        marker_color='blue',
        hovertemplate=(  
            f'Shooting: {attacker["shooting"]}<br>'
            f'Pace: {attacker["pace"]}<br>'
            f'Dribbling: {attacker["dribbling"]}<br>'  
            f'Totaal: {attacker_final_score:.2f}<extra></extra>'
        ),
    ))

    # Voeg de verdediger toe aan de figuur
    fig.add_trace(go.Bar(
        x=['Verdediger'],
        y=[defender_final_score],
        name=defender_name,
        marker_color='orange',
        hovertemplate=(  
            f'Defending: {defender["defending"]}<br>'
            f'Physical: {defender["physic"]}<br>'
            f'Totaal: {defender_final_score:.2f}<extra></extra>'
        ),
    ))

    # Plot de figuur in Streamlit
    st.plotly_chart(fig)
else:
    st.warning("Selecteer een aanvaller en verdediger om te vergelijken.")

# Filter de FIFA 19 dataset voor spelers onder de 21 jaar
df_19_under_21 = df_2019[df_2019['age'] < 21]

# Selecteer relevante kolommen uit beide datasets
df_19_filtered = df_19_under_21[['short_name', 'overall', 'potential', 'age', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']]
df_24_filtered = df_2024[['short_name', 'overall']]

# Merge beide datasets op 'short_name'
merged_df = pd.merge(df_19_filtered, df_24_filtered, on='short_name', how='left', suffixes=('_19', '_24'))

# Bereken het verschil tussen potentieel en overall rating in FIFA 24
merged_df['potential_vs_overall'] = merged_df['overall_24'] - merged_df['potential']

# Maak een nieuwe kolom om aan te geven of de speler zijn potentieel heeft bereikt
merged_df['potential_reached'] = merged_df['potential_vs_overall'] >= 0

# Verwijder rijen met NaN-waarden in de relevante kolommen
merged_df.dropna(subset=['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic', 'overall_24', 'potential'], inplace=True)

# Titel van de Streamlit app
st.title("FIFA 19 vs FIFA 24: Is het Potentieel Uitgekomen?")

# Maak een lijst voor geselecteerde spelers
if 'selected_players' not in st.session_state:
    st.session_state.selected_players = []

# Slider voor maximale rating voor de geselecteerde speler
max_player_rating = st.slider('Selecteer een maximale rating voor de geselecteerde speler', min_value=50, max_value=95, value=90)

# Filter de beschikbare spelers op basis van de maximale rating
filtered_players = merged_df[merged_df['overall_24'] <= max_player_rating]

# Selectiebox voor het kiezen van een speler onder de 21 jaar
available_players = merged_df[~merged_df['short_name'].isin(st.session_state.selected_players)]['short_name'].unique()
player = st.selectbox('Selecteer een speler onder de 21 jaar', available_players)

# Filter de data voor de geselecteerde speler
player_data = filtered_players[filtered_players['short_name'] == player]

# Toon de statistieken van de geselecteerde speler
st.write(f"Naam: {player}")
st.write(f"Leeftijd in FIFA 19: {player_data['age'].values[0]}")
st.write(f"Potentieel uit FIFA 19: {player_data['potential'].values[0]}")
st.write(f"Overall in FIFA 24: {player_data['overall_24'].values[0]}")
st.write(f"Verschil tussen Potentieel en Overall: {player_data['potential_vs_overall'].values[0]}")

# Analyseer of het potentieel is uitgekomen
if player_data['potential_vs_overall'].values[0] >= 0:
    st.success("Ja, het potentieel is uitgekomen!")
else:
    st.error("Nee, het potentieel is niet uitgekomen.")

# Maak een visualisatie: aantal spelers dat zijn potentieel heeft bereikt vs niet
potential_reached_counts = merged_df['potential_reached'].value_counts()

# Plot de data in een bar chart met Plotly
fig = px.bar(x=['Potentieel bereikt', 'Potentieel niet bereikt'],
             y=potential_reached_counts,
             color=['Potentieel bereikt', 'Potentieel niet bereikt'],
             title="Aantal Spelers dat zijn Potentieel heeft Bereikt in FIFA 24",
             labels={'x': 'Categorie', 'y': 'Aantal Spelers'})

# Toon de grafiek in Streamlit
st.plotly_chart(fig)

