from flask import Flask,session,url_for


app = Flask(__name__)
app.secret_key = "keep it secret,keep it safe"