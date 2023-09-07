"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'butterfingers'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """redirects to /users"""
    return redirect('/users')

@app.route('/users')
def list_users():
"""lists users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users-list.html', users=users)

@app.route('/users/new')
def users_new_form():
    """shows add user form"""
    return render_template('add-user.html')

@app.route('/users/new', methods=['POST'])
def users_new():
    """adds new user to db"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """shows user info"""
    user = User.query.get_or_404(user_id)
    return render_template('users-show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def user_edit_form(user_id):
    """shows a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods['POST'])
def user_update(user_id):
    """handles form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """handles form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")