Ignorer et passer au contenu
Vous avez dit :
voici mon readme est ce que tu peux le rendre plus jolie ? 
# Lancer l'environement virtuel 
- Bureau/Analyse_de_Sentiment/ticketSentiments
- source ticketSentiments/bin/activate

# Lancer l'app
- /home/shaney/Bureau/Analyse_de_Sentiment/ticketSentiments/bin/python /home/shaney/Bureau/Analyse_de_Sentiment/webApp_Tickets/run.py

### dans le dossier
- python3 run.py
- http://127.0.0.1:5000

### Docker
- cd webApp_Tickets
- sudo docker-compose up -d
- sudo docker-compose stop


# commands

docker --version

sudo apt install docker.io -y

systemctl status docker

sudo systemctl start docker

## mail :

<br>n0xsha@outlook.fr

<br>bONZAI666
==============================

# lancement :

docker-compose down
docker-compose up --build -d
==============================

# rebuild :

sudo docker-compose down

sudo docker-compose build --no-cache

sudo docker-compose up -d

# logs

sudo docker-compose logs



==============================

docker exec -it flask_app flask db init

docker exec -it flask_app flask db migrate -m "initial migration"

docker exec -it flask_app flask db upgrade

# rentrer dans le conteneur :
## - pour l'app :
sudo docker exec -it flask_app bash
## - pour la base de donnée :
sudo docker exec -it flask_mysql bash

# install mysql
apt update && apt install -y default-mysql-client
mysql -u user -p -h db



ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'root';
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
FLUSH PRIVILEGES;

docker exec -it flask_app bash
flask db migrate -m "final fix for plugin"
flask db upgrade
ChatGPT a dit :
Voici une version plus claire et joliment formatée de ton README, avec des titres et sections bien distinctes pour améliorer la lisibilité.

# Guide de Lancement de l'Application

## 1. Lancer l'Environnement Virtuel

### Sur votre machine locale :
1. Rendez-vous dans le répertoire du projet :
cd Bureau/Analyse_de_Sentiment/ticketSentiments

2. Activez l'environnement virtuel :
source ticketSentiments/bin/activate


## 2. Lancer l'Application

### Méthode 1 : Exécution directe
1. Utilisez Python pour lancer l'application :
/home/shaney/Bureau/Analyse_de_Sentiment/ticketSentiments/bin/python /home/shaney/Bureau/Analyse_de_Sentiment/webApp_Tickets/run.py


2. Accédez à l'application via le navigateur :
http://127.0.0.1:5000


### Méthode 2 : Lancer avec Python3
1. Dans le dossier contenant `run.py`, lancez l'application :
python3 run.py


## 3. Utiliser Docker pour Lancer l'App

### Démarrer les services Docker
1. Allez dans le dossier du projet `webApp_Tickets` :
cd webApp_Tickets


2. Démarrez les services en arrière-plan avec Docker Compose :
sudo docker-compose up -d


### Arrêter les services Docker
1. Pour arrêter les services :
sudo docker-compose stop


## 4. Commandes Docker Utiles

### Vérifier la version de Docker
docker --version


### Installer Docker
sudo apt install docker.io -y


### Vérifier l'état de Docker
systemctl status docker


### Démarrer Docker
sudo systemctl start docker


### Arrêter Docker
docker-compose down


### Rebuild de l'application
1. Arrêter et supprimer les conteneurs existants :
sudo docker-compose down


2. Reconstruire les services sans cache :
sudo docker-compose build --no-cache


3. Démarrer les services en arrière-plan après le rebuild :
sudo docker-compose up -d


### Consulter les logs
sudo docker-compose logs


## 5. Gestion de la Base de Données avec Docker

### Initialiser la base de données
docker exec -it flask_app flask db init


### Appliquer les migrations de base de données
docker exec -it flask_app flask db migrate -m "initial migration" docker exec -it flask_app flask db upgrade


### Accéder au Conteneur Docker
- Pour entrer dans le conteneur de l'application :
sudo docker exec -it flask_app bash


- Pour entrer dans le conteneur de la base de données MySQL :
sudo docker exec -it flask_mysql bash


## 6. Installation et Configuration de MySQL

### Installer le client MySQL
apt update && apt install -y default-mysql-client


### Se connecter à la base de données MySQL
mysql -u user -p -h db


### Configurer MySQL pour utiliser le mot de passe natif
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'root'; ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'; FLUSH PRIVILEGES;


### Migrations de la base de données dans le conteneur
docker exec -it flask_app bash flask db migrate -m "final fix for plugin" flask db upgrade


## 7. Informations de Contact

Si vous avez des questions ou avez besoin d'assistance, contactez-nous à l'adresse suivante :

- **Email** : n0xsha@outlook.fr
- **Mot de passe (si nécessaire)** : bONZAI666