import streamlit as st
import requests

st.set_page_config(page_title="Safe Multi-Live", page_icon="⚽")
st.title("⚽ Multi-Paris LIVE Safe")

API_KEY = "15d7247bbb3712f4858d3197e840724a"
# Changement ici : on utilise l'URL des cotes en DIRECT
URL = "https://v3.football.api-sports.io/odds/live"
HEADERS = {'x-apisports-key': API_KEY}

if st.button('Scanner les Matchs en Direct'):
    with st.spinner('Scan mondial des matchs en cours...'):
        # On appelle les cotes en Live
        res = requests.get(URL, headers=HEADERS)
        data = res.json()
        
        matchs = []
        if data.get('response'):
            for item in data['response']:
                league = item['league']['name']
                teams = f"{item['fixture']['status']['elapsed']}' - {item['fixture']['id']}"
                for bet in item.get('odds', []):
                    type_pari = bet['name']
                    for v in bet['values']:
                        cote = float(v['value'])
                        # Ta zone de sécurité
                        if 1.05 <= cote <= 1.50:
                            matchs.append({
                                "info": f"{league} ({teams})",
                                "pari": type_pari,
                                "choix": v['name'],
                                "cote": cote
                            })
        
        if matchs:
            st.success(f"🔥 {len(matchs)} opportunités trouvées !")
            for m in matchs[:10]:
                with st.expander(f"💰 Cote: {m['cote']} | {m['choix']}"):
                    st.write(f"**Ligue :** {m['info']}")
                    st.write(f"**Type :** {m['pari']}")
        else:
            st.warning("Rien en direct pour le moment. Réessaie dans quelques minutes.")
