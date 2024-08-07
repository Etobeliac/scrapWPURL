import streamlit as st
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import html
import io
import re

def clean_html_content(content):
    # Supprimer toutes les balises HTML
    clean_text = re.sub(r'<[^>]+>', '', content)
    
    # Remplacer les caractères spéciaux par leurs équivalents HTML
    special_chars = {
        'é': '&eacute;', 'è': '&egrave;', 'ê': '&ecirc;', 'à': '&agrave;', 
        'â': '&acirc;', 'ô': '&ocirc;', 'ù': '&ugrave;', 'û': '&ucirc;', 
        'ç': '&ccedil;', 'É': '&Eacute;', 'È': '&Egrave;', 'Ê': '&Ecirc;', 
        'À': '&Agrave;', 'Â': '&Acirc;', 'Ô': '&Ocirc;', 'Ù': '&Ugrave;', 
        'Û': '&Ucirc;', 'Ç': '&Ccedil;'
    }
    for char, html_char in special_chars.items():
        clean_text = clean_text.replace(char, html_char)
    
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

            # Export en XLSX
            xlsx_buffer = io.BytesIO()
            with pd.ExcelWriter(xlsx_buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Articles')
            xlsx_data = xlsx_buffer.getvalue()
            
            st.download_button(
                label="Télécharger tous les résultats (XLSX)",
                data=xlsx_data,
                file_name="articles_brouillons.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("Aucun article en brouillon trouvé.")

if st.button("Réinitialiser"):
    st.experimental_rerun()
