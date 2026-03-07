
Durée : 1 heure

Sujet : Gestion d’une Concession Automobile

Contexte : Vous devez modéliser une concession automobile qui vend différents types de voitures. Les voitures peuvent être de types variés : électriques, thermiques, hybrides. Pour simplifier, on se concentrera sur des voitures générales (classe de base) et des voitures électriques (classe dérivée).

Objectifs :
- Créer une hiérarchie de classes modélisant des voitures et une concession.
- Gérer la liste des voitures disponibles en inventaire.
- Ajouter une méthode de vente simulant le retrait d’une voiture de l’inventaire.
- Présenter un exemple d’héritage entre classes (une sous-classe “Voiture Électrique” héritant de la classe “Voiture”).

## Classe Voiture

- Créer une classe Voiture avec les attributs suivants :
- marque (string)
- modele (string)
- prix (float ou int)
- kilometrage (int, par défaut 0)
- Dans le constructeur (__init__), initialiser ces attributs.
- Ajouter une méthode afficher_info() qui affiche les informations de la voiture sous une forme lisible, par exemple :

```
Marque: Tesla  
Modèle: Model 3  
Prix: 35000  
Kilométrage: 10000  
```


## Classe VoitureElectrique (héritage)

- Créer une classe VoitureElectrique qui hérite de Voiture.
- Ajouter un attribut autonomie (en km).
- Le constructeur prend en plus de marque, modele, prix, kilometrage, la valeur d’autonomie.
- Redéfinir (surcharger) la méthode afficher_info() pour qu’elle affiche également l’autonomie du véhicule :

```
Marque: Renault
Modèle: Zoe
Prix: 20000
Kilométrage: 5000
Autonomie: 300 km
```

## Classe Concession

- Créer une classe Concession avec un attribut nom (string) et un attribut inventaire (liste de voitures, vide au départ).
- Le constructeur initialise le nom et l’inventaire (une liste vide).
- Ajouter une méthode ajouter_voiture(voiture) qui prend en paramètre un objet de type Voiture (ou VoitureElectrique) et l’ajoute à l’inventaire.
- Ajouter une méthode afficher_inventaire() qui affiche la liste des voitures disponibles, en appelant afficher_info() sur chacune.
- Ajouter une méthode vendre_voiture(marque, modele) qui :
	- Recherche dans l’inventaire une voiture correspondant à la marque et au modele.
	- Si trouvée, la retire de l’inventaire et affiche un message de vente du type : `La voiture Peugeot 308 a été vendue.`
	- Si aucune voiture ne correspond, afficher un message indiquant que la voiture n’a pas été trouvée.

- Créer une méthode qui calcule le prix total de toutes les voitures en inventaire et le prix moyen.
- Surcharger la méthode `__str__` pour afficher le nom de la concession et le nombre de voitures en inventaire.


## Tests

- Créer une instance de Concession (par exemple Concession("Concession du Centre")).
- Créer au moins 3 instances de Voiture et VoitureElectrique, avec des valeurs variées.
- Ajouter toutes ces voitures à la concession.
- Afficher l’inventaire complet.
- Tenter de vendre une voiture existante et une voiture inexistante, vérifier que le message affiché est correct.
- Utiliser la méthode print sur l’instance de Concession pour afficher le nom et le nombre de voitures en inventaire.
- Afficher le prix total et le prix moyen des voitures en inventaire.

## Question conceptuelle

- Expliquez en quelques lignes l’intérêt de l’héritage en POO. Pourquoi créer une classe VoitureElectrique héritant de Voiture plutôt que de tout réécrire dans une classe indépendante ?
