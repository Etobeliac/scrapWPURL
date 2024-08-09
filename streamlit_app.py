import streamlit as st
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import io
import csv
import random
import re
import json

# Liste complète des ancres
ancres = [
    "En savoir plus", "Cliquez ici pour plus d'informations", "Découvrir davantage",
    "En apprendre davantage", "Visitez notre site", "Découvrez notre site",
    "En découvrir plus sur ce site", "Cliquez ici", "Plus d'infos ici",
    "Accédez au site", "Lire la suite", "Découvrez ici",
    "Suivez ce lien", "Visitez cette page", "En savoir plus ici",
    "Plus d'informations", "Visitez notre page", "Cliquez pour en savoir plus",
    "Apprenez-en plus ici", "Plus d'infos", "Ce site spécialiste dans le domaine",
    "Voir plus", "Explorez ici", "Consultez ce site",
    "Plus de détails", "Plus d'informations ici", "Pour en savoir plus",
    "Détails ici", "En savoir plus sur ce site", "Visitez ce site",
    "Découvrez davantage ici", "Pour plus d'infos", "Accédez à plus d'informations",
    "Visitez le site", "Cliquez pour plus de détails", "En découvrir davantage",
    "Découvrez-en plus ici", "Cliquez pour des informations supplémentaires", "Accédez à ce site",
    "Explorez notre site", "En savoir plus maintenant", "Consultez cette page",
    "Cliquez pour découvrir", "En savoir plus sur notre site", "Voir ici",
    "Pour plus de détails", "Plus de détails ici", "Découvrez plus",
    "Cliquez ici pour des infos supplémentaires", "En savoir plus sur cette page", "Détails supplémentaires",
    "Visitez ce lien", "Explorez ce site", "Plus d'informations maintenant",
    "Cliquez pour accéder", "Accédez à notre site", "Plus d'infos sur ce site",
    "Découvrez plus ici", "En apprendre plus ici", "Cliquez pour en apprendre plus",
    "Informations supplémentaires", "Accédez aux informations", "En savoir davantage ici",
    "Plus de détails sur ce site", "Visitez notre lien", "Cliquez ici pour découvrir",
    "Détails supplémentaires ici", "En savoir plus sur ce lien", "Explorez davantage",
    "Visitez ici", "Cliquez ici pour accéder", "En savoir plus sur notre page",
    "Plus de renseignements", "Détails sur ce site", "Cliquez ici pour voir plus",
    "En découvrir plus maintenant", "Cliquez pour voir plus", "Accédez à plus de détails",
    "Découvrez des informations supplémentaires", "Consultez le site", "Informations détaillées",
    "Visitez pour en savoir plus", "Cliquez pour voir les détails", "En savoir plus sur notre page",
    "Cliquez pour des détails supplémentaires", "Plus d'informations sur notre site", "En savoir plus sur cette page",
    "Accédez à des informations supplémentaires", "Cliquez ici pour explorer", "En découvrir plus ici",
    "Plus de détails sur notre site", "Découvrez ici", "Cliquez pour accéder aux détails",
    "Informations détaillées ici", "Explorez notre page", "Plus d'informations sur cette page",
    "En savoir plus sur ce lien", "Visitez pour plus de détails", "Cliquez pour des informations détaillées",
    "En savoir plus sur ce site", "Découvrez des détails ici", "Cliquez ici pour voir les détails",
    "Explorez notre lien", "Plus d'informations disponibles ici", "Cliquez pour plus d'informations",
    "En savoir plus sur notre site", "Cliquez ici pour plus d'informations", "Accédez à plus de détails ici",
    "Découvrez des informations supplémentaires ici", "Consultez pour en savoir plus", "Cliquez ici pour voir plus de détails",
    "En savoir plus sur notre lien", "Détails supplémentaires disponibles ici", "En savoir plus ici",
    "Visitez notre site pour plus de détails", "Cliquez pour en savoir plus", "Informations supplémentaires disponibles ici",
    "Accédez à des détails supplémentaires ici", "Cliquez pour découvrir plus", "En découvrir plus maintenant ici",
    "Visitez pour plus d'informations", "Cliquez ici pour des détails supplémentaires", "Accédez aux détails ici",
    "Plus d'informations disponibles maintenant", "En savoir plus sur notre lien", "Découvrez des détails supplémentaires ici",
    "Cliquez ici pour des informations plus détaillées", "Explorez ce lien", "Plus de détails disponibles ici",
    "Cliquez ici pour des informations supplémentaires", "En savoir plus sur cette page", "Consultez pour des détails supplémentaires",
    "Cliquez pour en savoir davantage", "Informations détaillées disponibles ici", "En savoir plus maintenant ici",
    "Accédez aux informations supplémentaires", "Cliquez pour voir plus d'informations", "En découvrir davantage ici",
    "Cliquez ici pour des informations complémentaires", "Visitez pour des détails supplémentaires", "Cliquez pour accéder à plus d'informations",
    "En savoir plus sur cette page", "Accédez à des détails complémentaires ici", "Découvrez plus de détails ici",
    "Cliquez ici pour des détails complémentaires", "Explorez pour en savoir plus", "Cliquez pour des informations complémentaires",
    "En savoir plus ici", "Visitez notre site pour des informations complémentaires", "Cliquez pour en savoir plus maintenant",
    "Informations complémentaires disponibles ici", "Accédez à des informations complémentaires ici", "Cliquez pour découvrir des détails complémentaires",
    "En découvrir plus ici maintenant", "Visitez pour des informations complémentaires", "Cliquez ici pour plus d'informations complémentaires",
    "Accédez aux informations complémentaires ici", "Plus d'informations complémentaires disponibles ici", "En savoir plus sur notre lien",
    "Découvrez des détails complémentaires ici", "Cliquez ici pour des informations plus détaillées", "Explorez ce lien maintenant",
    "Plus de détails complémentaires disponibles ici", "Cliquez ici pour des informations supplémentaires", "En savoir plus sur cette page",
    "Consultez pour des informations supplémentaires", "Cliquez pour en savoir davantage ici", "Informations complémentaires disponibles maintenant",
    "En savoir plus ici", "Accédez aux informations complémentaires", "Cliquez pour voir plus d'informations",
    "En découvrir davantage ici", "Cliquez ici pour des informations complémentaires", "Visitez pour des détails complémentaires",
    "Cliquez pour accéder à des informations supplémentaires", "En savoir plus sur cette page", "Accédez à des détails supplémentaires ici",
    "Découvrez plus de détails ici", "Cliquez ici pour des détails complémentaires", "Explorez pour en savoir plus",
    "Cliquez pour des informations complémentaires", "En savoir plus ici", "Visitez notre site pour des informations supplémentaires",
    "Cliquez pour en savoir plus maintenant", "Informations supplémentaires disponibles ici", "Accédez à des informations complémentaires ici",
    "Cliquez pour découvrir des détails supplémentaires", "En découvrir plus ici maintenant", "Visitez pour des informations supplémentaires",
    "Cliquez ici pour plus d'informations supplémentaires", "Accédez aux informations supplémentaires ici", "Plus d'informations supplémentaires disponibles ici",
    "En savoir plus sur notre lien", "Découvrez des détails supplémentaires ici", "Cliquez ici pour des informations plus détaillées",
    "Explorez ce lien maintenant", "Plus de détails supplémentaires disponibles ici", "Cliquez ici pour des informations supplémentaires",
    "En savoir plus sur cette page", "Consultez pour des informations supplémentaires",
    "Pour plus d'informations, cliquez ici", "Découvrez notre expertise", "En savoir plus sur nos services",
    "Explorez nos solutions", "Cliquez ici pour plus de détails", "Approfondissez le sujet",
    "Informations complémentaires disponibles", "Découvrez nos offres", "Pour en apprendre davantage",
    "Visitez notre page dédiée", "Cliquez pour explorer", "Plus d'informations à votre disposition",
    "Accédez à notre catalogue complet", "Découvrez nos références", "Pour une analyse approfondie",
    "Consultez nos ressources", "En savoir plus sur notre approche", "Découvrez nos cas d'études",
    "Cliquez ici pour une démo", "Explorez nos fonctionnalités", "Pour des informations détaillées"
]

