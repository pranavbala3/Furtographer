# Instructions for Setup

1. **Recommended:** Create environment: `python3 -m venv env`

2. Start environment:

   **\*NIX:** `source env/bin/activte`

   **Windows:**

       In *cmd.exe:* `env\Scripts\activate.bat`

       In *powershell:* `env\Scripts\Activate.ps1`

3. Install requirements: *pip install -r requirements.txt*
4. Download datasets:

   If you have *make*: `make setup`

   Or run: `python get_datesets.py` and `python get_bottleneck_features.py`

5. Begin predicting with:

   `make predict IMG=*path*` or

   `python model.py *path*`

6. Begin training with

   `make train` or

   `python nets/train.py`
