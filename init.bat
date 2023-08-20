@echo off

C:\User\Escritorio\calculadora_de_costos_v1.2\venv\Scripts\activate
cd C:\User\Escritorio\calculadora_de_costos_v1.2\calculadora_de_costos

py manage.py runserver

npx electron .

pause
