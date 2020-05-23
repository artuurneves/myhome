from myhome.extensions.database import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    current_qnt = db.Column(db.Float)
    necessary_qnt = db.Column(db.Float)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_types.id'))

    type = db.relationship('ProductType', foreign_keys=product_type_id)

    def __init__(self, name, current_qnt, necessary_qnt, product_type_id):
        self.name = name
        self.current_qnt = current_qnt
        self.necessary_qnt = necessary_qnt
        self.product_type_id = product_type_id

    def __repr__(self):
        return f"<Product {self.id}>"


class ProductType(db.Model):
    __tablename__ = 'product_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Product Type {self.id}"


class Item(db.Model):
    __tablename__ = 'items'

    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String)
    item_brand = db.Column(db.String)
    item_price = db.Column(db.Float)
    item_qnt = db.Column(db.Float)
    shopping_id = db.Column(db.Integer, db.ForeignKey('shoppings.id'))

    type = db.relationship('Shopping', foreign_keys=shopping_id)

    def __init__(self, item_name, item_brand, item_price, item_qnt):

        self.item_name = item_name
        self.item_brand = item_brand
        self.item_price = item_price
        self.item_qnt = item_qnt

    def __repr__(self):
        return f"<Item {self.id}>"


class Shopping(db.Model):
    __tablename__ = 'shoppings'

    id = db.Column(db.Integer, primary_key=True)
    supermarket = db.Column(db.String)
    date = db.Column(db.Date)

    def __init__(self, supermarket, date):

        self.supermarket = supermarket
        self.date = date

    def __repr__(self):
        return f"<Shopping {self.id}>"
