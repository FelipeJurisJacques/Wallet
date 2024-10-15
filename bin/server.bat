@echo off

cd ..\

call .\virtualized\Scripts\activate.bat

python manage.py runserver

cmd /k
