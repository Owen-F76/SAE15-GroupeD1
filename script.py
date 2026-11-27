from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

dossier_data = Path.cwd() / "data"

# dossier de sortie (cree s'il n'existe pas)
dossier_resultat = Path.cwd() / "resultat"
dossier_resultat.mkdir(exist_ok=True)

fichiers = {
    "antenne": "sup_antenne.txt",
    "bande": "sup_bande.txt",
    "emetteur": "sup_emetteur.txt",
    "station": "sup_station.txt",
    "support": "sup_support.txt",
}

# 1. chargement + nettoyage (version 1)

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

station = donnees["station"]
emetteur = donnees["emetteur"]


# 2. preparation des donnees

# association des stations avec leurs departements
donnees_geo = station.merge(
    support[["STA_NM_ANFR", "COM_CD_INSEE"]],
    on="STA_NM_ANFR",
    how="left"
)

# association des emetteurs avec les exploitants
donnees_emetteur = emetteur.merge(
    station[["STA_NM_ANFR", "ADM_ID"]],
    on="STA_NM_ANFR",
    how="left"
)


# identification des technologies
def identifier_technologie(systeme):

    systeme = str(systeme).upper()

    if "5G" in systeme or "NR" in systeme:
        return "5G"

    elif "LTE" in systeme or "4G" in systeme:
        return "4G"

    elif any(mot in systeme for mot in ["UMTS", "WCDMA", "UTRA", "HSPA"]):
        return "3G"

    elif any(mot in systeme for mot in ["GSM", "GPRS", "EDGE"]):
        return "2G"

    return "autre"


donnees_emetteur["technologie"] = donnees_emetteur["EMR_LB_SYSTEME"].apply(
    identifier_technologie
)


# 3. analyse 1 : repartition par departement

repartition = (
    donnees_geo.groupby("COM_CD_INSEE")["STA_NM_ANFR"]
    .nunique()
    .sort_values(ascending=False)
)

# graphique des 10 premiers departements
repartition.head(10).plot(kind="bar", figsize=(10, 5))

plt.title("Les 10 départements ayant le plus d'installations")
plt.xlabel("Département")
plt.ylabel("Nombre d'installations")
plt.tight_layout()
plt.savefig(dossier_resultat / "analyse1_departements.png", dpi=150)
plt.close()


# 4. analyse 2 : technologies utilisees

technologies = (
    donnees_emetteur[donnees_emetteur["technologie"].isin(["2G", "3G", "4G", "5G"])]
    .groupby("technologie")["STA_NM_ANFR"]
    .nunique()
    .reindex(["2G", "3G", "4G", "5G"], fill_value=0)
)

technologies.plot(kind="bar", figsize=(8, 5))

plt.title("Répartition des installations par technologie")
plt.xlabel("Technologie")
plt.ylabel("Nombre de stations")
plt.tight_layout()
plt.savefig(dossier_resultat / "analyse2_technologies.png", dpi=150)
plt.close()


# 5. analyse 3 : evolution dans le temps

donnees_emetteur["date_service"] = pd.to_datetime(
    donnees_emetteur["EMR_DT_SERVICE"],
    errors="coerce",
    dayfirst=True
)

donnees_dates = donnees_emetteur.dropna(subset=["date_service"]).copy()

if not donnees_dates.empty:

    donnees_dates["annee"] = donnees_dates["date_service"].dt.year

    # on ignore les dates aberrantes (ex: annee 25) et les dates futures
    annee_actuelle = pd.Timestamp.now().year
    donnees_dates = donnees_dates[donnees_dates["annee"].between(1990, annee_actuelle)]

    evolution = pd.crosstab(
        donnees_dates["annee"],
        donnees_dates["technologie"]
    )

    evolution = evolution.reindex(
        columns=["2G", "3G", "4G", "5G"],
        fill_value=0
    )

    evolution.plot(figsize=(12, 6), marker="o")

    plt.title("Evolution des technologies dans le temps")
    plt.xlabel("Année")
    plt.ylabel("Nombre d'émetteurs")
    plt.legend(title="Technologie")
    plt.tight_layout()
    plt.savefig(dossier_resultat / "analyse3_evolution.png", dpi=150)
    plt.close()


# 6. analyse 4 : classement des exploitants

classement = (
    donnees_geo.groupby("ADM_ID")["STA_NM_ANFR"]
    .nunique()
    .sort_values(ascending=False)
)

total = donnees_geo["STA_NM_ANFR"].nunique()

parts = classement / total * 100

resultat_classement = pd.DataFrame({
    "nombre_installations": classement,
    "part_total_pct": parts.round(2)
})

# enregistrement du classement dans un fichier au format csv
resultat_classement.to_csv(
    dossier_resultat / "analyse4_classement_exploitants.txt",
    sep=";",
    encoding="utf-8"
)


# 7. analyse 5 : exploitants et technologies

comparaison = pd.crosstab(
    donnees_emetteur["ADM_ID"],
    donnees_emetteur["technologie"],
    values=donnees_emetteur["STA_NM_ANFR"],
    aggfunc=pd.Series.nunique
).fillna(0).astype(int)

comparaison = comparaison.reindex(
    columns=["2G", "3G", "4G", "5G"],
    fill_value=0
)

# on garde les 10 exploitants ayant le plus d'installations (voir analyse 4)
comparaison.index = comparaison.index.astype(int)
top_exploitants = classement.head(10).index.astype(int)
comparaison = comparaison.reindex(top_exploitants, fill_value=0)

comparaison.plot(kind="bar", figsize=(12, 6))

plt.title("Technologies utilisées par les 10 plus gros exploitants")
plt.xlabel("Exploitant (ADM_ID)")
plt.xticks(rotation=0)
plt.ylabel("Nombre de stations")
plt.legend(title="Technologie")
plt.tight_layout()
plt.savefig(dossier_resultat / "analyse5_exploitants_technologies.png", dpi=150)
plt.close()
