"""Application routes for the Bonnyrigg Pizza Blog."""

from functools import wraps

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user

from . import db
from .models import Comment, Recipe, User


def admin_required(view_function):
    """Protect admin-only routes."""
    @wraps(view_function)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You must be an administrator to access this page.', 'danger')
            return redirect(url_for('home'))
        return view_function(*args, **kwargs)
    return wrapped


def sanitize_text(value: str, max_length: int) -> str:
    """Simple input validation that trims whitespace and limits size.

    This helps prevent excessive input and improves robustness.
    """
    value = (value or '').strip()
    return value[:max_length]


def register_routes(app):
    """Register all routes on the provided Flask application."""

    @app.route('/')
    def home():
        """Show featured pizzas and recent recipes."""
        featured = Recipe.query.filter_by(featured=True).limit(3).all()
        latest = Recipe.query.order_by(Recipe.created_at.desc()).all()
        return render_template('home.html', featured=featured, recipes=latest)

    @app.route('/recipes')
    def recipes():
        """Search and filter pizza recipes."""
        search_query = sanitize_text(request.args.get('search', ''), 100)
        cuisine = sanitize_text(request.args.get('cuisine', ''), 30)
        difficulty = sanitize_text(request.args.get('difficulty', ''), 20)

        query = Recipe.query
        if search_query:
            like = f'%{search_query}%'
            query = query.filter((Recipe.title.ilike(like)) | (Recipe.tags.ilike(like)) | (Recipe.description.ilike(like)))
        if cuisine:
            query = query.filter_by(cuisine=cuisine)
        if difficulty:
            query = query.filter_by(difficulty=difficulty)

        results = query.order_by(Recipe.created_at.desc()).all()
        cuisines = sorted({recipe.cuisine for recipe in Recipe.query.all()})
        return render_template('recipes.html', recipes=results, cuisines=cuisines, selected_cuisine=cuisine, selected_difficulty=difficulty, search_query=search_query)

    @app.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
    def recipe_detail(recipe_id):
        """Display a recipe and allow logged-in users to comment."""
        recipe = Recipe.query.get_or_404(recipe_id)

        if request.method == 'POST':
            if not current_user.is_authenticated:
                flash('Please log in to post a comment.', 'warning')
                return redirect(url_for('login'))

            content = sanitize_text(request.form.get('content'), 300)
            if len(content) < 3:
                flash('Comment must be at least 3 characters long.', 'danger')
            else:
                comment = Comment(content=content, user_id=current_user.id, recipe_id=recipe.id)
                db.session.add(comment)
                db.session.commit()
                flash('Comment added successfully.', 'success')
                return redirect(url_for('recipe_detail', recipe_id=recipe.id))

        return render_template('recipe_detail.html', recipe=recipe)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Create a new user account with basic input validation."""
        if request.method == 'POST':
            username = sanitize_text(request.form.get('username'), 30)
            email = sanitize_text(request.form.get('email'), 120)
            password = request.form.get('password', '')
            confirm = request.form.get('confirm_password', '')

            errors = []
            if len(username) < 3:
                errors.append('Username must be at least 3 characters.')
            if '@' not in email or '.' not in email:
                errors.append('Please enter a valid email address.')
            if len(password) < 8:
                errors.append('Password must be at least 8 characters.')
            if password != confirm:
                errors.append('Passwords do not match.')
            if User.query.filter_by(username=username).first():
                errors.append('Username is already taken.')
            if User.query.filter_by(email=email).first():
                errors.append('Email is already registered.')

            if errors:
                for error in errors:
                    flash(error, 'danger')
            else:
                user = User(username=username, email=email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash('Your account was created successfully. Please log in.', 'success')
                return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Authenticate a user securely using hashed passwords."""
        if request.method == 'POST':
            email = sanitize_text(request.form.get('email'), 120)
            password = request.form.get('password', '')

            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user, remember=True)
                flash('Welcome back. You are now logged in.', 'success')
                return redirect(url_for('home'))
            flash('Invalid email or password.', 'danger')

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        """End the current user session safely."""
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))

    @app.route('/admin', methods=['GET', 'POST'])
    @login_required
    @admin_required
    def admin_dashboard():
        """Manage recipe content from a simple admin dashboard."""
        if request.method == 'POST':
            title = sanitize_text(request.form.get('title'), 100)
            description = sanitize_text(request.form.get('description'), 300)
            ingredients = sanitize_text(request.form.get('ingredients'), 2000)
            instructions = sanitize_text(request.form.get('instructions'), 3000)
            cuisine = sanitize_text(request.form.get('cuisine'), 50)
            difficulty = sanitize_text(request.form.get('difficulty'), 20)
            tags = sanitize_text(request.form.get('tags'), 120)
            image_url = sanitize_text(request.form.get('image_url'), 255)

            try:
                cooking_time = int(request.form.get('cooking_time', 0))
            except ValueError:
                cooking_time = 0

            if not all([title, description, ingredients, instructions, cuisine, difficulty, tags, image_url]) or cooking_time <= 0:
                flash('All fields are required and cooking time must be a positive number.', 'danger')
            else:
                recipe = Recipe(
                    title=title,
                    description=description,
                    ingredients=ingredients,
                    instructions=instructions,
                    cuisine=cuisine,
                    difficulty=difficulty,
                    cooking_time=cooking_time,
                    image_url=image_url,
                    tags=tags,
                    featured=bool(request.form.get('featured'))
                )
                db.session.add(recipe)
                db.session.commit()
                flash('Recipe added successfully.', 'success')
                return redirect(url_for('admin_dashboard'))

        recipe_list = Recipe.query.order_by(Recipe.created_at.desc()).all()
        return render_template('admin.html', recipes=recipe_list)

    @app.route('/delete-recipe/<int:recipe_id>', methods=['POST'])
    @login_required
    @admin_required
    def delete_recipe(recipe_id):
        """Delete a recipe from the admin dashboard."""
        recipe = Recipe.query.get_or_404(recipe_id)
        db.session.delete(recipe)
        db.session.commit()
        flash('Recipe deleted successfully.', 'info')
        return redirect(url_for('admin_dashboard'))

    @app.errorhandler(404)
    def page_not_found(error):
        """Handle missing pages without crashing the application."""
        return render_template('error.html', error_code=404, message='The page you requested could not be found.'), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle unexpected server errors gracefully."""
        db.session.rollback()
        return render_template('error.html', error_code=500, message='Something went wrong on the server. Please try again.'), 500
