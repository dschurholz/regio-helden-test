# Regio Helden Test

This repository contains a django test project with the following characteristics:

 - Admin users can manage CRUD Users, who will be called customers.
 - Customers have a First Name, Last Name and IBAN (standarized bank account number).
 - Admins of the app should authenticate using a Google account.
 - Admins should be able to create, read, update and delete customers.
 - Admins can only manipulate customers they created.

## Installing Regio Helden Test

Some requirements before installing regio-helden-test:

Install Postgresql and create database regioheldentest

To Install regio-helden-test we need to create a virtualenv:

if we have not installed virtualenv:

    $ sudo apt-get install python-virtualenv

then we need to run (note that we are using python 3):

    $ virtualenv regio-helden-test -p /usr/bin/python3
    $ cd regio-helden-test

and we are ready to clone the repo:

    $ git clone git@github.com:dschurholz/regio-helden-test.git
    $ cd regio-helden-test

Once on regio-helden-test directory, we need to run

    $ source ../bin/activate

or if we have on regio-helden-test directory

    $ source bin/activate

and to install all the project's dependencies:

    $ pip install -r requirements.txt

Before starting to run the project, we need to set up the settings, execute:

    $ cd regio-helden-test/RegioHeldenTest
    $ cp local_settings.py.example local_settings.py

and change database default settings to your settings in the local_settings.py file.

Then you are ready to run

    $ ./manage.py migrate
    $ ./manage.py runserver

to test you can got to [http://localhost:8000/admin](http://localhost:8000/admin)

## Testing

To run the test suite, please use the following command, from the project root directory:

    $ ./manage.py test --settings=RegioHeldenTest.test_settings 
