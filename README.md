# SAE15-GroupeD1
Projet en groupe sur la SAE15 ( Traitement de données ) 

Les modules qui seront a installé pour utiliser le programme sont :
Pandas et folium.


Logique algorithmique :

Début
	Importer les bibliothèques

	Définir le chemin du dossier du Project
	Définir le chemin du dossier des données

	Créer un dictionnaire pour les noms des fichiers
	Créer un dictionnaire vide pour stocker les données

	Pour chaque fichier faire :
       Récupérer le chemin du fichier
		Lire le fichier
		Stocker les données dans le dictionnaire
		Afficher le nombre de ligne
	Fin pour

	Copier les données de la table support
	
	Pour chaque colonne de coordonnées faire
		Convertir les valeurs en nombre
		Remplacer les valeurs incorrectes
	Fin pour 

	Pour chaque support faire 
		Calculer la latitude en degrés
		Calculer la longitude en degrés
		Si la direction de la latitude est sud alors
			Latitude prend la valeur latitude *(-1)
		Fin si
		Si la direction de la longitude est ouest alors
			Longitude prend la valeur longitude * (-1)
		Fin si
	Fin pour
	
	Supprimer les supports ayant des coordonnées invalides
	
	Pour chaque support faire
Si latitude est compris entre 41 et 52 et la longitude entre -6 et 10 alors
		Conserver le support
Sinon
		Exclure le support
Fin si
	Fin pour

	Afficher le nombre de support valide
	
       Créer une carte centrée sur la France
	
       Ajouter le fond de carte principal
	Ajouter le fond de carte alternatif
		
       Créer une liste de coordonnées géographique
	
	Ajouter les marqueurs sur la carte
	Regrouper les marqueurs proches

	Ajouter un sélecteur de fond de carte

	Enregistrer la carte en format HTML

	Afficher un message de réussite
	Afficher le nombre de support
	Afficher le chemin du fichier HTML
Fin


  
