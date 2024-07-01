# P10 Créez une API sécurisée RESTful en utilisant Django REST #

## Création d'une API sécurisée pour le se suivi de Projets/Problèmes/Commentaires##
Projet réalisé dans le cadre du parcours OpenClassrooms Développeur d'application Python

## Prérequis ##
 - IDE(VSCode,Pycharm...)
 - Python disponible sur https://www.python.org/

## Installation sous Windows ##
- Clonez ce repository  
`` git clone https://github.com/Laysi88/P10 ``
- Créez un environnement virtuel dans le dossier source du projet  
``python -m venv env``

- Activez votre environnement virtuel en exécutant la commande Powershell:  
`` .\env\Scripts\Activate.ps1``

- Installez les dépendances  
`` pip install -r requiremnts.txt``

## Lancement

- Effectuez les migrations   
``python manage.py migrate``
- Démarez l'API  
``python manage.py runserver``