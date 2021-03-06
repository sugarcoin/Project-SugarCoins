"""Models and database functions for SugarCoins project."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import (
    create_database,
    database_exists,
)

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions


class User(db.Model):
    """User of SugarCoin website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.String(64), nullable=True)
    gender_code = db.Column(db.String(1), db.ForeignKey('gender.gender_code'))

    gender = db.relationship("Gender", backref="user")
    weight = db.relationship("Weight", backref="user")
    glucose = db.relationship("Glucose", backref="user")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} name = {self.name} password = {self.password} gender = {self.gender_code} email = {self.email} phone = {self.phone}>"


class Gender(db.Model):
    """Table to hold user gender."""

    __tablename__ = "gender"

    gender_code = db.Column(db.String(1), nullable=False, primary_key=True)
    allowance = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Gender gender_code={self.gender_code} allowance={self.allowance}>"


class Weight(db.Model):
    """Table to hold user weight."""

    __tablename__ = "weight"

    weight_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) # one user to one weight at a time
    current_weight = db.Column(db.Integer, nullable=True)
    date_time = db.Column(db.DateTime)

    #user = db.relationship("User", backref="weight")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Weight weight_id={self.weight_id} current_weight={self.current_weight} date_time={self.date_time}>"

class Glucose(db.Model):
    """Table to hold user blood-glucose level."""

    __tablename__ = "glucose"

    glucose_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    current_glucose = db.Column(db.Integer, nullable=True)
    date_time = db.Column(db.DateTime)

    #user = db.relationship("User", backref="glucose")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Glucose glucose_id={self.glucose_id} current_glucose={self.current_glucose} date_time={self.date_time}>"

class Food(db.Model):
    """Table to track food intake."""

    __tablename__ = "food"

    food_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    food_name = db.Column(db.String(64), nullable=True)
    cost = db.Column(db.Integer, nullable=True) # This will always change if you put it in the intake table, but here it is static

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Food food={self.food_name} cost={self.cost}>"


class Sugar(db.Model):
    """Table to track sugar intake of each user."""

    __tablename__ = "sugar_intake"

    intake_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True) # one user to one food_id at a time
    food_id = db.Column(db.Integer, db.ForeignKey('food.food_id'), index=True) # one food to many users
    date_time = db.Column(db.DateTime)
    notes = db.Column(db.String(64), nullable=True) # FIX ME, IS THIS A DROP DOWN OPTION?

    food = db.relationship("Food", backref="intakes") # not necessary for instantiating a sugar object
    user = db.relationship("User", backref="intakes")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Sugar intake_id={self.intake_id} user_id={self.user_id} food_id={self.food_id} " \
            f"date_time={self.date_time} notes={self.notes}>"

#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    uri = 'postgresql://postgres@db/sugarcoins'
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app

    engine = create_engine(uri)
    seed = False
    if not database_exists(engine.url):
        create_database(engine.url)
        seed = True

    db.init_app(app)

    # automatically seed the database if we just created it
    if seed:
        db.create_all()
        if app.debug:
            # import cycle
            from seed import (
                load_gender,
                load_users,
                load_food,
                load_sugar_intake,
                load_weight,
                load_weight_two,
                load_weight_three,
                load_glucose,
                load_glucose_two,
                load_glucose_three,
            )
            load_gender() # here we loaded Gender first
            load_users()
            load_food()
            load_sugar_intake()
            load_weight()
            load_weight_two()
            load_weight_three()
            load_glucose()
            load_glucose_two()
            load_glucose_three()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.
    from server import app
    connect_to_db(app)

    # you specified db.create_all() here to create the database no need to type this command on the terminal
    db.create_all()

    print("Connected to DB.")
