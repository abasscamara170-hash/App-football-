import streamlit as st
import requests
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Safe Ticket Generator", page_icon="⚽")
st.title("⚽ Générateur de Tickets Safe")

API_KEY = "15d7247bbb3712f4858d3197e840724a"
URL = "https://v3.football.api-sports.io/odds"
HEADERS = {'x-apisports-key': API_KEY}

st.sidebar.info("Cotes entre 1.09 et 1.30")

if st.button('Générer mon ticket du jour'):
    today = datetime.now().strftime('%Y-%m-%d')
    # On récupère les cotes (Exemple sur la Premier League ou une ligue majeure)
    with st.spinner('Recherche des meilleures opportunités...'):
        # On fait l'appel API
        response = requests.get(URL, headers=HEADERS, params={"date": today, "league": "39", "season": "2025"})
        data = response.json()
        
        matches = []
        if data.get('response'):
            for item in data['response']:
                match_name = f"{item['fixture']['status']['long']}" # On peut ajuster selon les besoins
                for book in item['bookmakers']:
                    if book['name'] == "Bet365": # Un bookmaker standard
                        for bet in book['bets']:
                            if bet['name'] == "Match Winner":
                                for val in bet['values']:
                                    cote = float(val['odd'])
                                    if 1.09 <= cote <= 1.30:
                                        matches.append({"name": val['value'], "cote": cote})

        if matches:
            st.success(f"Ticket trouvé !")
            total_cote = 1.0
            for m in matches[:3]: # On prend les 3 meilleurs
                st.write(f"🔹 **{m['name']}** | Cote: `{m['cote']}`")
                total_cote *= m['cote']
            st.metric("Cote Totale", round(total_cote, 2))
        else:
            st.warning("Pas de matchs 'safe' trouvés pour le moment. Réessayez plus tard !")
