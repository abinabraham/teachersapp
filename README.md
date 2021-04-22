#Teachers Directory Application

## Setup
The first thing to do is to clone the repository:

$ git clone https://github.com/abinabraham/teachersapp.git
$ cd teachersapp
Create a virtual environment to install dependencies in and activate it:

$ virtualenv2 --no-site-packages env
$ source env/bin/activate
Then install the dependencies:

(env)$ pip install -r requirements.txt
Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv2.

Once pip has finished downloading the dependencies:

(env)$ cd teachersapp
(env)$ python manage.py runserver
And navigate to http://127.0.0.1:8000/

There you can see, there are unapplied migrations

Create new env file using command
(env)$ cp .env.example .env

And add db details, Debug status and secret key

Run the command to migrate all the tables
(env)$ python manage.py migrate

You can create a superuser by command
(env)$ python manage.py createsuperuser --username="<>" --email="<>"
then need to set password also

And navigate to http://127.0.0.1:8000/
And login with those credentials

You will redirect to Home page as TEACHERS LIST

There you can create Subjects and Teachers one by one
While click on add button will redirect to corresponding modal form
And validations are added

Second menu will be the Subjects list of created

Third menu will be importer
where we can import CSV bulk create of teachers
