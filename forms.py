from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AssetForm(FlaskForm):
    name = StringField('Asset Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Laptop', 'Laptop'),
        ('Monitor', 'Monitor'),
        ('Phone', 'Phone'),
        ('Tablet', 'Tablet'),
        ('Peripheral', 'Peripheral'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    serial_number = StringField('Serial Number', validators=[DataRequired()])
    assigned_to = SelectField('Assign To', coerce=int, validators=[DataRequired()])
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d')
    status = SelectField('Status', choices=[
        ('Available', 'Available'),
        ('In Use', 'In Use'),
        ('Faulty', 'Faulty'),
        ('Retired', 'Retired')
    ], validators=[DataRequired()])
    submit = SubmitField('Submit')