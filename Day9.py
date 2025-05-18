from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os

def hashed_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Day_9.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname('instance'))

db = SQLAlchemy(app)


class Hello(db.Model):
    __tablename__="user"
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    hashed_pass = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f"{self.sno} - {self.username}"


def register():
    username=input("Enter the username: ")
    password=input("Enter the password: ")
    hashed=hashed_pass(password)

    with app.app_context():
        if db.session.query(Hello).filter_by(username=username).first():
            print("This Username is already taken.")
            return

        new_user=Hello(username=username,hashed_pass=hashed)

        db.session.add(new_user)
        db.session.commit()
        print("Registration is successful.")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print(f"Database created at: {os.path.join(basedir, 'Day_9.db')}")  # This will create the database tables
    register()
    app.run(debug=True)
    
    
