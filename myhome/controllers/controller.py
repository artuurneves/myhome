import base64

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user

from myhome import app, db, lm
from myhome.models import forms
from myhome.models import tables


@lm.user_loader
def load_user(id):
    return tables.User.query.filter_by(id=id).first()


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('homepage.html')
    else:
        return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password_hash = base64.b64encode(form.password.data.encode())

        if tables.User.query.filter_by(email=email).first():
            flash('Email already regitered')
            return redirect(url_for('login'))

        if tables.User.query.filter_by(username=username).first():
            flash('Username already regitered')
            return redirect(url_for('login'))

        new_user = tables.User(name=name.capitalize(), email=email, username=username, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Registered Successfully. Welcome {form.name.data.capitalize()}")
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = tables.User.query.filter_by(username=form.username.data).first()

        if user and base64.b64encode(form.password.data.encode()) == user.password:
            if form.remember_me.data:
                flash('Logged In')
                login_user(user, remember=True)

            else:
                flash('Logged In')
                login_user(user, remember=False)

            return render_template('homepage.html', name=user.name)
        elif not user:
            flash('Invalid User')
            return redirect(url_for('login'))

        else:

            flash('Invalid Credentials')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/inventory')
def inventory():
    if current_user.is_authenticated:
        inventory = tables.Product.query.all()
        for product in inventory:
            if product.product_type_id == 1:
                flash(f"{product.name} has no category!")
        return render_template('inventory.html', products=inventory)
    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/new_product', methods=['GET', 'POST'])
def new_product():
    if current_user.is_authenticated:
        form = forms.Product()
        product_types = tables.ProductType.query.all()
        choices = ['']
        for pt in product_types:
            choices.append(pt.name)

        form.product_type_id.choices = choices
        if form.validate_on_submit():
            name = form.name.data.capitalize()
            current_qnt = form.current_qnt.data
            necessary_qnt = form.necessary_qnt.data
            product_type_id = form.product_type_id.data
            if tables.Product.query.filter_by(name=name).first():
                flash('Product Already Exists')
                return redirect(url_for('new_product'))
            product_type = tables.ProductType.query.filter_by(name=product_type_id).first()
            new_prod = tables.Product(name=name, current_qnt=current_qnt, necessary_qnt=necessary_qnt, product_type_id=product_type.id)
            db.session.add(new_prod)
            db.session.commit()
            flash('Product Registered Successfully')
        return render_template('new_product.html', form=form)

    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if current_user.is_authenticated:
        choices = []
        product = tables.Product.query.filter_by(id=id).first()
        product_type_name = tables.ProductType.query.filter_by(id=product.product_type_id).first().name
        choices.append(product_type_name)

        product_types = tables.ProductType.query.all()
        for type in product_types:
            if type.name not in choices:
                choices.append(type.name)

        form = forms.Product()
        form.name.data = product.name
        form.current_qnt.data = product.current_qnt
        form.necessary_qnt.data = product.necessary_qnt
        form.product_type_id.choices = choices

        if form.validate_on_submit():
            product.name = form.name.raw_data[0]
            product.current_qnt = form.current_qnt.raw_data[0]
            product.necessary_qnt = form.necessary_qnt.raw_data[0]
            new_product_type = tables.ProductType.query.filter_by(name=form.product_type_id.raw_data[0]).first()
            product.product_type_id = new_product_type.id

            db.session.commit()
            flash('Product Edited Successfully')
            return redirect(url_for('inventory'))
        return render_template('edit_product.html', form=form)

    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/add_product/<int:id>', methods=['GET', 'POST'])
def add_product(id):
    if current_user.is_authenticated:
        product = tables.Product.query.filter_by(id=id).first()
        product.current_qnt += 1
        db.session.commit()
        return redirect(url_for('inventory'))
    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/sub_product/<int:id>', methods=['GET', 'POST'])
def sub_product(id):
    if current_user.is_authenticated:
        product = tables.Product.query.filter_by(id=id).first()
        if product.current_qnt > 0:
            product.current_qnt -= 1
            db.session.commit()
        return redirect(url_for('inventory'))
    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/remove_product/<int:id>', methods=['GET', 'POST'])
def remove_product(id):
    if current_user.is_authenticated:
        product = tables.Product.query.filter_by(id=id).first()
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('inventory'))
    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/new_type', methods=['GET', 'POST'])
def new_type():
    if current_user.is_authenticated:
        form = forms.ProductType()
        types = tables.ProductType.query.all()
        if form.validate_on_submit():
            name = form.name.data.capitalize()
            if tables.ProductType.query.filter_by(name=name).first():
                flash('Type Already Exists')
                return redirect(url_for('new_type'))
            product_type = tables.ProductType(name=name)
            db.session.add(product_type)
            db.session.commit()
            flash('Product Type Registed Successfully')
            return redirect(url_for('new_type'))

        return render_template('new_type.html', form=form, types=types)
    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/edit_type/<int:id>', methods=['GET', 'POST'])
