"""Database models for the Bonnyrigg Pizza Blog.

This module keeps the application's data structure consistent and easy to
maintain. Each class has a clear purpose so the code is modular and readable.
"""

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager


class User(db.Model, UserMixin):
    """Stores account information for registered users and admins."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def set_password(self, password: str) -> None:
        """Hash the password before saving it to protect user data."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Validate an entered password against the stored hash."""
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    """Load a user from the database for secure session management."""
    return User.query.get(int(user_id))


class Recipe(db.Model):
    """Stores pizza recipes shown on the site."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    featured = db.Column(db.Boolean, default=False)
    tags = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='recipe', lazy=True, cascade='all, delete-orphan')


class Comment(db.Model):
    """Stores community comments for each recipe."""

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)


def seed_data():
    """Populate the database with starter content so the teacher can test quickly."""
    if User.query.first():
        return

    admin = User(username='admin', email='admin@bonnyriggpizza.local', is_admin=True)
    admin.set_password('Admin123!')

    demo = User(username='studentchef', email='student@bonnyriggpizza.local')
    demo.set_password('Student123!')

    recipes = [
        Recipe(
            title='Margherita School Special',
            description='A classic pizza with fresh basil, mozzarella and a bright tomato sauce.',
            ingredients='Pizza dough\nTomato sauce\nFresh mozzarella\nBasil leaves\nOlive oil\nSalt',
            instructions='1. Preheat oven to 220°C.\n2. Stretch the dough onto a tray.\n3. Spread sauce evenly.\n4. Add mozzarella pieces.\n5. Bake for 12–15 minutes.\n6. Finish with basil and olive oil.',
            cuisine='Italian',
            difficulty='Easy',
            cooking_time=20,
            image_url='https://images.unsplash.com/photo-1604382355076-af4b0eb60143?auto=format&fit=crop&w=1200&q=80',
            featured=True,
            tags='classic,vegetarian,quick'
        ),
        Recipe(
            title='BBQ Chicken Pizza',
            description='Smoky barbecue sauce, chicken, onion and capsicum make this a student favourite.',
            ingredients='Pizza dough\nBBQ sauce\nCooked chicken\nRed onion\nCapsicum\nMozzarella',
            instructions='1. Preheat oven to 220°C.\n2. Spread BBQ sauce over dough.\n3. Add chicken, onion and capsicum.\n4. Top with mozzarella.\n5. Bake for 15 minutes until golden.',
            cuisine='Australian',
            difficulty='Medium',
            cooking_time=25,
            image_url='https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=1200&q=80',
            featured=True,
            tags='bbq,chicken,party'
        ),
        Recipe(
            title='Pepperoni Feast',
            description='A bold and cheesy pepperoni pizza with crispy edges and extra flavour.',
            ingredients='Pizza dough\nTomato sauce\nPepperoni\nMozzarella\nOregano\nOlive oil',
            instructions='1. Roll out dough.\n2. Add sauce and cheese.\n3. Arrange pepperoni slices.\n4. Sprinkle oregano.\n5. Bake for 12–14 minutes.',
            cuisine='American',
            difficulty='Easy',
            cooking_time=18,
            image_url='https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=1200&q=80',
            featured=False,
            tags='pepperoni,cheesy,fast'
        ),
        Recipe(
            title='Vegetarian Garden Pizza',
            description='Loaded with mushrooms, olives, capsicum and tomatoes for a colourful finish.',
            ingredients='Pizza dough\nTomato sauce\nMushrooms\nOlives\nCapsicum\nTomatoes\nMozzarella',
            instructions='1. Prepare dough and sauce.\n2. Add vegetables evenly.\n3. Sprinkle cheese.\n4. Bake for 15 minutes until vegetables are tender.',
            cuisine='Mediterranean',
            difficulty='Easy',
            cooking_time=22,
            image_url='https://images.unsplash.com/photo-1594007654729-407eedc4be65?auto=format&fit=crop&w=1200&q=80',
            featured=False,
            tags='vegetarian,fresh,healthy'
        ),
        Recipe(
            title='Spicy Meat Lovers Pizza',
            description='A hearty pizza with pepperoni, sausage and chilli flakes for extra heat.',
            ingredients='Pizza dough\nTomato sauce\nPepperoni\nSausage\nMozzarella\nChilli flakes',
            instructions='1. Spread sauce on dough.\n2. Add meats and cheese.\n3. Sprinkle chilli flakes.\n4. Bake for 15 minutes.\n5. Rest for 2 minutes before slicing.',
            cuisine='American',
            difficulty='Medium',
            cooking_time=24,
            image_url='https://images.unsplash.com/photo-1548365328-9f547fb0953b?auto=format&fit=crop&w=1200&q=80',
            featured=True,
            tags='spicy,meat,popular'
        ),
    ]

    db.session.add_all([admin, demo] + recipes)
    db.session.commit()

    starter_comment = Comment(content='This pizza looks amazing. Great for a school food blog!', user_id=demo.id, recipe_id=recipes[0].id)
    db.session.add(starter_comment)
    db.session.commit()
