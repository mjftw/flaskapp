# Readme

Flask based simple web app for viewing the status of and controlling embedded devices, connected using the code in the [flask_node project](https://github.com/mjftw/flask_node).
UI is based on bootstrap, and the tool uses AJAX to sent and receive data from the control nodes.
This app was created while learning Flask.


## Setup
To install the required packaged run:
```console
$ pip3 install -r requirements.txt
```

To run the flask server simply run:
```console
$ ./run
```

It is recommended that you create a secret key, and store it in a file called *secrets.txt*, in this directory.

## Database modifications

The project uses an Alembic database migration repository in order to manage chages to the database structure.

First the database migration repositroy must be initilised:
```console
$ ./run db init
```

Any changes made to the database models can be automatically converted to a migration:
```console
$ ./run db migrate
```

A migration can be applied to the database with:
```console
$ ./run db upgrade
```

## References
To create this project, I am following Miguel Grenberg's Flask [tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).
