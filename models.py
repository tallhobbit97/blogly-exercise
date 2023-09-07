"""Models for Blogly."""
from  flask_sqlalchemy import SQLalchemy

db = SQLalchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable False)
    last_name = db.Column(db.String(20), nullable False)
    profile_url = db.Column(db.String, nullable=False, default=DEFAULT_IMAGE_URL)
    
    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

def connect_db(app):
    """Connect app to database"""
    db.app = app
    db.init_app(app)