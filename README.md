# hackaton-2


#@ gadget-marketplace backend


### Technologies and requirements:
Python 
Django 
DRF 
Celery 
PostgreSQL 
Redis

### Author
Ade, unfortunately i was alone

### How to use:
#### Clone this repository to your local folder
git clone git@github.com:kimazatot/hackaton-2.git

#### Create a virtual environment
python3 -m venv

#### Activate a virtual environment
. /bin/activate

#### Install requirements from a file
pip3 install -r requirements.txt

#### Create an .env file and write all neccessary information in it
touch .env

#### Make all neccessary migrations
python3 manage.py migrate

And run your project!
python3 manage.py runserver

