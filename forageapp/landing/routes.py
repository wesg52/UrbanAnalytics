from flask import Blueprint, flash, redirect, render_template, request

landing = Blueprint('landing', __name__)


@landing.route("/")
def home():
    return render_template('landing.html')

@landing.route("/about")
def about():
    return render_template('about.html', title='About')
