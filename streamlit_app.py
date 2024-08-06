import streamlit as st
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import time

def get_draft_urls(username, password, base_url):
    # ... (cette fonction reste inchangée)

st.title("Récupérateur d'URLs des Articles en Brouillon WordPress")

username = st.text_input("Nom d'utilisateur WordPress")
password = st.text_input("Mot de passe WordPress", type="password")
base_urls = st.text_area("URLs de base de vos sites WordPress (une par ligne)")

if 'progress' not in st.session_state:
    st.session_state.progress = 0
    st.session_state.progress_text = ""

progress_bar = st.progress(st.session_state.progress)
progress_text = st.empty()
progress_text.text(st.session_state.progress_text)

if st.button("Récupérer les URLs"):
    if not username or not password or not base_urls:
        st.error("Veuillez remplir tous les champs.")
    else:
        base_urls_list = [url.strip() for url in base_urls.split("\n") if url.strip()]
        all_urls = []
        total_sites = len(base_urls_list)
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
            
            st.session_state.progress = progress
            st.session_state.progress_text = f"Progression globale: {progress:.1%} - Temps restant estimé: {int(estimated_remaining_time)} secondes"
            
            progress_bar.progress(st.session_state.progress)
            progress_text.text(st.session_state.progress_text)
            
            time.sleep(0.1)

        st.session_state.progress_text = "Récupération terminée."
        progress_text.text(st.session_state.progress_text)

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
    st.session_state.progress = 0
    st.session_state.progress_text = ""
    st.experimental_rerun()
