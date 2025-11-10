import streamlit as st
import pandas as pd
from logic import load_data, calculate_result
from io import StringIO
from datetime import datetime
# Add a logo
st.image("batimar.jpg", width=300)
# Title
st.title("Système Pour le Calcul de Stock")
# Load dataset
df = load_data("data.csv")
# Stocker les résultats dans la session
if "results_df" not in st.session_state:
    st.session_state.results_df = pd.DataFrame(columns=["Date", "Cuve", "Densite", "Resultat"])
# Inputs
st.subheader("Entrez les données pour effectuer les calculs")
cuve_name = st.selectbox(
    "Entrez le nom de la cuve:",
    ['', 'T841', 'T805', 'T840', 'T301','T820','T821','T822','T830','T831','T832', 
     'T807', 'T808', 'T810', 'V110', 'C AGL Sy', 'T804', 'T809', 'T806', 
     'T811', 'T842', 'T843', 'Bassin 2','Bassin 3', 'Bassin 4', '1500- 1',
     '1500- 2', '1500- 3', '1500- 4', '1500- 5', '1500-6', '500-1', '500-2',
     '500-3', '500-4', 'C130-1', 'C130-2', 'C130-3', 'C65- 1', 'C65- 2', 'C65- 3',
     'C65- 4', 'C65- 5', 'C65- 6', 'C65- 7', 'C65- 8', 'C65- 9', 
     'C65- 10', 'C65- 11', 'C65- 12', 'C65- 13', 'C65- 14']
)
density = st.number_input("Entrez la densité de l'article", min_value=0.0, format="%.2f")
H1 = st.number_input("Entrez la hauteur à vide:", min_value=000.0, format="%.2f")
# Button
if st.button("Calculer"):
    result, message = calculate_result(df, cuve_name, density, H1)
    if result is None:
        st.error("Une erreur est survenue : données invalides !")
    else:
        st.success(f"Le résultat final pour la cuve **{cuve_name}** est: **{result:.2f}**")
        # Ajouter le résultat au DataFrame de la session
        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Cuve": cuve_name,
            "Densite": density,
            "Hauteur vide": H1,
            "Resultat": result
        }
        st.session_state.results_df = pd.concat(
            [st.session_state.results_df, pd.DataFrame([new_row])],
            ignore_index=True
        )
# Afficher tous les résultats de la session
if not st.session_state.results_df.empty:
    st.subheader("Tous les résultats calculés dans cette session")
    st.dataframe(st.session_state.results_df)
    # Préparer le CSV à télécharger
    csv_buffer = StringIO()
    st.session_state.results_df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    # Bouton de téléchargement
    st.download_button(
        label="Télécharger tous les résultats en CSV",
        data=csv_data,
        file_name="resultats_session.csv",
        mime="text/csv"
    )


