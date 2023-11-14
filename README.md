# Furtographer
CSDS 393: Software Engineering Project

## Setup Locally

Requires Python *3.11* and the docker application.

### Clone
```
git clone https://github.com/pranavbala3/Furtographer.git
cd Furtographer
```
### Virtual Environment
```
python3 -m venv venv
```
**\*NIX:** `source env/bin/activate`

**Windows:**

In *cmd.exe:* `env\Scripts\activate.bat`

In *powershell:* `env\Scripts\Activate.ps1`

### Install Requirements
```
pip install -r requirements.txt
```

### Setup Database
1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Install `docker` and `docker-compose`
    ```
    $ brew install docker
    $ brew install docker-compose
    ```
3.  Open the Docker Desktop app to start Docker Engine

### Start the DB Container
1. Change directory to `database` folder.
2. Run the following command to start db. It will apply all SQL scripts under `sql` folder using the db migration tool "Flyway"
If you have make:
```
make docker_up
```
otherwise
```
docker-compose --file docker-compose.yml up --detach
```

### Stop the DB Container
If you have make
```
make docker_down
```
otherwise
```
docker-compose --file docker-compose.yml down
```

### To Run
(make sure running from an app that has or can have access to your systems camera)
```
python app.py
```

## For Training and Predicting

1. Download datasets:

- If You Have ```make```: `make setup_training`
- Otherwise run
  - ```python -m model.scripts.get_datasets```
  - ```python -m model.scripts.get_bottleneck_features```

2. Look at `train.ipynb` for example training.

3. Begin predicting with:

   `make predict IMG=*path*`
