
Durée : 1 heure

Sujet : Les décorateurs en Python sont un moyen pratique de modifier le comportement d’une fonction sans en altérer le code source directement. Ils sont utiles pour la journalisation, la validation, le contrôle d’accès, etc.

## Décorateur de Journalisation Simple

- Écrire un décorateur @journaliser qui, appliqué à une fonction, affiche :
	- Le nom de la fonction appelée
	- Les arguments positionnels et nommés passés à cette fonction
	- La fonction décorée doit ensuite s’exécuter normalement et retourner son résultat.

Exemple d’utilisation :

```python
@journaliser
def addition(a, b):
    return a + b
```

Appeler `addition(3, 5)` devrait afficher quelque chose comme :

`Appel de addition(3, 5)`

Et retourner 8.

## Décorateur de Mémorisation (Caching)

   - Écrire un décorateur @memoriser qui stocke les résultats de la fonction décorée en fonction de ses arguments.
   - Si la fonction est appelée à nouveau avec les mêmes arguments, retourner directement le résultat mémorisé au lieu de recalculer.
   - Tester ce décorateur sur une fonction de calcul un peu coûteuse (par exemple, une fonction qui calcule le n-ième nombre de Fibonacci de manière récursive).

# Combinaison de décorateurs

Appliquer les deux décorateurs @journaliser et @memoriser à la même fonction pour observer l’ordre d’exécution (décorer la fonction avec @journaliser puis @memoriser, ou l’inverse, et commenter le comportement).
