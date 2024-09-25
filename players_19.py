import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader(r"C:\Users\goedh\Downloads\players_19.csv", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df.head())

# Laad de data
df = pd.read_csv(r"C:\Users\goedh\Downloads\players_19.csv")

# Categorieën voor posities
aanval_posities = ['ST', 'CF', 'LW', 'RW', 'LF', 'RF']
middenveld_posities = ['CAM', 'CM', 'LM', 'RM', 'CDM', 'LAM', 'RAM', 'LCM', 'RCM']
verdediging_posities = ['CB', 'LB', 'RB', 'LWB', 'RWB', 'LCB', 'RCB', 'LDM', 'RDM']
keeper_posities = ['GK']

# Voeg de optie voor alle posities toe
positie_categorieen = ['Alle posities', 'Aanval', 'Middenveld', 'Verdediging', 'Keeper']

# Titel van de applicatie
st.title("FIFA 19 Spelerstatistieken - Ontdek de Beste Spelers")

# Dropdown-menu voor positie categorie
positie_categorie = st.selectbox('Kies een categorie', options=positie_categorieen)

# Filter de data op basis van de geselecteerde categorie
if positie_categorie == 'Aanval':
    # Filteren op aanvallende posities
    filtered_df = df[df['player_positions'].apply(lambda x: any(pos in x for pos in aanval_posities))]
elif positie_categorie == 'Middenveld':
    # Filteren op middenveld posities
    filtered_df = df[df['player_positions'].apply(lambda x: any(pos in x for pos in middenveld_posities))]
elif positie_categorie == 'Verdediging':
    # Filteren op verdediging posities
    filtered_df = df[df['player_positions'].apply(lambda x: any(pos in x for pos in verdediging_posities))]
elif positie_categorie == 'Keeper':
    # Filteren op keeper posities
    filtered_df = df[df['player_positions'].isin(keeper_posities)]
else:
    filtered_df = df  # Voor 'Alle posities', gebruik de volledige dataset

# Slider voor algemene beoordeling
overall = st.slider('Selecteer een minimale algemene beoordeling (Overall)', min_value=50, max_value=99, value=75)
filtered_df = filtered_df[filtered_df['overall'] >= overall]

# Dropdown-menu voor clubs
club = st.selectbox('Selecteer een club om spelers te zien', options=['Alle clubs'] + list(df['club'].unique()))
if club != 'Alle clubs':
    filtered_df = filtered_df[filtered_df['club'] == club]

# Checkbox voor aanvallende statistieken
if st.checkbox('Toon aanvallende statistieken'):
    st.write(filtered_df[['short_name', 'shooting', 'passing', 'dribbling']])

# Checkbox voor verdedigende statistieken
if st.checkbox('Toon verdedigende statistieken'):
    st.write(filtered_df[['short_name', 'defending', 'physic']])

# Lijst met gefilterde spelers weergeven
st.dataframe(filtered_df[['short_name', 'club', 'overall', 'potential', 'age', 'value_eur']])

# Optionele informatie in de sidebar
st.sidebar.header('Hulp en Informatie')
st.sidebar.info("""
    Gebruik de dropdown-menu's om spelers te filteren op basis van positie en club. 
    Je kunt ook de minimale algemene beoordeling aanpassen om spelers te vinden die aan jouw criteria voldoen.
""")




