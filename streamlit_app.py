import streamlit as st
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import time

def get_draft_urls(username, password, base_url):
    url = f"{base_url}/wp-json/wp/v2/posts?status=draft&per_page=100"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        posts = response.json()
        total_pages = int(response.headers.get('X-WP-TotalPages', 1))
        urls = []

        for page in range(1, total_pages + 1):
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
            else:
                st.error(f"Erreur lors de la récupération de la page {page} pour {base_url}.")
                break

        return urls
    else:
        st.error(f"Erreur lors de la récupération des articles en brouillon pour {base_url}.")
        return []

st.title("Récupérateur d'URLs des Articles en Brouillon WordPress")

username = st.text_input("Nom d'utilisateur WordPress")
password = st.text_input("Mot de passe WordPress", type="password")
base_urls = st.text_area("URLs de base de vos sites WordPress (une par ligne)")

if st.button("Récupérer les URLs"):
    if not username or not password or not base_urls:
        st.error("Veuillez remplir tous les champs.")
    else:
        base_urls_list = [url.strip() for url in base_urls.split("\n") if url.strip()]
        all_urls = []
        total_sites = len(base_urls_list)
        progress_bar = st.progress(0)
        progress_text = st.empty()
        start_time = time.time()

        for i, base_url in enumerate(base_urls_list):
            st.write(f"Traitement du site : {base_url}")
            
            urls = get_draft_urls(username, password, base_url)
            if urls:
                all_urls.extend(urls)
                st.write(f"Nombre d'URLs trouvées pour {base_url}: {len(urls)}")
            else:
                st.write(f"Aucune URL trouvée pour {base_url}")
            
            progress = (i + 1) / total_sites
            elapsed_time = time.time() - start_time
            estimated_total_time = elapsed_time / progress if progress > 0 else 0
            estimated_remaining_time = max(estimated_total_time - elapsed_time, 0)
            
            progress_bar.progress(progress)
            progress_text.text(f"Progression globale: {int(progress * 100)}% - Temps restant estimé: {int(estimated_remaining_time)} secondes")
            time.sleep(0.1)

        progress_text.text("Récupération terminée.")

        if all_urls:
            st.success(f"URLs des brouillons récupérés avec succès. Total: {len(all_urls)} URLs.")
            st.write("Aperçu des URLs des brouillons :")

            df = pd.DataFrame(all_urls, columns=['URL du site', 'URL du brouillon', 'Thématique'])
            st.write(df.head(10))

            csv = df.to_csv(index=False)
            st.download_button(
                label="Télécharger tous les résultats (CSV)",
                data=csv,
                file_name="urls_brouillons.csv",
                mime="text/csv",
            )
        else:
            st.info("Aucune URL de brouillon trouvée.")

if st.button("Réinitialiser"):
    st.experimental_rerun()
