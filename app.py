from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm, AssetForm
from models import db, User, Asset
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)


### zoha: dummy data seed

def seed_dummy_assets():
    if Asset.query.first():
        return  # Don't insert if data already exists

    from datetime import date

    dummy_assets = [
        Asset(name='Laptop A', category='Laptop', serial_number='SN1001', assigned_to='Alice', purchase_date=date(2022, 5, 10), status='In Use'),
        Asset(name='Monitor B', category='Monitor', serial_number='SN1002', assigned_to='Bob', purchase_date=date(2021, 3, 22), status='Available'),
        Asset(name='Phone X', category='Phone', serial_number='SN1003', assigned_to='Charlie', purchase_date=date(2023, 1, 14), status='In Use'),
        Asset(name='Laptop Z', category='Laptop', serial_number='SN1004', assigned_to='', purchase_date=date(2020, 11, 2), status='Retired'),
        Asset(name='Monitor Y', category='Monitor', serial_number='SN1005', assigned_to='Diana', purchase_date=date(2021, 7, 19), status='Faulty'),
    ]

    db.session.bulk_save_objects(dummy_assets)
    db.session.commit()
    print("✅ Dummy assets seeded.")

def seed_admin_user():
    if User.query.filter_by(username='admin').first():
        return  # Admin already exists

    admin = User(
        username='admin',
        password=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin user created (username: admin, password: admin123)")

with app.app_context():
    db.create_all()
    seed_dummy_assets()
    seed_admin_user()

#zoha: this didnt work originally. idk why.
# @app.before_first_request
# def create_tables():
#     db.create_all()

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
    if form.validate_on_submit():
        asset = Asset(
            name=form.name.data,
            category=form.category.data,
            serial_number=form.serial_number.data,
            assigned_to=form.assigned_to.data,
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
    form = AssetForm(obj=asset)

    if form.validate_on_submit():
        form.populate_obj(asset)
        db.session.commit()
        flash('Asset updated!', 'success')
        return redirect(url_for('dashboard'))
    elif form.errors:
        print("Form errors:", form.errors)

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
