
Durée : 1 heure


Sujet de l’examen : Binary Search

Contexte : La recherche dichotomique (binary search) est une méthode efficace pour trouver la position d’un élément dans une liste triée. Votre objectif est d’implémenter cette méthode, de la tester, et de l’étendre avec quelques variantes.

## Implémentation de la Recherche Dichotomique 

1.	Écrire une fonction `binary_search(sorted_list, target)` qui :
	- Prend en entrée une liste triée sorted_list (de nombres ou de chaînes de caractères, au choix, mais cohérente) et une valeur target à rechercher.
	- Retourne l’indice où la valeur target se trouve, si elle est présente dans la liste, avec la méthode de recherche dichotomique.
	- Retourne -1 si l’élément n’est pas trouvé.

Vous veillerez à ce que votre fonction soit itérative (pas de récursion).

>[!info]
Voici le détail de l’algorithme de recherche dichotomique :
> - Initialiser deux variables, low et high, qui représentent les indices de début et de fin de la liste à explorer. Au départ, low est à 0 et high est l'indice du dernier élément.
> - Répéter les étapes suivantes tant que low <= high :
> - Calculer l’indice qui se trouve au milieu de la liste, arrondi à l’entier inférieur.
> - Si l'élément à cet indice est égal à la valeur cherchée, retourner cet élément.
> - Sinon, si l'élément recherché est plus grand que l'élément au milieu, mettre à jour low pour être mid + 1. et donc chercher dans la moitié supérieure.
> - Sinon, mettre à jour high = mid - 1 pour chercher dans la moitié inférieure.
> - Si on sort de la boucle sans avoir trouvé la valeur, retourner -1.


Exemple:

![dichotomie](dichotomie.png)

Vidéo en plus : https://www.youtube.com/watch?v=0vOS48RiOag


2.	Tester votre fonction sur au moins trois cas différents :
- Une recherche où l’élément est présent au milieu de la liste.
- Une recherche où l’élément n’est pas présent.
- Une recherche où l’élément est présent aux extrémités (début ou fin) de la liste.

Afficher les résultats pour vérifier le bon comportement de la fonction.

## Gestion de Cas Spéciaux 

1.	Que se passe-t-il si la liste est vide ?
    - Modifier (ou vérifier) le comportement de binary_search pour qu’elle retourne -1 quand sorted_list est vide.
2.	Tester votre fonction sur une liste vide et une liste à un seul élément, pour s’assurer du bon fonctionnement dans ces cas particuliers.

## Variation – Première occurrence

Écrire une nouvelle fonction `binary_search_first_occurrence(sorted_list, target)` qui, dans une liste triée pouvant contenir des doublons, retourne l’indice de la première occurrence de target. Si l’élément n’est pas présent, retourner -1.

Tester cette fonction sur un exemple :
- `sorted_list = [1,2,2,2,3,4]` et `target = 2` doit retourner l’indice de la première occurrence de 2, donc 1.


