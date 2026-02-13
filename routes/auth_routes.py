from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import users
from datetime import datetime

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = users.find_one({"email": request.form["email"]})
        if user and check_password_hash(user["password"], request.form["password"]):
            session["email"] = user["email"]
            session["role"] = user["role"]
            return redirect("/admin/dashboard" if user["role"] == "admin" else "/client/dashboard")
        return "Invalid credentials"
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if users.find_one({"email": request.form["email"]}):
            return "User already exists"

        users.insert_one({
            "name": request.form["name"],
            "email": request.form["email"],
            "password": generate_password_hash(request.form["password"]),
            "role": "client",
            "wallet": 0.0,
            "created_at": datetime.now().strftime("%Y-%m-%d")
        })
        return redirect("/")
    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
