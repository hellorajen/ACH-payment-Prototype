@echo off
REM Contents of Create_Django_project_and_app.bat
python -m venv venv
call venv\Scripts\activate
pip install django
django-admin startproject ach_project