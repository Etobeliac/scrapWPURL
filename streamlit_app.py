import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

# Fonction pour récupérer les URLs des articles en brouillon
def get_draft_urls(username, password, base_url):
    url = f"{base_url}/wp-json/wp/v2/posts?status=draft"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        posts = response.json()
        urls = [post['link'] for post in posts]
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
            for url in all_urls:
                st.write(url)

            # Option de téléchargement
            if st.button("Télécharger les URLs"):
                urls_text = "\n".join(all_urls)
                st.download_button(
                    label="Télécharger le fichier texte",
                    data=urls_text,
                    file_name="urls_brouillons.txt",
                    mime="text/plain"
                )
        else:
            st.info("Aucune URL de brouillon trouvée.")

# Gestion des erreurs
if st.button("Réinitialiser"):
    st.experimental_rerun()
