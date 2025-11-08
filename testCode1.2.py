import pandas as pd
from datetime import datetime
df = pd.read_csv(r"data.csv")
print(df.columns)

cuve_name = input("Entrez le nom de la cuve: ")
density = float(input("Entrez la densite de l'article: "))
H1 = float(input("Entrez le volume a vide: "))
#Cette ligne permet d'acceder a la ligne du nom de la cuve choisie
row = df[df['Cuve'] == cuve_name]
#Si le nom de la cuve existe dans le jeux de donnees
if not row.empty:
    #Cette ligne nous permet d'acceder a la ligne du nom de la cuve entree et la colomn voulue
    H_vide = float(row.iloc[0]['H.Vide'])
    #meme que la derniere sauf celle ci c'est pour le coefficient
    coeff = float(row.iloc[0]['Coefficient'])
    #La formule utilise pour avoir le resultat
    final_result = (H_vide - H1) * density * coeff
    print(f"The final result for {cuve_name} is: {final_result}")
    #ce code permet de creer un fichier csv ou sauvgarder les resultats obtenues
    result_data = pd.DataFrame({
        "Date": [datetime.now().strftime("%Y-%m-%d ")],
        "Cuve": [cuve_name],
        "Density": [density],
        "H1": [H1],
        "Result": [final_result]
    })
    result_file = "results_log.csv"
    try:
        old_data = pd.read_csv(result_file)
        updated_data = pd.concat([old_data, result_data], ignore_index=True)
        updated_data.to_csv(result_file, index=False)
    except FileNotFoundError:
        result_data.to_csv(result_file, index=False)
    print(f"✅ Result saved to '{result_file}' successfully!")
else:
    print("Cuve not found in the data.")
