import os
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm, AssetForm
from models import db, User, Asset
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret123')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
db.init_app(app)

def seed_users():
    if User.query.first():
        return

    users = [
        User(username='admin', password=generate_password_hash('admin123'), role='admin'),
        User(username='michael', password=generate_password_hash('worldsbest'), role='regular'),
        User(username='dwight', password=generate_password_hash('beets123'), role='regular'),
        User(username='jim', password=generate_password_hash('halpert7'), role='regular'),
        User(username='pam', password=generate_password_hash('artpass1'), role='regular'),
        User(username='angela', password=generate_password_hash('ilovemycat'), role='regular'),
        User(username='kevin', password=generate_password_hash('chilli77'), role='regular'),
        User(username='stanley', password=generate_password_hash('crossword'), role='regular'),
        User(username='kelly', password=generate_password_hash('ryanryan'), role='regular'),
        User(username='creed', password=generate_password_hash('mungbeans'), role='regular'),
        User(username='ryan', password=generate_password_hash('ryan123'), role='regular'),
    ]

    db.session.bulk_save_objects(users)
    db.session.commit()
    print("Users created")

def seed_dummy_assets():
    if Asset.query.first():
        return

    from datetime import date
    
    user_michael = User.query.filter_by(username='michael').first()
    user_dwight = User.query.filter_by(username='dwight').first()
    user_jim = User.query.filter_by(username='jim').first()
    user_pam = User.query.filter_by(username='pam').first()
    user_angela = User.query.filter_by(username='angela').first()
    user_kevin = User.query.filter_by(username='kevin').first()
    user_stanley = User.query.filter_by(username='stanley').first()
    user_kelly = User.query.filter_by(username='kelly').first()
    user_creed = User.query.filter_by(username='creed').first()
    user_admin = User.query.filter_by(username='admin').first()

    dummy_assets = [
        Asset(name='Laptop A', category='Laptop', serial_number='SN2001', assigned_to_id=user_michael.id, purchase_date=date(2022, 5, 10), status='In Use'),
        Asset(name='Monitor A', category='Monitor', serial_number='SN2002', assigned_to_id=user_dwight.id, purchase_date=date(2021, 3, 22), status='Available'),
        Asset(name='Phone A', category='Phone', serial_number='SN2003', assigned_to_id=user_jim.id, purchase_date=date(2023, 1, 14), status='In Use'),
        Asset(name='Tablet A', category='Tablet', serial_number='SN2004', assigned_to_id=user_pam.id, purchase_date=date(2020, 11, 2), status='Retired'),
        Asset(name='Monitor B', category='Monitor', serial_number='SN2005', assigned_to_id=user_angela.id, purchase_date=date(2021, 7, 19), status='Faulty'),
        Asset(name='Laptop B', category='Laptop', serial_number='SN2006', assigned_to_id=user_kevin.id, purchase_date=date(2022, 2, 5), status='In Use'),
        Asset(name='Docking Station A', category='Peripheral', serial_number='SN2007', assigned_to_id=user_stanley.id, purchase_date=date(2023, 4, 1), status='Available'),
        Asset(name='Mouse A', category='Peripheral', serial_number='SN2008', assigned_to_id=user_kelly.id, purchase_date=date(2022, 9, 9), status='In Use'),
        Asset(name='Keyboard A', category='Peripheral', serial_number='SN2009', assigned_to_id=user_creed.id, purchase_date=date(2021, 12, 30), status='In Use'),
        Asset(name='Headset A', category='Peripheral', serial_number='SN2010', assigned_to_id=user_jim.id, purchase_date=date(2023, 6, 15), status='Available'),
        Asset(name='Monitor C', category='Monitor', serial_number='SN2011', assigned_to_id=user_kevin.id, purchase_date=date(2022, 3, 17), status='In Use'),
        Asset(name='Laptop C', category='Laptop', serial_number='SN2012', assigned_to_id=user_admin.id, purchase_date=date(2023, 8, 20), status='Available'),
        Asset(name='Tablet B', category='Tablet', serial_number='SN2013', assigned_to_id=user_pam.id, purchase_date=date(2021, 5, 11), status='In Use'),
        Asset(name='Docking Station B', category='Peripheral', serial_number='SN2014', assigned_to_id=user_angela.id, purchase_date=date(2020, 10, 1), status='Retired'),
        Asset(name='Laptop D', category='Laptop', serial_number='SN2015', assigned_to_id=user_michael.id, purchase_date=date(2022, 11, 8), status='In Use'),
    ]

    db.session.bulk_save_objects(dummy_assets)
    db.session.commit()
    print("assets seeded")

with app.app_context():
    db.create_all()
    seed_users()
    seed_dummy_assets()
    
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_pw, role='regular')
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['username'] = user.username
            session['role'] = user.role
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    assets = Asset.query.all()
    return render_template('dashboard.html', user=session['username'], role=session['role'], assets=assets)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/assets/add', methods=['GET', 'POST'])
def add_asset():
    if 'username' not in session:
        return redirect(url_for('login'))

    form = AssetForm()
    form.assigned_to.choices = [(user.id, user.username) for user in User.query.all()]

    if form.validate_on_submit():
        asset = Asset(
            name=form.name.data,
            category=form.category.data,
            serial_number=form.serial_number.data,
            assigned_to_id=form.assigned_to.data,
            purchase_date=form.purchase_date.data,
            status=form.status.data
        )
        db.session.add(asset)
        db.session.commit()
        flash('Asset added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_asset.html', form=form)

@app.route('/assets/edit/<int:asset_id>', methods=['GET', 'POST'])
def edit_asset(asset_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    asset = Asset.query.get_or_404(asset_id)

    if session['role'] != 'admin' and (
        not asset.assigned_user or asset.assigned_user.username != session['username']
    ):
        flash("You can only edit assets assigned to you.", "danger")
        return redirect(url_for('dashboard'))

    form = AssetForm(obj=asset)
    form.assigned_to.choices = [(user.id, user.username) for user in User.query.all()]

    if form.validate_on_submit():
        asset.name = form.name.data
        asset.category = form.category.data
        asset.serial_number = form.serial_number.data
        asset.assigned_to_id = form.assigned_to.data
        asset.purchase_date = form.purchase_date.data
        asset.status = form.status.data

        db.session.commit()
        flash('Asset updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    else:
        # Only pre-fill this on GET, NOT after submission
        form.assigned_to.data = asset.assigned_to_id

    return render_template('add_asset.html', form=form)

@app.route('/assets/delete/<int:asset_id>')
def delete_asset(asset_id):
    if 'username' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    asset = Asset.query.get_or_404(asset_id)
    db.session.delete(asset)
    db.session.commit()
    flash('Asset deleted.', 'info')
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run()