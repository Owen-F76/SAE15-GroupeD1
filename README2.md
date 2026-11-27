# SAE 15 - Version 2

## Présentation

Ce projet consiste à analyser les données de l'ANFR sur les installations radioélectriques à l'aide de Python et de Pandas.

Le programme permet de réaliser cinq analyses :
- Le nombre d'installations par département.
- Les différentes technologies utilisées (2G, 3G, 4G et 5G).
- L'évolution des technologies au fil des années.
- Le classement des exploitants selon le nombre d'installations.
- La comparaison des exploitants et des technologies.

## Comment lancer le programme ?

**1. Cloner le dépôt GitHub**

Ouvrir un terminal et exécuter la commande suivante :

```bash
git clone LIEN_DU_DEPOT
```

Remplacer `LIEN_DU_DEPOT` par le lien du dépôt GitHub.

**2. Ouvrir le projet**

Se placer dans le dossier cloné :

```bash
cd SAE15-GroupeD1
```

Puis ouvrir ce dossier dans VS Code.

**3. Installer les bibliothèques nécessaires**

Dans le terminal, exécuter :

```bash
pip install pandas matplotlib
```

**4. Lancer le programme**

Exécuter la commande :

```bash
python script.py
```

## Organisation des fichiers

- script.py : contient le programme Python.
- `data/` : contient les fichiers de données de l'ANFR.

**Important :** ne pas déplacer le dossier `data` et ne pas modifier les noms des fichiers, sinon le programme risque de ne plus fonctionner.

## Résultats

Les résultats des analyses s'affichent dans le terminal. Certains graphiques s'ouvrent également pour faciliter la lecture des résultats.