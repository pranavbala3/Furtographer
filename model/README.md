# Instructions for Setup

1. **Recommended:** Create environment: `python3 -m venv env`

2. Start environment:

   **\*NIX:** `source env/bin/activate`

   **Windows:**

       In *cmd.exe:* `env\Scripts\activate.bat`

       In *powershell:* `env\Scripts\Activate.ps1`

3. Install requirements: *pip install -r requirements.txt*

## For Web Application

4. Run `flask run`

## For Training and Predicting

4. Download datasets:

   If you have *make*: `make setup_training`

5. Begin predicting with:

   `make predict IMG=*path*`
