# projet streamlit Mohamed ZENATI

# Objectifs :

L'objectif de ce projet est de créer une application simplifiée et de la publier avec un partage simplifié.

Le jeu de données étant très riche (40 variables nous sont données), il nous donne la possibilité d'expérimenté un tas de choses et de mieux se familiariser avec python et la visualisation de données en générale.


# 1. Chargement des données

Les données qui nous ont été fournis étaient trop volumineuse pour pouvoir être traité par Github. J'ai donc pris la décision d'échantillionné chacun des .CSV afin de réduire au maximum leurs tailles respectives. Plusieurs méthodes étaient proposés afin de réduire le volume de nos .CSV sans perdre de données.


# 2. Explorer et traiter : Nettoyage, prétraitement, transformation et enrichissement des données

J'ai d'abord chargé chacun de mes .CSV dans des dataframe. J'ai ensuite ouvert un .CSV afin de voir les 40 variables qui m'étaient proposés.

Par la suite, j'ai supprimé l'ensemble des colonnes qui m'étaient inutile pour le commencement.
Sur l'ensemble des colonnes que j'ai gardé, j'ai supprimé tout les doublons ainsi que les lignes vides.

Voulant dés le départ faire une courbe d'évolution entre chaque année, j'ai renomé certaines colonnes afin d'avoir une meilleure visualisation sur l'évolution que je contais effectuer.

J'ai aussi convertie certaines variables en "int","float","str" afin de les utilisés plus facilement.


# 3. Visualisation des données : fonctionnalité de l'application

Mon application est divisé en plusieurs partie. Pour chaque année, l'utilisateur peut visualisé les données pour la France entière, Paris, Marseille ou Lyon. J'ai voulu travaillé sur Paris, Lyon et Marseille car ce sont les 3 plus grosses ville de France et j'avais pour idée de base de comparer les données obtenus entre elles. Par manque de données (car j'ai du échantillionné chaque .CSV) et par manque de temps je n'ai pas pu faire de visuel comparant ces 3 villes.

Pour ce qui est des visuels, vous pourrez retrouver plusieurs carte, plusieurs histogrammes, plusieurs courbes, ...


 
