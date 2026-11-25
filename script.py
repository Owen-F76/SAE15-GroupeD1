from pathlib import Path
import pandas as pd

dossier_data = Path.cwd() / "data"

fichiers = {
    "antenne": "sup_antenne.txt",
    "bande": "sup_bande.txt",
    "emetteur": "sup_emetteur.txt",
    "station": "sup_station.txt",
    "support": "sup_support.txt",
}

# chargement + suppression des lignes vides
donnees = {}
for nom, nom_fichier in fichiers.items():
    tableau = pd.read_csv(dossier_data / nom_fichier, sep=";", low_memory=False)
    donnees[nom] = tableau.dropna(how="all")
    print(f"{nom}: {len(tableau)} lignes, {len(tableau) - len(donnees[nom])} vides supprimees")

# suppression des supports sans coordonnees
colonnes_coord = [
    "COR_NB_DG_LAT", "COR_NB_MN_LAT", "COR_NB_SC_LAT",
    "COR_NB_DG_LON", "COR_NB_MN_LON", "COR_NB_SC_LON",
]
support = donnees["support"].copy()
support[colonnes_coord] = support[colonnes_coord].apply(pd.to_numeric, errors="coerce")

nb_avant = len(support)
support = support.dropna(subset=colonnes_coord)
print(f"coordonnees manquantes supprimees: {nb_avant - len(support)}")
print("supports valides:", len(support))