def insert_anchor(content):
    anchor = random.choice(ancres)
    links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', content)
    for link in links:
        new_a_tag = f'<a href="{link}">{anchor}</a>'
        content = content.replace(f'<a href="{link}">', new_a_tag)
    return content

def get_draft_urls_and_content(username, password, base_url, max_articles):
    api_url = f"{base_url}/wp-json/wp/v2/posts"
    params = {
        "status": "draft",
        "per_page": max_articles
    }
    auth = HTTPBasicAuth(username, password)
    
    try:
        response = requests.get(api_url, params=params, auth=auth)
        response.raise_for_status()
        posts = response.json()
        
        data = []
        for post in posts:
            content = post['content']['rendered']
            modified_content = insert_anchor(content)
            data.append({
                'URL du site': base_url,
                'URL du brouillon': post['link'],
                'Thématique': ', '.join([tag['name'] for tag in post['tags']]) if post['tags'] else 'Non spécifié',
                'Contenu': content,
                'Contenu modifié': modified_content
            })
        
        return data
    except requests.RequestException as e:
        st.error(f"Erreur lors de la récupération des données: {str(e)}")
        return None

def save_progress(data):
    st.session_state.progress_data = data

def load_progress():
    return st.session_state.get('progress_data', None)

st.title("Récupérateur d'URLs et Contenu des Articles en Brouillon WordPress")

