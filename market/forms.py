from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    username = StringField(
        label="username", validators=[Length(min=5, max=30), DataRequired()]
    )
    email_address = StringField(label="email", validators=[Email(), DataRequired()])
    password = PasswordField(
        label="password", validators=[Length(min=8, max=16), DataRequired()]
    )
    confirm_password = PasswordField(
        label="confirm password", validators=[EqualTo("password"), DataRequired()]
    )
    submit = SubmitField(label="register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken! Please try a different one.")

    def validate_email_address(self, email_address):
        user = User.query.filter_by(email_address=email_address.data).first()
        if user:
            raise ValidationError("Email already taken! Please try a different one.")


class LoginForm(FlaskForm):
    username = StringField(
        label="username", validators=[Length(min=5, max=30), DataRequired()]
    )
    password = PasswordField(
        label="password", validators=[Length(min=8, max=16), DataRequired()]
    )
    submit = SubmitField(label="login")


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase Item!")


class SellItemForm(FlaskForm):
    submit = SubmitField(label="Sell Item!")
