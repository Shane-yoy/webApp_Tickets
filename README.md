
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

# Tests

docker exec -it flask_app pytest