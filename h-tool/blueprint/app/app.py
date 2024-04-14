from flask import Flask,render_template,url_for,Blueprint,request,session
import sqlite3_db as db

app_bp = Blueprint("app",__name__,template_folder = "templates")

@app_bp.route("/")
#home page with login and singin buttons and some additional info
def index():
    db_name = db.DB_NAMES(db = "Development")
    with db.conn(db_name) as conn:
        db.create_tables(conn)
        add = db.user(conn,"add_user","omerkemal2019@gmail.com","DEVILO.K")
        login = db.user(conn,"login","ufuhihii8h6","yfiyihi9u")
        login_t = db.user(conn,"login","omerkemal2019@gmail.com","DEVILO.K")

    return f"<h1>user add = {add} login fail = {login} s = {login_t} </h1>"

@app_bp.route("/login",methods=["GET","POST"])
def login():
    return "login page"
@app_bp.route("/logout")
def logout():
    return "Logout route"
