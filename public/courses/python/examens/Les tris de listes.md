# Examen 1 : Tri à Bulles (Bubble Sort)

Durée : 30 minutes

Explications du tri à bulles: Le tri à bulles compare des paires d’éléments adjacents dans une liste et les échange s’ils ne sont pas dans le bon ordre (du plus petit au plus grand). On répète ce processus autant de fois que nécessaire jusqu’à ce que la liste soit totalement triée. L’idée est que, comme des bulles dans l’eau, les plus grands éléments « remontent » progressivement vers la fin de la liste.

Algorithme :
1.	On regarde la liste du début à la fin.
2.	Pour chaque paire d’éléments (positions i et i+1), on compare :
    -	Si l’élément à gauche est plus grand, on échange.
    -	Sinon, on ne fait rien.
3.	On recommence plusieurs passages tant qu’on a fait au moins un échange.


Cette méthode est très simple à comprendre mais peu performante quand la liste devient grande.

**Exemple de fonctionnement**

Liste initiale : [5, 3, 8, 6, 2]

-	Passage 1 :
	-	Compare 5 et 3 → 5 > 3, on échange → [3, 5, 8, 6, 2]
	-	Compare 5 et 8 → 5 < 8, pas d’échange → [3, 5, 8, 6, 2]
	-	Compare 8 et 6 → 8 > 6, on échange → [3, 5, 6, 8, 2]
	-	Compare 8 et 2 → 8 > 2, on échange → [3, 5, 6, 2, 8]
-	Passage 2 :
	-	Compare 3 et 5 → 3 < 5, pas d’échange → [3, 5, 6, 2, 8]
	-	Compare 5 et 6 → 5 < 6, pas d’échange → [3, 5, 6, 2, 8]
	-	Compare 6 et 2 → 6 > 2, on échange → [3, 5, 2, 6, 8]
	-	Compare 6 et 8 → 6 < 8, pas d’échange → [3, 5, 2, 6, 8]
-	Passage 3 :
	-	Compare 3 et 5 → pas d’échange
	-	Compare 5 et 2 → 5 > 2, on échange → [3, 2, 5, 6, 8]
	-	Compare 5 et 6 → pas d’échange
	-	Compare 6 et 8 → pas d’échange
-	Passage 4 :
	-	Compare 3 et 2 → 3 > 2, on échange → [2, 3, 5, 6, 8]
	-	Compare 3 et 5 → pas d’échange
	-	Compare 5 et 6 → pas d’échange
	-	Compare 6 et 8 → pas d’échange
	-	On constate maintenant qu’aucun échange n’est nécessaire : la liste est triée.




# Examen 2 : Tri Rapide (Quick Sort)

Durée : 30 minutes

Explications du tri rapide: Le tri rapide (quick sort) est basé sur l’idée de choisir un pivot dans la liste et de séparer (partitionner) tous les éléments en deux sous-listes :
- Les éléments inférieurs ou égaux au pivot
- Les éléments supérieurs au pivot

On trie ensuite récursivement ces deux sous-listes, puis on combine le tout pour obtenir la liste finale triée.

Étapes principales :
1.	Choisir un pivot (par exemple, le dernier élément de la liste).
2.	Créer deux sous-listes :
      -	petits pour ceux qui sont <= pivot
      -	grands pour ceux qui sont > pivot
3.	Appliquer récursivement quick sort sur petits et grands.
4.	Combiner : (tri(petits)) + [pivot] + (tri(grands)).

**Exemple de fonctionnement**

Liste initiale : [7, 2, 8, 1, 5]

- On choisit le pivot = 5 (le dernier élément).
  - petits = [2, 1] (car 7 et 8 sont > 5)
  - grands = [7, 8]
  - On trie récursivement [2, 1] (pivot=1, petits=[], grands=[2]) → [1, 2]
  - On trie récursivement [7, 8] → c’est déjà trié → [7, 8]
  - On combine : [1, 2] + [5] + [7, 8] → [1, 2, 5, 7, 8].




# Examen 3 : Tri par Insertion (Insertion Sort)

Durée : 30 minutes

Explications du tri par insertion: Le tri par insertion consiste à parcourir la liste élément par élément, en considérant que les éléments avant la position courante sont déjà triés. On « insère » alors le nouvel élément dans la partie déjà triée à la bonne place.

Étapes principales :
1.	On commence au deuxième élément de la liste (car le premier est déjà « trié » tout seul).
2.	On prend la valeur courante (disons `val`) et on la compare aux éléments situés avant elle.
3.	Tant qu’un élément précédent est plus grand que `val`, on le décale d’une position vers la droite.
4.	Quand on a trouvé l’emplacement correct, on place `val`.

Cette méthode est très efficace si la liste est déjà presque triée, mais devient moins efficace sur de très grandes listes totalement désordonnées.

Exemple de fonctionnement

Liste initiale : [3, 1, 2]

-	i = 1 : élément courant = 1
    -	Compare avec 3 (index 0) : 3 > 1, on décale 3 → la liste devient [3, 3, 2]
    -	On insère 1 au début → [1, 3, 2]
-	i = 2 : élément courant = 2
    -	Compare avec 3 (index 1) : 3 > 2, on décale 3 → la liste devient [1, 3, 3]
    -	Compare avec 1 (index 0) : 1 < 2, on s’arrête et on insère 2 → [1, 2, 3]



# Examen 4 : Tri par Fusion (Merge Sort)

Durée : 30 minutes

Explications du tri par fusion: Le tri par fusion (merge sort) est une technique « diviser pour régner » :
1.	Diviser la liste en deux moitiés.
2.	Trier chacune des moitiés de façon récursive.
3.	Fusionner (merge) les deux moitiés triées pour former une liste globale triée.

L’intérêt : la fusion de deux listes déjà triées se fait en temps linéaire par rapport à la taille totale des deux listes. C’est un algorithme en général plus rapide que bubble sort ou insertion sort pour des listes de grande taille.

**Exemple de fonctionnement**

Liste initiale : [8, 3, 5, 2, 9, 1]

-	On la coupe en deux : [8, 3, 5] et [2, 9, 1]
-	On trie [8, 3, 5] en la recoupant en [8] et [3, 5] :
     -	[] est déjà trié
     -	[3, 5] → recoupé en [3] et [5] → puis fusion → [3, 5]
     -	fusion de [8] et [3, 5] → [3, 5, 8]
-	On trie [2, 9, 1] de même en la coupant en [2] et [9, 1] :
     -	[ 2] est déjà trié
     -	[9, 1] → recoupé en [9] et [1] → fusion → [1, 9]
     -	fusion de [2] et [1, 9] → [1, 2, 9]
-	On fusionne enfin [3, 5, 8] et [1, 2, 9] pour obtenir [1, 2, 3, 5, 8, 9].


Pour le code, on va écrire une fonction auxiliaire `fusionner(left, right)` qui prend en paramètre deux listes déjà triées et renvoie une liste fusionnée et triée.