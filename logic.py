import pandas as pd
from datetime import datetime

def load_data(file_path):
    """Charger le fichier CSV"""
    return pd.read_csv(file_path)

def calculate_result(df, cuve_name, density, H1):
    """Faire le calcul principal"""
    row = df[df['Cuve'] == cuve_name]

    if row.empty:
        return None, "❌La Cuve est introuvable."
    
    H_vide = float(row.iloc[0]['H.Vide'])
    coeff = float(row.iloc[0]['Coefficient'])
    final_result = round((H_vide - H1) * density * coeff)

    # Sauvegarde du résultat
    result_file = "results_log.csv"
    result_data = pd.DataFrame({
        "Date": [datetime.now().strftime("%Y-%m-%d")],
        "Cuve": [cuve_name],
        "Densite": [density],
        "Result": [final_result]
    })

    try:
        old_data = pd.read_csv(result_file)
        last_date = old_data.iloc[-1]['Date']
        today_date = datetime.now().strftime("%Y-%m-%d")

        if last_date != today_date:
            empty_row = pd.DataFrame([{"Date": "", "Cuve": "", "Density": "", "H1": "", "Result": ""}])
            old_data = pd.concat([old_data, empty_row], ignore_index=True)

        updated_data = pd.concat([old_data, result_data], ignore_index=True)
        updated_data.to_csv(result_file, index=False)

    except FileNotFoundError:
        result_data.to_csv(result_file, index=False)

    return final_result, f"✅ Le resultat est sauvgarde dans **{result_file}** avec succes !"
