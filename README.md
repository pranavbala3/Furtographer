# Furtographer
CSDS 393: Software Engineering Project

## Setup Locally

```
git clone https://github.com/pranavbala3/Furtographer.git
python3 -m venv venv
# activate venv
pip install -r requirements.txt
```

## Setup
To install Flask
```
pip install Flask
```

## Instructions
To run the web app
```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
The application will run locally on the URL http://127.0.0.1:5000/

## How to Run Database in Docker

1. Install [Docker Desktop] (https://www.docker.com/products/docker-desktop/)
1. Install `docker` and `docker-compose`
    ```
    $ brew install docker
    $ brew install docker-compose
    ```
1.  Open the Docker Desktop app to start Docker Engine

### Start the DB Container
1. Change directory to `database` folder.
1. Run the following command to start db. It will apply all SQL scripts under `sql` folder using the db migration tool "Flyway"
```
docker-compose --file docker-compose.yml up --detach
```

### Stop the DB Container
```
docker-compose --file docker-compose.yml down
```

### Create New SQL Scripts and Apply to DB
1. Create a new file in the sql subfolder `sql/data` or `sql/tables`.
1. Follow the file naming convention below for Flyway to install files.
    ```
    format: VYYYMMDD_HHmm__[file name].sql
    eg: V20231026_0302__create_table_users.sql
    ```
1. Run the following command if the docker containers are up.
    ```
    docker-compose run --rm furto_flyway migrate
    ```
1. Or, execute sql script(s) from a database management tool.

## For Training and Predicting

1. Download datasets:

    `make setup_training`

    Look at `train.ipynb` for example training.

2. Begin predicting with:

   `make predict IMG=*path*`
