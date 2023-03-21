from flask import Flask, render_template,request,redirect,session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.entry import Entry
from flask import flash

@app.route("/home")
def home():
    if "user_id" not in session:
        flash(" You must be logged in to access the home page.")
        return redirect ("/")
    total_calories = Entry.total_calories(session["user_id"])
    user = User.get_by_id(session["user_id"])
    user_obj = Entry.get_all(session["user_id"])
    # print(user_obj.entid)

    return render_template("home.html", user=user, user_obj=user_obj,total_calories = total_calories)

@app.route("/inputs/<int:entry_id>")
def entry_detail(entry_id):
    user = User.get_by_id(session["user_id"])
    entry = Entry.get_by_id(entry_id)
    print (entry)
    return render_template("details.html",user=user, entry=entry)

@app.route("/inputs/create")
def entry_create():
    return render_template("create.html")

@app.route("/inputs/edit/<int:entry_id>")
def entry_edit(entry_id):
    entry = Entry.get_by_id(entry_id)
    return render_template("edit.html", entry = entry)

@app.route("/inputs", methods=["POST"])
def create_entry():
    valid_entry = Entry.create_valid_entry(request.form)
    if valid_entry:
        return redirect('/home')
    return redirect("/inputs/create")

@app.route("/inputs/<int:entry_id>", methods=["POST"])
def update_entry(entry_id):
    valid_entry = Entry.update_entry(request.form)
    if not valid_entry:
        return redirect(f'/inputs/{entry_id}')
    return redirect('/home')

@app.route("/inputs/delete/<int:entry_id>")
def delete_by_id(entry_id):
    Entry.delete_by_id(entry_id)
    return redirect("/home")

