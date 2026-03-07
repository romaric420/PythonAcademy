
Durée : 1 heure


Sujet : Les générateurs en Python permettent de créer des itérateurs en écrivant des fonctions utilisant le mot-clé `yield`. Ils offrent un moyen efficace de produire des séquences sans charger toute la liste en mémoire.


## 1. Générateur de suite simple
- Écrire une fonction générateur compter(start, end) qui produit tous les entiers de start à end inclus.
- Tester en itérant dessus et en affichant les valeurs produites.

## 2. Générateur filtrant
- Écrire un générateur nombres_pairs(iterable) qui prend un itérable de nombres et ne yield que les nombres pairs.
- Tester ce générateur avec une liste de nombres de 1 à 10 et afficher uniquement les pairs.

## 3. Générateur infini avec pause
- Écrire un générateur `fibonacci()` qui produit la suite de Fibonacci sans fin `(0, 1, 1, 2, 3, 5, 8, …)`.
- Dans le code principal, afficher les 10 premiers termes puis arrêter l’itération (avec une boucle `for` par exemple)

## 4. Générateur de puissances
- Écrire une fonction `générateur_puissance(n)` qui prend un entier n et produit les puissances de 2 jusqu’à n.
- Tester ce générateur avec `n=10` et afficher les valeurs produites.

## 5. Utiliser next() pour afficher les lignes d'un texte une par une
- Écrire une fonction qui lit les lignes d'un texte et les affiche une par une avec un iterateur. Les lignes doivent apparaitre à chaque appel de `next`.


Le texte : 
```python
"""
Il faut, autant qu'on peut, obliger tout le monde :
On a souvent besoin d'un plus petit que soi.
De cette vérité deux fables feront foi,
Tant la chose en preuves abonde.
Entre les pattes d'un Lion,
Un Rat sortit de terre assez à l'étourdie.
Le Roi des animaux, en cette occasion,
Montra ce qu'il était, et lui donna la vie.
Ce bienfait ne fut pas perdu.
Quelqu'un aurait-il jamais cru
Qu'un Lion d'un Rat eût affaire (1)?
Cependant il avint(2)qu'au sortir des forêts
Ce Lion fut pris dans des rets (3),
Dont ses rugissements ne le purent défaire.
Sire Rat accourut, et fit tant par ses dents
Qu'une maille rongée emporta tout l'ouvrage.
Patience et longueur de temps
Font plus que force ni que rage.
"""
```