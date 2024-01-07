Projet Hello DBMS

Le projet DBMS vise l'acquisition des competences SQL, HTML, Python et Flask.

J'ai utilisé DBeaver pour la création de mes bases de données et SQLite. Les differentes requettes SQL je les ai effectué via l'editeur SQL de DBeaver ensuite j'ai utilisé VSCode pour faire la partie du Job 9.
Dans cette partie nous utilisont Flask pour analyser et afficher les emissions de CO2 pour les pays que nous avons dans notre fichier csv.
A travers defferents consignes nous faisons des liens via des routes entre le fichier python et notre html et on affiche les resultats en localhost.
On exécute l'application Flask à partir de : `python app.py`
On accéde à l'application dans le navigateur : Running on http://127.0.0.1:5000
Nous avons differentes pages http pour afficher les résultats.
Sur la page d'accueil nous avons nos deux tables; Country et World
Sur la page test nous avons le Pays qui émet le plus de CO2 (Albanie) mais c'est juste une page de test
Sur la page analysis nous avons un tableau avec les émissions de CO2 par source en Pourcentage
Sur la page contribution nous avons la contribution des sources en emissions de CO2
Enfin sur la dérnière page; contibution_filtered nous avons modifié l'application Flask afin de pouvoir filtrer nos données selon un pays
sélectionnable depuis une selection box.
Nous affichons aussi l'emission totale de CO2 par rapport au pays qui est selectionné et on clacule le nombre d'arbres nécessaires pour absorber le CO2 par an
