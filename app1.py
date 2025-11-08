import streamlit as st
import pandas as pd
from logic import load_data, calculate_result
from io import StringIO

# Add a logo
st.image("batimar.jpg", width=300)

# Title
st.title("Système Pour le Calcul de Stock")

# Load dataset
df = load_data("data.csv")

# Inputs
st.subheader("Entrer les données pour effectuer les calculs")

cuve_name = st.selectbox(
    "Entrez le nom de la cuve:",
    ['', 'T841', 'T805', 'T840', 'T301', 'T807', 'T808', 'T810', 'V110', 
     'C AGL Sy', 'T804', 'T809', 'T806', 'T811', 'T842', 'T843', 'Bassin 2', 
     'Bassin 3', 'Bassin 4', '1500- 1', '1500- 2', '1500- 3', '1500- 4', 
     '1500- 5', '1500-6', '500-1', '500-2', '500-3', '500-4', 'C130-1', 
     'C130-2', 'C130-3', 'C65- 1', 'C65- 2', 'C65- 3', 'C65- 4', 'C65- 5', 
     'C65- 6', 'C65- 7', 'C65- 8', 'C65- 9', 'C65- 10', 'C65- 11', 'C65- 12', 
     'C65- 13', 'C65- 14']
)

density = st.number_input("Entrez la densité de l'article", min_value=0.0, format="%.3f")
H1 = st.number_input("Entrez la hauteur à vide:", min_value=0.0, format="%.3f")

# Button
if st.button("Calculer"):
    result, message = calculate_result(df, cuve_name, density, H1)
    
    if result is None:
        st.error(message)
    else:
        st.success(f"Le résultat final pour la cuve **{cuve_name}** est: **{result:.3f}**")
        st.info(message)

        # Prepare CSV for instant download
        output_df = pd.DataFrame({
            "Date": [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Cuve": [cuve_name],
            "Densite": [density],
            "Hauteur vide": [H1],
            "Result": [result]
        })

        csv_buffer = StringIO()
        output_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        st.download_button(
            label="Télécharger le résultat en CSV",
            data=csv_buffer,
            file_name=f"result_{cuve_name}.csv",
            mime="text/csv"
        )


