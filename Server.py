from flask import Flask, redirect, request, url_for, render_template, Response
from userDatabase import user_existence, add_user_to_database, user_authenticate, get_all_user_posts, add_posts_to_user, edit_posts_to_user
from mongoengine import *
import json

app = Flask(__name__)


@app.route("/")
def home_page():
    return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        """ Handle the request data and populate the json file """
        clean_user_data = request.form
        status = user_existence(clean_user_data['user_name'])
        if request.form["submitType"] == "register":
            if status:
                thrown_error = clean_user_data["user_name"] + " already exists in database, please choose another name"
                ret_response = Response(response=thrown_error, status=302)
                return ret_response
            else:
                add_user_to_database(clean_user_data)
                print "%s has been added to the Database" % clean_user_data["user_name"]
        else:
            if status:
                status = user_authenticate(user_data=clean_user_data)
                if not status:
                    thrown_error = "In-correct password please retry"
                    ret_response = Response(response=thrown_error, status=302)
                    return ret_response
                else:
                    print "User Authenticated"
            else:
                thrown_error = clean_user_data["user_name"] + " is not present in the Database"
                ret_response = Response(response=thrown_error, status=302)
                return ret_response
        return Response(response="Success", status=200)
    if request.method == "GET":
        """ Renders the Login Page """
        return render_template('login.html')


@app.route("/user/<user_name>", methods=["GET"])
def posts_page(user_name):
    if request.method == "GET":
        return render_template('post.html')


@app.route("/user/<user_name>/posts", methods=["POST", "GET"])
def posts_grid(user_name):
    if request.method == "POST":
        """ Handle the add/delete/update/task for a particular task"""
        if request.form["task_status"] == "new":
            new_post_json = add_posts_to_user(user_name, request.form)
        else:
            new_post_json = edit_posts_to_user(user_name, request.form)
        return new_post_json
    if request.method == "GET":
        """ Get all the tasks related to particular user """
        print "Request to get all posts related to the user"
        json_output = get_all_user_posts(user_name)
        return json_output


if __name__ == "__main__":
    my_db = connect('todoapp-database')
    app.debug = True
    app.Thread = True
    app.run('localhost', 8080)