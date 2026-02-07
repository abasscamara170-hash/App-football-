import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Elite Safe Tips", page_icon="⚽")
st.title("⚽ Pronos Élite (1ère Div)")

API_KEY = "15d7247bbb3712f4858d3197e840724a"
URL = "https://v3.football.api-sports.io/odds"
HEADERS = {'x-apisports-key': API_KEY}

# Liste des IDs des premières divisions majeures
# 39=Premier League, 61=Ligue 1, 140=La Liga, 135=Serie A, 78=Bundesliga
MAJOR_LEAGUES = [39, 61, 140, 135, 78, 94, 13, 2, 3] 

if st.button('Générer Combiné Élite'):
    with st.spinner('Analyse des grandes ligues...'):
        matchs_trouves = []
        today = datetime.now().strftime('%Y-%m-%d')
        
        for league_id in MAJOR_LEAGUES:
            params = {"date": today, "league": league_id, "season": "2025"}
            res = requests.get(URL, headers=HEADERS, params=params)
            data = res.json()
            
            if data.get('response'):
                for item in data['response']:
                    league_name = item['league']['name']
                    for book in item.get('bookmakers', []):
                        if book['name'] == "Bet365":
                            for bet in book.get('bets', []):
                                for v in bet['values']:
                                    cote = float(v['odd'])
                                    if 1.05 <= cote <= 1.50:
                                        matchs_trouves.append({
                                            "ligue": league_name,
                                            "pari": bet['name'],
                                            "choix": v['value'],
                                            "cote": cote
                                        })
        
        if matchs_trouves:
            st.success(f"🔥 {len(matchs_trouves)} options trouvées dans les grandes ligues !")
            for m in matchs_trouves[:6]:
                st.info(f"🏆 {m['ligue']} : **{m['choix']}** ({m['pari']}) | Cote: `{m['cote']}`")
        else:
            st.warning("Pas encore de cotes disponibles pour les grandes ligues. Réessaie vers 10h !")
