from flask import Blueprint, request, redirect
from models.plan_model import create_plan

plan_bp = Blueprint("plans", __name__)

@plan_bp.route("/create-plan", methods=["POST"])
def create_new_plan():
    create_plan(
        request.form["name"],
        int(request.form["price"]),
        int(request.form["cycle"])
    )
    return redirect("/dashboard")
