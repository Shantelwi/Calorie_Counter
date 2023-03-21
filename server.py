from flask_app import app
from flask_app.controllers import entries, users
from flask import Flask,request,redirect,session,render_template,url_for

if __name__ == "__main__":
    app.run(debug=True)