def edit_type(id):
    if current_user.is_authenticated:
        type = tables.ProductType.query.filter_by(id=id).first()
        form = forms.ProductType()
        form.name.data = type.name
        if form.validate_on_submit():
            type.name = form.name.raw_data[0]
            db.session.commit()
            flash('Product Type Edited Successfully')
            return redirect(url_for('new_type'))
        return render_template('edit_type.html', form=form)
    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/remove_type/<int:id>', methods=['GET', 'POST'])
def remove_type(id):
    if current_user.is_authenticated:
        type = tables.ProductType.query.filter_by(id=id).first()
        db.session.delete(type)
        db.session.commit()
        return redirect(url_for('new_type'))
    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/supermarket_list')
def supermarket_list():
    if current_user.is_authenticated:
        products = tables.Product.query.all()
        list = []
        for product in products:
            if product.necessary_qnt - product.current_qnt > 0:
                items = tables.Item.query.filter_by(item_name=product.name)
                values = []
                for item in items:
                    values.append(item.item_price)
                if len(values) > 0:
                    list.append({'name': product.name, 'qnt': product.necessary_qnt - product.current_qnt, 'hp': max(values), 'lp': min(values), 'ap': sum(values) / len(values)})
                else:
                    list.append({'name': product.name, 'qnt': product.necessary_qnt - product.current_qnt, 'hp': '-', 'lp': '-','ap': '-'})
        return render_template('supermarket_list.html', supermarket_list=list)
    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/new_item', methods=['GET', 'POST'])
def new_item():
    if current_user.is_authenticated:
        form = forms.Item()
        if form.validate_on_submit():
            name = form.item_name.data.capitalize()
            brand = form.item_brand.data.capitalize()
            price = form.item_price.data
            quantity = form.item_qnt.data
            item = tables.Item(item_name=name, item_brand=brand, item_price=price, item_qnt=quantity)
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('shopping_list'))
        return render_template('new_item.html', form=form)
    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/edit_item/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    if current_user.is_authenticated:
        item = tables.Item.query.filter_by(item_id=id).first()
        form = forms.Item()
        form.item_name.data = item.item_name
        form.item_brand.data = item.item_brand
        form.item_price.data = item.item_price
        form.item_qnt.data = item.item_qnt

        if form.validate_on_submit():
            item.item_name = form.item_name.raw_data[0]
            item.item_brand = form.item_brand.raw_data[0]
            item.item_price = form.item_price.raw_data[0]
            item.item_qnt = form.item_qnt.raw_data[0]
            db.session.commit()
            return redirect(url_for('shopping_list'))

        return render_template('edit_item.html', form=form)
    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/remove_item/<int:id>', methods=['GET', 'POST'])
def remove_item(id):
    if current_user.is_authenticated:
        item = tables.Item.query.filter_by(item_id=id).first()
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('shopping_list'))
    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/shopping_list', methods=['GET', 'POST'])
def shopping_list():
    if current_user.is_authenticated:
        form = forms.Shopping()
        products = tables.Product.query.all()
        items = tables.Item.query.filter_by(shopping_id=None)
        if form.validate_on_submit():
            supermarket = form.supermarket.data
            date = form.date.data
            shopping = tables.Shopping(supermarket=supermarket, date=date)
            db.session.add(shopping)
            db.session.commit()

            for item in items:
                check_item = True
                item.shopping_id = shopping.id
                for product in products:
                    if item.item_name == product.name:
                        product.current_qnt += item.item_qnt
                        check_item = False
                        break

                if check_item:
                    product = tables.Product(name=item.item_name, current_qnt=item.item_qnt, necessary_qnt=item.item_qnt, product_type_id=1)
                    db.session.add(product)
            db.session.commit()

        return render_template('shopping_list.html', form=form, items=items)
    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/shopping', methods=['GET'])
def shopping():
    if current_user.is_authenticated:
        shopping = tables.Shopping.query.all()

        return render_template('shopping.html', shopping=shopping)
    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/shopping/<int:id>', methods=['GET'])
def shopping_details(id):
    if current_user.is_authenticated:
        items = tables.Item.query.filter_by(shopping_id=id)

        return render_template('shopping_details.html', items=items)
    else:
        flash('Please Log In')
        return redirect(url_for('login'))


@app.route('/teste')
def teste():
    form = forms.Product()
    return render_template('teste.html', form=form)