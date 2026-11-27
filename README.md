# SAÉ 1.5 — Traitement de données ANFR

**Groupe D1 | BUT Réseaux et Télécommunications | Python**


## 1. Présentation

Ce projet consiste à analyser les données de l'ANFR sur les installations radioélectriques à l'aide de Python et de Pandas.
Le programme permet de réaliser cinq analyses :

Le nombre d'installations par département.
Les différentes technologies utilisées (2G, 3G, 4G et 5G).
L'évolution des technologies au fil des années.
Le classement des exploitants selon le nombre d'installations.
La comparaison des exploitants et des technologies.

## 2. Structure du projet

SAE15-GroupeD1/
├── README.md           
├── script.py           
└── data/               
    ├── sup_antenne.txt
    ├── sup_bande.txt
    ├── sup_emetteur.txt
    ├── sup_station.txt
    └── sup_support.txt


## 3. Installation et utilisation

### 3.1. Prérequis



| Outil | Rôle | Nécessité |
| --- | --- | --- |
| Python 3 | Exécution du programme | Obligatoire |
| Pandas | Lecture, nettoyage et agrégation des données | Obligatoire |
| Matplotlib | Création des graphiques | Obligatoire |
| pathlib | Gestion des chemins de fichiers | Inclus dans Python |




### 3.2. Récupérer le projet

1. Cloner le dépôt GitHub
Ouvrir un terminal et exécuter la commande suivante :
git clone LIEN_DU_DEPOT
Remplacer LIEN_DU_DEPOT par le lien du dépôt GitHub.

2. Ouvrir le projet
Se placer dans le dossier cloné :
cd SAE15-GroupeD1
Puis ouvrir ce dossier dans VS Code.

3. Installer les bibliothèques nécessaires
Dans le terminal, exécuter :
pip install pandas matplotlib

4. mettre le dossier data doit être aux mêmes endroits que le scripte 

5. Lancer le programme



## 4. Démarche algorithmique


DEBUT

    Importer pathlib, pandas et matplotlib

    Définir le chemin du dossier data

    Créer un dictionnaire contenant les noms des 5 fichiers :
        - antenne
        - bande
        - emetteur
        - station
        - support

    Créer un dictionnaire vide pour les données


    pour chaque fichier du dictionnaire faire
        Lire le fichier CSV avec le séparateur ";"
        Supprimer les lignes entièrement vides
        Stocker les données dans le dictionnaire
        Afficher le nombre de lignes et les lignes supprimées
    Fin pour

    Copier les données des supports

    Convertir les colonnes de coordonnées en nombres
    Remplacer les valeurs incorrectes par des valeurs manquantes
    Supprimer les supports sans coordonnées complètes
    Afficher le nombre de supports conservés

    Récupérer les données des stations et des émetteurs

    Associer les stations aux départements
    Associer les émetteurs aux exploitants

    Définir une fonction d'identification des technologies

    pour chaque système radioélectrique faire
        Convertir son nom en majuscules

        Si le système contient 5G ou NR alors
            Technologie = 5G
        Sinon si le système contient LTE ou 4G alors
            Technologie = 4G
        Sinon si le système correspond à UMTS, WCDMA,
        UTRA ou HSPA alors
            Technologie = 3G
        Sinon si le système correspond à GSM, GPRS
        ou EDGE alors
            Technologie = 2G
        Sinon
            Technologie = autre
        Fin si
    Fin pour


    Regrouper les stations par département
    Compter les installations différentes
    Trier les départements par ordre décroissant
    Afficher les résultats
    Créer un graphique des 10 premiers départements


    Conserver les technologies 2G, 3G, 4G et 5G
    Regrouper les installations par technologie
    Compter les stations différentes
    Afficher les résultats
    Créer un graphique en barres


    Convertir les dates de mise en service
    Supprimer les dates invalides

    Si des dates exploitables existent alors
        Extraire l'année de chaque date
        Regrouper les émetteurs par année et technologie
        Compter les émetteurs
        Afficher les résultats
        Créer un graphique d'évolution
    Sinon
        Afficher un message d'erreur
    Fin si

    Regrouper les installations par exploitant
    Compter les installations différentes
    Trier les exploitants par ordre décroissant
    Calculer le pourcentage de chaque exploitant
    Afficher le classement et les pourcentages


    Croiser les données des exploitants et des technologies
    Compter les stations différentes pour chaque combinaison
    Remplacer les valeurs manquantes par zéro
    Afficher le tableau comparatif
    Créer un graphique en barres

    Afficher la fin des cinq analyses

Fin



## 5. Limites et perspectives

### Limites

- Le nettoyage peut exclure certaines données incomplètes.
- La classification par mots-clés peut produire des erreurs si les libellés évoluent.
- Les pourcentages d’installations ne constituent pas des parts de marché en nombre d’abonnés.
- Le regroupement par date de mise en service ne suffit pas à reconstituer l’état historique complet du réseau.


**Projet pédagogique — SAÉ 15 — Groupe D1**

Source des données : Agence nationale des fréquences (ANFR).

