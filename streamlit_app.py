import streamlit as st
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# Fonction pour récupérer les URLs des articles en brouillon avec pagination
def get_draft_urls(username, password, base_url):
    url = f"{base_url}/wp-json/wp/v2/posts?status=draft&per_page=100"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        posts = response.json()
        total_pages = int(response.headers.get('X-WP-TotalPages', 1))
        urls = []

        # Récupérer les articles de la première page
        for post in posts:
            categories = []
            if 'categories' in post:
                categories_ids = post['categories']
                for category_id in categories_ids:
                    category_response = requests.get(f"{base_url}/wp-json/wp/v2/categories/{category_id}", auth=HTTPBasicAuth(username, password))
                    if category_response.status_code == 200:
                        category_name = category_response.json().get('name', '')
                        categories.append(category_name)
            urls.append((base_url, post['link'], ', '.join(categories)))

        # Récupérer les articles des pages suivantes
        for page in range(2, total_pages + 1):
            page_url = f"{base_url}/wp-json/wp/v2/posts?status=draft&per_page=100&page={page}"
            page_response = requests.get(page_url, auth=HTTPBasicAuth(username, password))
            if page_response.status_code == 200:
                page_posts = page_response.json()
                for post in page_posts:
                    categories = []
                    if 'categories' in post:
                        categories_ids = post['categories']
                        for category_id in categories_ids:
                            category_response = requests.get(f"{base_url}/wp-json/wp/v2/categories/{category_id}", auth=HTTPBasicAuth(username, password))
                            if category_response.status_code == 200:
                                category_name = category_response.json().get('name', '')
                                categories.append(category_name)
                    urls.append((base_url, post['link'], ', '.join(categories)))

        return urls
    else:
        st.error(f"Erreur lors de la récupération des articles en brouillon pour {base_url}.")
        return []

# Interface utilisateur
st.title("Récupérateur d'URLs des Articles en Brouillon WordPress")

# Entrée des informations
username = st.text_input("Nom d'utilisateur WordPress")
password = st.text_input("Mot de passe WordPress", type="password")
base_urls = st.text_area("URLs de base de vos sites WordPress (une par ligne)")

# Bouton de récupération
if st.button("Récupérer les URLs"):
    if not username or not password or not base_urls:
        st.error("Veuillez remplir tous les champs.")
    else:
        base_urls_list = [url.strip() for url in base_urls.split("\n") if url.strip()]
        all_urls = []
        progress_bar = st.progress(0)
        total_sites = len(base_urls_list)

        for i, base_url in enumerate(base_urls_list):
            urls = get_draft_urls(username, password, base_url)
            if urls:
                all_urls.extend(urls)
            progress_bar.progress((i + 1) / total_sites)

        if all_urls:
            st.success("URLs des brouillons récupérés avec succès.")
            st.write("URLs des brouillons :")
            for site_url, draft_url, categories in all_urls:
                st.write(f"Site: {site_url}, Brouillon: {draft_url}, Thématique: {categories}")

            # Prévisualisation sous forme de tableau
            df = pd.DataFrame(all_urls, columns=['URL du site', 'URL du brouillon', 'Thématique'])
            st.write(df)
        else:
            st.info("Aucune URL de brouillon trouvée.")

# Gestion des erreurs
if st.button("Réinitialiser"):
    st.experimental_rerun()
