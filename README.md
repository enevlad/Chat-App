# Chat-App

- **Authors: Ene Vlad-Mihnea, Dorneanu Stefan, Alexadrescu Andrei**

## app.py

- Handles most of the backend of the app (login, sign up)
- Stores the messages using SQLAlchemy library

## templates

- Holds the htmls (chat.html, login.html, register.html)
- chat.html represents the main page of the web application which displays the chat text between all the participants in the session
- login.html requests a username and a password for loging in
- register.html is the sign up page of the web app. It requests a username and a password which is then saved using sql in app.py
