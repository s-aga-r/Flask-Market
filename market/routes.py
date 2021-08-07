from market import app, db
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/market", methods=["GET", "POST"])
@login_required
def market():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        # Purchase Item
        purchased_item = request.form.get("purchased_item")
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(
                    "You purchased {} for {}".format(
                        p_item_object.name, p_item_object.price
                    ),
                    category="success",
                )
            else:
                flash(
                    "Unfortunately, you don't have enough money to purchase {}!".format(
                        p_item_object.name
                    ),
                    category="warning",
                )
        # Sell Item
        sold_item = request.form.get("sold_item")
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(
                    "You sold {} back to market!".format(s_item_object.name),
                    category="success",
                )
            else:
                flash(
                    "Something went wrong with selling {}!".format(p_item_object.name),
                    category="warning",
                )
        return redirect(url_for("market"))
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template(
            "market.html",
            items=items,
            purchase_form=purchase_form,
            selling_form=selling_form,
            owned_items=owned_items,
        )


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(password_text=form.password.data):
            login_user(user)
            flash(
                "Success! You are logged in as : {}".format(user.username),
                category="success",
            )
            return redirect(url_for("market"))
        else:
            flash("Incorrect username/password!", category="danger")
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(
            "Account created successfully! You are now logged in as : {}".format(
                user.username
            ),
            category="success",
        )

        return redirect(url_for("market"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category="danger")
    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for("index"))
