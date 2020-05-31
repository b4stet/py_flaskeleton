# py_flaskeleton

A skeleton for an API using Flask factory.  
It follows the MVC pattern without any decorator.  
This example also illustrates usage of PostgreSQL without ORM.

## Requirements
- postgresql
- python3-psycopg2 (from PostgreSQL repository)
- python3-flask
- python3-pycryptodome
- python3-scrypt

## Project structure
### General
```
.
├── src/
├── bin/
├── cli.py
├── config.template.yml
├── migration/
└── web.py
```

- `src/` is the application itself, structure is detailed in next section
- `bin/` contains bash wrappers to run CLI and API
- `migration/` contains db schemas in raw SQL format
- `cli.py` and `web.py` instantiate the application accordingly
- `config.template.yml` must be copied somewhere as `config.yml` and will contain app/db/logger parameters

By default, bash wrappers assume `config.yml` being at the root of the project.  
This can be changed by specifying/exporting the environment variable `FLASKLELETON_CONFIG` before the command.


### The application
```
src/
├── action
├── bo
├── cli
├── converter
├── crypto
├── entity
├── include
├── __init__.py
├── middleware
├── service
├── table
├── template
└── validator

```

| Path                | Purpose                                                                                              |
|:-------------------:|:-----------------------------------------------------------------------------------------------------|
| `__init__.py`       | app bootstrap: inject dependencies, register services/routes/cli                                     |
| `include/`          | define app components: API routing, CLI commands, services to build the application                  |
| `middleware/`       | implement pre-processing applied automatically on requests before controllers (eg. authorization)    |
| `action/`           | implement controllers as defined in `routing.py`. usually validate inputs then delegate to bo        |
| `cli/`              | implement commands as defined in `clis.py`                                                           |
| `bo/`               | implement the logic to process requests and prepare the response                                     |
| `table/`            | implement database operations                                                                        |
| `entity/`           | map database tables as object                                                                        |
| `template/`         | encapsulate common formatting like responses                                                         |
| `service/`          | implement global services (DB connector, logger, error handler, depency injection)                   |
| `crypto/`           | centralize encryption and hashing needs                                                              |
| `validator/`        | centralize user inputs validation                                                                    |
| `converter/`        | centralize needs for type conversion (eg. datetime)                                                  |



## Local run
### DB creation
- create db and user, and complete `config.yml` accordingly.
```
$ sudo -u postgres createuser -h localhost -p 5432 --pwprompt my_user
$ sudo -u postgres createdb -h localhost -p 5432 -O my_user --encoding='utf-8' my_db 
```

- create db schema. From root:
```
$ bash bin/cli.sh dev db_migration init
$ bash bin/cli.sh dev db_migration check
$ bash bin/cli.sh dev db_migration apply
```

### Run application
From project root:
- for API: `bash bin/web.sh dev`
- for CLI: `bash bin/cli.sh dev --help`

### Run tests
From root:
```
$ python3 -m unittest discover
```
