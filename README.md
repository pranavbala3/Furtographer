# Furtographer
Designed and Developed for CSDS 393 @ CWRU
By: Benjamin Luo, Pranav Balabhadra, Timothy Cronin, Anthony Wang, Mia Yang
<p align="center">
    <img alt="Picutre of Website" src="https://github.com/pranavbala3/Furtographer/assets/115095351/637bf8bd-7a10-4c7b-bb36-a637d42ff0e5" width="700">
</p>
Furtographer is a Flask web app that allows users to login/register, take/upload photos of dogs, receive a dog breed classification, and store their captures in a personalized, interactable collection. It is designed to run on your local machine, and can be set up following the instructions below.

Status of known bugs can be found in the issues tab, and omissions will be discussed below (After Setup)

You can find the User Manual here:
![User Manual](./USER_MANUAL.md)

Thank you so much and we hope you enjoy it!

# Setup For Application

To set up the Furtographer app, please make sure you have at least Python *3.11* and the Docker application installed beforehand.

### Step 1: Clone the repository
```
git clone https://github.com/pranavbala3/Furtographer.git
cd Furtographer
```
### Step 2: Set up your Virtual Environment
```
python3 -m venv venv
```
**\*NIX:** `source env/bin/activate`

**Windows:**

In *cmd.exe:* `venv\Scripts\activate.bat`

In *powershell:* `venv\Scripts\Activate.ps1`

### Step 3: Install Requirements
```
pip install -r requirements.txt
```

### Step 4: Setup Database
1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. For Mac: Can Install `docker` and `docker-compose` below using Brew
    ```
    $ brew install docker
    $ brew install docker-compose
    ```
#### 3.  Open the Docker Desktop app to start Docker Engine

### Step 5: Start the DB Container
1. Change directory to `database` folder (cd database).
2. Run the following command to start db. It will apply all SQL scripts under `sql` folder using the db migration tool "Flyway"
If you have make:
```
make docker_up
```
otherwise
```
docker-compose --file docker-compose.yml up --detach
```

### Step 5.5: Stop the DataBase Container once done using the app (After step 6)
If you have make
```
make docker_down
```
otherwise
```
docker-compose --file docker-compose.yml down
```

### Step 6: Launch the app:
(make sure running from an app that has or can have access to your systems camera), then run the following command.
```
python app.py
```
In the console a link will appear to run this app that you can paste into your browser.

If you get errors relating to `psychodb2` try stop the container and restarting it.

(If coming from step 5, you might need to cd .. to get out of the database folder)
```
make docker_down
make docker_up
```

## Setup For Machine Learning Training

### Download datasets:

- If You Have ```make```: `make setup_training`
- Otherwise run
  - ```python -m model.scripts.get_datasets```
  - ```python -m model.scripts.get_bottleneck_features```

### Start jupyter notebook
  - Make sure that the jupyter executable you are running is the downloaded by pip install and not be another source, this could require you to stop your current virtual and restart it
    - **\*NIX:** Check executable location with ```which jupyter```
    - ***Windows:** Check executable location with ```which jupyter```
  - ```jupyter notebook```

### Look at `train.ipynb` for example training.

### Begin predicting with:

   `make predict IMG=*path*`

## Omissions and discussion of future developments
- Deploy Furtographer as a mobile application (Containerize, incorporate server-side deployment for ML model and database image storage)
- Add FAQs and help section for user guidance
- User’s ability to edit their profile information
- Increase criteria/customization to profile information
- Support functionality to enable Users to reset their password in case forgot password
- Support functionality to allow users to log in with emails (Gmail login support)
- Users can delete their account and remove their associated data from the Furtographer database permanently
- Privacy may need to be investigated
- Images/Furtos can contain additional metadata, including location
- Track images by location of captured image
- Different collection views (not just table, but map of images based on captured location)
- Interacting with other users (social media aspect)
