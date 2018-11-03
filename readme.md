# Readme

A simple web app, for the purposes of getting to grips with Flask.

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
