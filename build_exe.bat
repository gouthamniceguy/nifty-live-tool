@echo off
REM Local build helper - run from repo root in cmd.exe
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller==5.11.0
pyinstaller --noconfirm --onefile --add-data "smartapi_client.py;." app.py
echo Done. exe is in dist\.
pause