cd ..\

python -m venv virtualized

call .\virtualized\Scripts\activate.bat

pip install -r .\bin\requirements.txt

copy /y .\bin\fix\forecaster.py virtualized\Lib\site-packages\prophet\

deactivate
