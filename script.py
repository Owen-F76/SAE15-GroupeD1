# SAE 15 - VERSION 2
# ANALYSE DES INSTALLATIONS RADIOELECTRIQUES DE L'ANFR

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# 1. CHARGEMENT DES DONNEES

DOSSIER = Path(__file__).resolve().parent
DATA = DOSSIER / "data"

station = pd.read_csv(DATA / "sup_station.txt", sep=";", low_memory=False)
support = pd.read_csv(DATA / "sup_support.txt", sep=";", low_memory=False)
emetteur = pd.read_csv(DATA / "sup_emetteur.txt", sep=";", low_memory=False)

print("       SAE 15 - PRESENTATION VERSION 2")

print("\nLes données de l'ANFR ont été chargées.")
print("Nous allons présenter les cinq analyses demandées.")


# 2. PREPARATION DES DONNEES

# Association des stations avec leurs départements
donnees_geo = station.merge(
    support[["STA_NM_ANFR", "COM_CD_INSEE"]],
    on="STA_NM_ANFR",
    how="left"
)

# Association des émetteurs avec les exploitants
donnees = emetteur.merge(
    station[["STA_NM_ANFR", "ADM_ID"]],
    on="STA_NM_ANFR",
    how="left"
)


# Identification des technologies
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

    return "Autre"


donnees["technologie"] = donnees["EMR_LB_SYSTEME"].apply(
    identifier_technologie
)


# 3. ANALYSE 1 : REPARTITION PAR DEPARTEMENT

print("\n----------------------------------------------")
print("ANALYSE 1 : REPARTITION PAR DEPARTEMENT")
print("----------------------------------------------")

repartition = (
    donnees_geo.groupby("COM_CD_INSEE")["STA_NM_ANFR"]
    .nunique()
    .sort_values(ascending=False)
)

print(repartition.to_string())

print("\nLes départements sont classés selon leur nombre d'installations.")

# Graphique des 10 premiers départements
repartition.head(10).plot(kind="bar", figsize=(10, 5))

plt.title("Les 10 départements ayant le plus d'installations")
plt.xlabel("Département")
plt.ylabel("Nombre d'installations")
plt.tight_layout()
plt.show()


# 4. ANALYSE 2 : TECHNOLOGIES UTILISEES

print("\n----------------------------------------------")
print("ANALYSE 2 : TECHNOLOGIES UTILISEES")
print("----------------------------------------------")

technologies = (
    donnees[donnees["technologie"].isin(["2G", "3G", "4G", "5G"])]
    .groupby("technologie")["STA_NM_ANFR"]
    .nunique()
    .reindex(["2G", "3G", "4G", "5G"], fill_value=0)
)

print(technologies.to_string())

print("\nCette analyse permet de comparer la présence des quatre technologies.")

technologies.plot(kind="bar", figsize=(8, 5))

plt.title("Répartition des installations par technologie")
plt.xlabel("Technologie")
plt.ylabel("Nombre de stations")
plt.tight_layout()
plt.show()


# 5. ANALYSE 3 : EVOLUTION DANS LE TEMPS

print("\n----------------------------------------------")
print("ANALYSE 3 : EVOLUTION DANS LE TEMPS")
print("----------------------------------------------")

donnees["date_service"] = pd.to_datetime(
    donnees["EMR_DT_SERVICE"],
    errors="coerce",
    dayfirst=True
)

donnees_dates = donnees.dropna(subset=["date_service"]).copy()

if not donnees_dates.empty:

    donnees_dates["annee"] = donnees_dates["date_service"].dt.year

    evolution = pd.crosstab(
        donnees_dates["annee"],
        donnees_dates["technologie"]
    )

    evolution = evolution.reindex(
        columns=["2G", "3G", "4G", "5G"],
        fill_value=0
    )

    print(evolution.to_string())

    print("\nCe graphique présente l'évolution des technologies selon les dates disponibles.")

    evolution.plot(figsize=(10, 5), marker="o")

    plt.title("Evolution des technologies dans le temps")
    plt.xlabel("Année")
    plt.ylabel("Nombre d'émetteurs")
    plt.legend(title="Technologie")
    plt.tight_layout()
    plt.show()

else:
    print("Les dates de mise en service ne sont pas exploitables.")
    print("Il n'est donc pas possible de présenter une évolution fiable.")



# 6. ANALYSE 4 : CLASSEMENT DES EXPLOITANTS

print("\n----------------------------------------------")
print("ANALYSE 4 : CLASSEMENT DES EXPLOITANTS")

classement = (
    donnees_geo.groupby("ADM_ID")["STA_NM_ANFR"]
    .nunique()
    .sort_values(ascending=False)
)

total = donnees_geo["STA_NM_ANFR"].nunique()

parts = classement / total * 100

resultat_classement = pd.DataFrame({
    "Nombre d'installations": classement,
    "Part du total (%)": parts.round(2)
})

print(resultat_classement.to_string())

print("\nCe classement permet de comparer le nombre d'installations par exploitant.")


# 7. ANALYSE 5 : EXPLOITANTS ET TECHNOLOGIES


print("\n----------------------------------------------")
print("ANALYSE 5 : EXPLOITANTS ET TECHNOLOGIES")


comparaison = pd.crosstab(
    donnees["ADM_ID"],
    donnees["technologie"],
    values=donnees["STA_NM_ANFR"],
    aggfunc=pd.Series.nunique
).fillna(0).astype(int)

comparaison = comparaison.reindex(
    columns=["2G", "3G", "4G", "5G"],
    fill_value=0
)

print(comparaison.to_string())

print("\nCette comparaison montre les technologies présentes chez chaque exploitant.")

comparaison.plot(kind="bar", figsize=(11, 6))

plt.title("Technologies utilisées par exploitant")
plt.xlabel("Exploitant")
plt.ylabel("Nombre de stations")
plt.legend(title="Technologie")
plt.tight_layout()
plt.show()



# 8. FIN DE LA PRESENTATION

print("      \n FIN DES CINQ ANALYSES")
