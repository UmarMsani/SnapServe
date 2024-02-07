from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    home_address = db.Column(db.String(255), nullable=False)
    picture_url = db.Column(db.String(255), nullable=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    picture_url = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)

    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))

    def __repr__(self):
        return f'<CartItem(id={self.id}, user_id={self.user_id}, name={self.name}, amount={self.amount})>'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        flash('You are already logged in.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        phone_number = request.form['phone_number']
        country = request.form['country']
        state = request.form['state']
        home_address = request.form['home_address']
        picture_url = request.form['picture']

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Email already exists. Please log in.')
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password)
        new_user = User(
            email=email,
            password=hashed_password,
            fullname=fullname,
            phone_number=phone_number,
            country=country,
            state=state,
            home_address=home_address,
            picture_url=picture_url
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully. You can now log in.')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating account. Please try again.')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        flash('You are already logged in.')
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
            # User exists, check password
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash('Logged in successfully.')
                return redirect(url_for('profile'))
            else:
                error_message = 'Login failed. Check your username and password.'
                session['error_messages'] = [error_message]
                return redirect(url_for('login'))
        else:
            error_message = 'User does not exist. Please Sign Up.'
            session['error_messages'] = [error_message]
            return redirect(url_for('login'))

    error_messages = session.pop('error_messages', [])
    return render_template('login.html', error_messages=error_messages)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        # Update user profile information
        user.fullname = request.form['fullname']
        user.phone_number = request.form['phone_number']
        user.country = request.form['country']
        user.state = request.form['state']
        user.home_address = request.form['home_address']
        user.picture_url = request.form['picture']

        try:
            db.session.commit()
            flash('Profile updated successfully.')
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile. Please try again.')

    return render_template('profile.html', user=user)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'user_id' not in session:
        flash('You need to log in first.')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        # Add item to the cart
        name = request.form['name']
        amount = float(request.form['amount'])
        picture_url = request.form['picture_url']
        description = request.form['description']

        new_cart_item = CartItem(user_id=user.id, name=name, amount=amount, picture_url=picture_url, description=description)

        try:
            db.session.add(new_cart_item)
            db.session.commit()
            flash(f'{name} added to your cart.')
        except Exception as e:
            db.session.rollback()
            flash('Error adding item to the cart. Please try again.')

    # Fetch items from the database based on the user's ID
    cart_items = CartItem.query.filter_by(user_id=user.id).all()

    return render_template('cart.html', user=user, cart_items=cart_items)

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    try:
        cart_item = CartItem.query.get(item_id)
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify(success=True)
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, error=str(e))
    
# Define the menu route
@app.route('/menu')
def menu():
    return render_template('menu.html')

# Define the about route
@app.route('/about')
def about():
    return render_template('about.html')

# Define the book route
@app.route('/book')
def book():
    return render_template('book.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.')
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        flash('You need to log in first.')
        return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
