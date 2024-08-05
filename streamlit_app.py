import streamlit as st
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
from io import BytesIO

# Fonction pour récupérer les URLs des articles en brouillon
def get_draft_urls(username, password, base_url):
    url = f"{base_url}/wp-json/wp/v2/posts?status=draft"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        posts = response.json()
        urls = [(base_url, post['link'], post.get('categories', [])) for post in posts]
        return urls
    else:
        st.error(f"Erreur lors de la récupération des articles en brouillon pour {base_url}.")
        return []

# Interface utilisateur
st.title("Récupérateur d'URLs des Articles en Brouillon WordPress")

# Entrée des informations
username = st.text_input("Nom d'utilisateur WordPress")
password = st.text_input("Mot de passe WordPress", type="password")
base_urls = st.text_area("URLs de base de vos sites WordPress (séparées par des virgules)")

# Bouton de récupération
if st.button("Récupérer les URLs"):
    if not username or not password or not base_urls:
        st.error("Veuillez remplir tous les champs.")
    else:
        base_urls_list = [url.strip() for url in base_urls.split(",")]
        all_urls = []
        for base_url in base_urls_list:
            urls = get_draft_urls(username, password, base_url)
            if urls:
                all_urls.extend(urls)

        if all_urls:
            st.success("URLs des brouillons récupérés avec succès.")
            st.write("URLs des brouillons :")
            for site_url, draft_url, categories in all_urls:
                st.write(f"Site: {site_url}, Brouillon: {draft_url}, Thématique: {', '.join(categories)}")

            # Option de téléchargement
            if st.button("Télécharger les URLs"):
                df = pd.DataFrame(all_urls, columns=['URL du site', 'URL du brouillon', 'Thématique'])
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False)
                output.seek(0)

                st.download_button(
                    label="Télécharger le fichier Excel",
                    data=output,
                    file_name="urls_brouillons.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.info("Aucune URL de brouillon trouvée.")

# Gestion des erreurs
if st.button("Réinitialiser"):
    st.experimental_rerun()