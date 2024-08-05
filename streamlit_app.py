import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

# Configuration de la page Streamlit
st.title('Récupération des URLs des Brouillons WordPress')

# Entrée pour les informations d'authentification
username = st.text_input('Nom d\'utilisateur WordPress')
password = st.text_input('Mot de passe WordPress', type='password')

# Entrée pour la base URL de WordPress
base_url = st.text_input('Base URL de WordPress', 'https://votresitewordpress.com')

# Bouton pour récupérer les URLs des brouillons
if st.button('Récupérer les URLs des Brouillons'):
    if username and password and base_url:
        # Fonction pour récupérer les URLs des brouillons
        def get_draft_urls(base_url, username, password):
            draft_urls = []
            page = 1

            while True:
                # Construire l'URL de l'API REST avec le paramètre de pagination
                url = f"{base_url}/wp-json/wp/v2/posts?status=draft&per_page=100&page={page}"
                
                # Effectuer la requête GET avec authentification
                response = requests.get(url, auth=HTTPBasicAuth(username, password))
                
                # Vérifier si la requête a réussi
                if response.status_code != 200:
                    st.error(f"Erreur lors de la récupération des données : {response.status_code}")
                    break
                
                # Extraire les articles de la réponse JSON
                posts = response.json()
                
                # Vérifier si des articles ont été retournés
                if not posts:
                    break
                
                # Ajouter les URLs des articles en brouillon à la liste
                for post in posts:
                    draft_urls.append(post['link'])
                
                page += 1

            return draft_urls

        # Récupérer les URLs des brouillons
        draft_urls = get_draft_urls(base_url, username, password)

        if draft_urls:
            # Afficher les URLs récupérées
            st.success('URLs des brouillons récupérées avec succès.')
            for url in draft_urls:
                st.write(url)
            
            # Enregistrer les URLs dans un fichier texte
            with open('draft_urls.txt', 'w') as file:
                for url in draft_urls:
                    file.write(f'{url}\n')

            st.download_button(
                label='Télécharger les URLs des Brouillons',
                data='\n'.join(draft_urls),
                file_name='draft_urls.txt',
                mime='text/plain'
            )
        else:
            st.warning('Aucun brouillon trouvé.')
    else:
        st.error('Veuillez entrer toutes les informations nécessaires.')
