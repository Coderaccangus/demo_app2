from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql+psycopg2://ecommerce_dev:123456@localhost:5432/jul_ecommerce"

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Model - Table
class Product(db.Model):
    # define tablename
    __tablename__ = "products"
    # define the primary key
    id = db.Column(db.Integer, primary_key=True)
    # more attributes
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)

# Schema
class ProductSchema(ma.Schema):
    class Meta:
        #Fields
        fields = ("id", "name", "description", "price", "stock")

# to handle multiple products
products_schema = ProductSchema(many=True)
# to handle a single products
product_schema = ProductSchema()

# CLI Commands
@app.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@app.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@app.cli.command("seed")
def seed_db():
    # create a product object
    product1 = Product(
        name="Product 1",
        description="Product 1 description",
        price=12.99,
        stock=15
    )

    product2 = Product()
    product2.name = "Product 2"
    product2.price = 149.99
    product2.stock = 25

    # add to session
    db.session.add(product1)
    db.session.add(product2)
    # commit
    db.session.commit()
    print("Tables seeded")

# get all products - /products - GET
# get a single product - /products/id - GET
# create a product - /products - POST
# update a product - /products/id - PUT, PATCH
# delete a product - /products/id - DELETE 

#CRUD for products
# R of CRUD - READ - GET
@app.route("/products")
def get_products():
    stmt = db.select(Product) # Select * FROM products;
    products_list = db.session.scalars(stmt)
    data = products_schema.dump(products_list)
    return data

@app.route("/products/<int:product_id>")
def get_product(product_id):
    stmt = db.select(Product).filter_by(id=product_id) # Select * FROM product WHERE id=product_id;
    product = db.session.scalar(stmt)
    if product:
        data = product_schema.dump(product)
        return data
    else:
        return {"message:": f"product with id {product_id} does not exist"}, 404
