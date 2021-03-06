import ipdb
from flask import Flask, render_template, redirect, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import datetime

app = Flask(__name__)
app.config.from_object("punchstarter.default_settings")
manager = Manager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

from punchstarter.models import *

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/projects/create", methods=["GET","POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        #Form submission

        now = datetime.datetime.now()

        time_end = request.form.get("funding_end_date")
        time_end = datetime.datetime.strptime(time_end, "%Y-%m-%d")
        
        new_project = Project(
            member_id = 1,
        	name = request.form.get("project_name"),
        	short_description =request.form.get("short_description"),
        	long_description = request.form.get("long_description"),
        	goal_amount = request.form.get("goal_amount"),
        	time_start = now,
        	time_end = time_end,
        	time_created = now
        )

        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for("create"))
