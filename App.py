import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Safe Multi-Tips", page_icon="⚽")
st.title("⚽ Générateur Multi-Paris Safe")

API_KEY = "15d7247bbb3712f4858d3197e840724a"
URL = "https://v3.football.api-sports.io/odds"
HEADERS = {'x-apisports-key': API_KEY}

st.markdown("Recherche de cotes entre **1.05** et **1.50** sur tous les marchés.")

if st.button('Générer mon Combiné Multi-Options'):
    with st.spinner('Analyse de tous les marchés (Gagnant, Total, Handicap...)'):
        today = datetime.now().strftime('%Y-%m-%d')
        # On scanne les matchs du jour sans limite de ligue
        res = requests.get(URL, headers=HEADERS, params={"date": today})
        data = res.json()
        
        matchs = []
        if data.get('response'):
            for item in data['response']:
                league_name = item['league']['name']
                for book in item.get('bookmakers', []):
                    # On utilise souvent Bet365 ou Pinnacle car ils ont le plus d'options
                    if book['name'] in ["Bet365", "Pinnacle"]:
                        for bet in book.get('bets', []):
                            type_pari = bet['name'] # Ex: Goals Over/Under, Double Chance, etc.
                            for v in bet['values']:
                                cote = float(v['odd'])
                                if 1.05 <= cote <= 1.50:
                                    matchs.append({
                                        "ligue": league_name,
                                        "type": type_pari,
                                        "choix": v['value'],
                                        "cote": cote
                                    })
        
        if matchs:
            st.success(f"🔥 {len(matchs)} options safe trouvées !")
            # On mélange pour varier les tickets
            import random
            random.shuffle(matchs)
            
            for m in matchs[:10]: # On affiche les 10 meilleures options
                with st.expander(f"📍 {m['ligue']} - Cote: {m['cote']}"):
                    st.write(f"**Marché :** {m['type']}")
                    st.write(f"**Pronostic :** {m['choix']}")
        else:
            st.warning("Aucune option trouvée. Les cotes varient vite, réessaie plus tard !")
