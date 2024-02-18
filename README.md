Gadget-Marketplace
Backend for online store. 

Technologies and requirements:
Python
Drf
Django
PosrtgeSQL
Celery
RestAPI
JWT-token

Author:
Ade(I did it on my own, bruh)

How to use:

Clone this repository to your local folder
git clone git@github.com:kimazatot/hackaton-2.git

Create a virtual environment
python3 -m env

Activate a virtual environment
. env/bin/activate

Install requirements from a file
pip3 install -r requirements.txt

Create an .env file and write all neccessary information in it
touch .env

Make all neccessary migrations
python3 manage.py migrate

And run your project!
python3 manage.py runserver