if 'wordpress_username' not in st.session_state:
    st.session_state.wordpress_username = ''
if 'base_urls' not in st.session_state:
    st.session_state.base_urls = ''
if 'progress_data' not in st.session_state:
    st.session_state.progress_data = None

username = st.text_input("Nom d'utilisateur WordPress", value=st.session_state.wordpress_username)
password = st.text_input("Mot de passe WordPress", type="password")
base_urls = st.text_area("URLs de base de vos sites WordPress (une par ligne)", value=st.session_state.base_urls)

if st.button("Sauvegarder les paramètres"):
    st.session_state.wordpress_username = username
    st.session_state.base_urls = base_urls
    st.success("Paramètres sauvegardés!")

if st.button("Récupérer les URLs et le Contenu"):
    if not username or not password or not base_urls:
        st.error("Veuillez remplir tous les champs.")
    else:
        base_urls_list = [url.strip() for url in base_urls.split("\n") if url.strip()]
        all_data = load_progress() or []
        progress_bar = st.progress(0)

        for i, base_url in enumerate(base_urls_list):
            st.write(f"Traitement du site : {base_url}")
            
            try:
                data = get_draft_urls_and_content(username, password, base_url, 100)
                if data:
                    all_data.extend(data)
                    st.write(f"Nombre d'articles trouvés pour {base_url}: {len(data)}")
                else:
                    st.write(f"Aucun article trouvé pour {base_url}")
                
                save_progress(all_data)
            except requests.RequestException as e:
                st.error(f"Erreur lors de la récupération des données pour {base_url}: {str(e)}")
            
            progress_bar.progress((i + 1) / len(base_urls_list))

        st.success("Récupération terminée.")

        if all_data:
            st.success(f"Articles en brouillon récupérés avec succès. Total: {len(all_data)} articles.")
            
            df = pd.DataFrame(all_data)
            st.write("Aperçu des données récupérées (avec un extrait du contenu) :")
            preview_df = df[['URL du site', 'URL du brouillon', 'Thématique', 'Contenu', 'Contenu modifié']].head(10).copy()
            preview_df['Contenu'] = preview_df['Contenu'].str[:100] + '...'
            preview_df['Contenu modifié'] = preview_df['Contenu modifié'].str[:100] + '...'
            st.write(preview_df)

            if st.button("Prévisualiser le contenu modifié"):
                article_index = st.selectbox("Choisir un article à prévisualiser", range(len(df)))
                st.write(df.iloc[article_index]['Contenu modifié'])

            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8-sig', sep=';')
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label="Télécharger tous les résultats (CSV)",
                data=csv_data.encode('utf-8-sig'),
                file_name="articles_brouillons.csv",
                mime="text/csv"
            )
        else:
            st.info("Aucun article en brouillon trouvé.")

if st.button("Réinitialiser"):
    st.session_state.progress_data = None
    st.experimental_rerun()
