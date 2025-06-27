import pytest
from app import app, db
from models import User, Asset
from datetime import date  
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Asset' in response.data

def test_register(client):
    response = client.post('/register', data={
        'username': 'dwight',
        'password': 'beetfarm'
    }, follow_redirects=True)
    assert b'Account created' in response.data

def test_login(client):
    with app.app_context():
        hashed_pw = generate_password_hash('password')
        db.session.add(User(username='jim', password=hashed_pw, role='regular'))
        db.session.commit()

    response = client.post('/login', data={
        'username': 'jim',
        'password': 'password'
    }, follow_redirects=True)
    assert b'Logged in successfully' in response.data

def test_add_asset_as_regular_user(client):
    with app.app_context():
        hashed_pw = generate_password_hash('pam123')
        user = User(username='pam', password=hashed_pw, role='regular')
        db.session.add(user)
        db.session.commit()

    client.post('/login', data={'username': 'pam', 'password': 'pam123'}, follow_redirects=True)

    response = client.post('/assets/add', data={
        'name': 'Monitor X',
        'category': 'Monitor',
        'serial_number': 'SNX12345',
        'assigned_to': '1',
        'purchase_date': '2023-06-01',
        'status': 'Available'
    }, follow_redirects=True)

    assert b'Asset added successfully' in response.data

def test_regular_user_cannot_edit_unassigned_asset(client):
    with app.app_context():
        pam = User(username='pam', password=generate_password_hash('pam123'), role='regular')
        jim = User(username='jim', password=generate_password_hash('jim123'), role='regular')
        db.session.add_all([pam, jim])
        db.session.commit()

        asset = Asset(
            name='Laptop X',
            category='Laptop',
            serial_number='TEST001',
            assigned_to_id=pam.id,
            purchase_date=date(2023, 1, 1),
            status='In Use'
        )
        db.session.add(asset)
        db.session.commit()

        asset_id = asset.id 
        pam_id = pam.id

    client.post('/login', data={'username': 'jim', 'password': 'jim123'}, follow_redirects=True)

    response = client.post(f'/assets/edit/{asset_id}', data={
        'name': 'Laptop X',
        'category': 'Laptop',
        'serial_number': 'TEST001',
        'assigned_to': str(pam_id),
        'purchase_date': '2023-01-01',
        'status': 'In Use'
    }, follow_redirects=True)

    assert b'You can only edit assets assigned to you' in response.data

def test_admin_can_delete_asset(client):
    with app.app_context():
        admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)
        db.session.commit()

        asset = Asset(
            name='Test Laptop',
            category='Laptop',
            serial_number='DEL12345',
            assigned_to_id=None,
            purchase_date=date(2022, 2, 2),
            status='Available'
        )
        db.session.add(asset)
        db.session.commit()
        asset_id = asset.id

    client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)

    response = client.get(f'/assets/delete/{asset_id}', follow_redirects=True)

    assert b'Asset deleted.' in response.data

    with app.app_context():
        deleted = db.session.get(Asset, asset_id)
        assert deleted is None
