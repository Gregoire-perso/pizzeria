# Pizzeria #

## Explication du jeu ##



## Fonctionnements statistiques ##

Une pizza est optimale si chaque ingrédient est présent 8 fois, qu'elle est cuite, et qu'il y a de la sauce tomate.

Une note entre 0 et 1 est donnée à chaque type d'ingrédient par un rapport (ingredient sur la pizza/ingredients attendus).

La note globale de l'attribution des ingrédients est ensuite calculée comme suit : 
		somme de la note des ingrédients individuels / nombre total d'ingrédients

La note globale des ingrédient diminue d'1% par ingrédient non demandé.

La note globale de la pizza diminue de 25% si la pizza n'est pas cuite.

La note globale de la pizza non cuite correspond à : 
		note des ingredients * 0.75 * 100

La note globale de la pizza si elle est cuie correspond à :
		note des ingredients * 0.10 * 100

Le pourboire correspond au calcul suivant :
		note globale de la pizza / 100 * 0.10 * prix de la pizza brute

