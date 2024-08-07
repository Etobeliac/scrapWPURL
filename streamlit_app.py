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
    # ... (le reste de la fonction reste inchangé)

st.title("Récupérateur d'URLs et Contenu des Articles en Brouillon WordPress")

# ... (le reste du code reste inchangé jusqu'à la partie d'exportation)

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
