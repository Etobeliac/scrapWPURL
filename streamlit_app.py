import streamlit as st
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import html
import io
import re
import csv

def clean_html_content(content):
    # Supprimer toutes les balises HTML
    clean_text = re.sub(r'<[^>]+>', '', content)
    # Remplacer les sauts de ligne par des espaces
    clean_text = re.sub(r'\n', ' ', clean_text)
    # Supprimer les espaces multiples
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text.strip()

def get_draft_urls_and_content(username, password, base_url):
    url = f"{base_url}/wp-json/wp/v2/posts?status=draft&per_page=100"
    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        posts = response.json()
        total_pages = int(response.headers.get('X-WP-TotalPages', 1))
        urls_and_content = []

        for page in range(1, total_pages + 1):
            page_url = f"{url}&page={page}"
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
                    
                    content_html = post.get('content', {}).get('rendered', '')
                    cleaned_content = clean_html_content(content_html)
                    
                    urls_and_content.append({
                        'URL du site': base_url,
                        'URL du brouillon': post['link'],
                        'Thématique': ', '.join(categories),
                        'Contenu': cleaned_content
                    })
            else:
                st.error(f"Erreur lors de la récupération de la page {page} pour {base_url}.")
                break

        return urls_and_content
    else:
        st.error(f"Erreur lors de la récupération des articles en brouillon pour {base_url}.")
        return []

st.title("Récupérateur d'URLs et Contenu des Articles en Brouillon WordPress")

username = st.text_input("Nom d'utilisateur WordPress")
password = st.text_input("Mot de passe WordPress", type="password")
base_urls = st.text_area("URLs de base de vos sites WordPress (une par ligne)")

if st.button("Récupérer les URLs et le Contenu"):
    if not username or not password or not base_urls:
        st.error("Veuillez remplir tous les champs.")
    else:
        base_urls_list = [url.strip() for url in base_urls.split("\n") if url.strip()]
        all_data = []
        progress_bar = st.progress(0)

        for i, base_url in enumerate(base_urls_list):
            st.write(f"Traitement du site : {base_url}")
            
            data = get_draft_urls_and_content(username, password, base_url)
            if data:
                all_data.extend(data)
                st.write(f"Nombre d'articles trouvés pour {base_url}: {len(data)}")
            else:
                st.write(f"Aucun article trouvé pour {base_url}")
            
            progress_bar.progress((i + 1) / len(base_urls_list))

        st.success("Récupération terminée.")

        if all_data:
            st.success(f"Articles en brouillon récupérés avec succès. Total: {len(all_data)} articles.")
            
            df = pd.DataFrame(all_data)
            st.write("Aperçu des données récupérées (avec un extrait du contenu) :")
            preview_df = df[['URL du site', 'URL du brouillon', 'Thématique', 'Contenu']].head(10).copy()
            preview_df['Contenu'] = preview_df['Contenu'].str[:100] + '...'
            st.write(preview_df)

            # Export en CSV avec un encodage spécifique
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8-sig')
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label="Télécharger tous les résultats (CSV)",
                data=csv_data,
                file_name="articles_brouillons.csv",
                mime="text/csv"
            )
        else:
            st.info("Aucun article en brouillon trouvé.")

if st.button("Réinitialiser"):
    st.experimental_rerun()
