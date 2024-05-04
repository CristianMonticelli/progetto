from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


FILE_PATH = "registered_users.json" 
try:
    with open(FILE_PATH, 'r') as file:
        registered_users = json.load(file)
except FileNotFoundError:
    registered_users = {"utente": {}, "istruttore": {}}


registered_users["utente"]['pippo']= 2
file_json = "registrazioni.json"
with open(file_json, "w") as f:
    json.dump(registered_users, f)
f.close()