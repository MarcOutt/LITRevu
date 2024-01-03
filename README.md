![image](https://github.com/MarcOutt/OC_p10/assets/112987151/2a0b87b9-46d3-4135-a890-e8b52cd4c8ee)
![image](https://github.com/MarcOutt/OC_p10/assets/112987151/ddc0679e-fabc-4655-804b-351da4c3433c)
![image](https://github.com/MarcOutt/OC_p12/assets/112987151/c4f736d8-40a8-460f-a86f-886034772ce4)

# LITRevu - Application Web pour Critiques de Livres et d'Articles

## Table des matières
- [Introduction](#introduction)
- [Cahier des charges](#cahier-des-charges)
- [Installation](#installation)
- [Technologie](#technologie)
- [Utilisation](#utilisation)
- [Rapport Flake8](#rapport-flake8)
- [Wireframes](#wireframes)

## Introduction

Ce projet consiste à créer un site web pour la société LITReview. Le but de l'application web est de permettre aux utilisateurs de demander et de publier des critiques de livres ou d'articles. L'application présente deux cas d'utilisation principaux :

1. Les personnes qui demandent des critiques sur un livre ou sur un article particulier.
2. Les personnes qui recherchent des articles et des livres intéressants à lire, en se basant sur les critiques des autres.

## Cahier des charges :

L'objectif de l'application LITRevu est de permettre aux utilisateurs de demander et de publier des critiques de livres ou d'articles. Voici les fonctionnalités principales attendues :

Un utilisateur devra pouvoir : 
* se connecter et s’inscrire – le site ne doit pas être accessible à un utilisateur non connecté ;
* consulter un flux contenant les derniers tickets et les commentaires des utilisateurs qu'il suit, classés par ordre chronologique, les plus récents en premier ; 
* créer de nouveaux tickets pour demander une critique sur un livre/article ;
* créer des critiques en réponse à des tickets ;
* créer des critiques qui ne sont pas en réponse à un ticket. Dans le cadre d'un processus en une étape, l'utilisateur créera un ticket puis un commentaire en réponse à son propre ticket ;
* voir, modifier et supprimer ses propres tickets et commentaires ; 
* suivre les autres utilisateurs en entrant leur nom d'utilisateur ;
* voir qui il suit et suivre qui il veut ;
* cesser de suivre un utilisateur.

Un développeur devra pouvoir :
* créer un environnement local en utilisant venv, et gérer le site en se basant sur la documentation détaillée présentée dans le fichier README.md.

Le site devra :
* avoir une interface utilisateur correspondant à celle des wireframes ;
* avoir une interface utilisateur propre et minimale.

## Installation
------------------

* Télécharger python 3.7 (https://www.python.org/downloads/)
* Installer python 3 
* Sous Window:
    Ouvrir l'invite de commande : ``` touche windows + r``` et entrez ```cmd```
* Sous MacOs:
    Ouvrir l'invite de commande : ```touche command + espace``` et entrez ```terminal```
* Sous Linux:
    Ouvrir l'invite de commande : ```Ctrl + Alt + T```
* Mettre pip en version 21.3.1
```bash
python -m pip install --upgrade pip 21.3.1
```

* Il est préférable d'utiliser un environnement virtuel, pour l'installer:  
```bash
pip install venv
```

* Créer un dossier au nom de l'application avec mkdir
```bash
mkdir/LITReview
```

* Aller dans le dossier crée:
```bash
cd/LITReview
```

**LINUX MACOS**
* Créer votre environnement virtuel:
```bash
python3.xx -m venv .env
```
* Sourcer l'environnement virtuel:
```bash
source env/bin/activate
```

* Installer la configuration à l'aide du fichier requirements.txt:
```bash
pip install -r requirement.txt
```
**WINDOWS**
* Créer votre environnement virtuel:
```bash
python -m venv env
```
* Sourcer cette environnement virtuel:  
```bash
source env/Scripts/activate
```
* Installer la configuration à l'aide du fichier requirements.txt:
```bash
pip install -r requirement.txt
```
* Télécharger les fichiers et les dossier du repository.
* Ajouter les dans le dossier LITReview

## Technologie

- **Framework :** Django
- **Base de données :** SQLite (fichier db.sqlite3 inclus)
- **Langage :** Python 3.7
- **Front-end :** HTML, CSS, JavaScript

## Utilisation 

* Naviguer dans le dossier LITReview et entrez la commande suivante dans le terminal pour lance le serveur :
```bash
python manage.py runserver
```
* Entrer l'adresse suivante dans votre navigateur pour accéder au site : http:/127.0.0.1:8000/


Afin de tester les différentes fonctionalités du site, 3 comptes utilisateurs ont été créés : "Jean", "Severine" et "Sarah".  
Le mot de passe est identique pour les 3 : hello1234  

Pour accéder à l'interface d'administration::
* Aller sur http:/127.0.0.1:8000/admin
* Nom du compte: admin
* Mot de passe: admin

## RAPPORT FLAKE8
-------------------
* Ouvrir l'invite de commande ( se reporter à la rubrique installation)
* Lancer votre environnement virtuel ( se reporter à la rubrique installation)
* Rentrer le code suivant:
```bash
flake8 --exclude=.env/ --max-line-length=119 --format=html --htmldir=flake8-rapport
``` 
* Aller dans le dossier flake8-rapport
* Ouvrir le fichier index




