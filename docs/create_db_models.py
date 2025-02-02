# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# Define the tables

class Customer(Base):
    """description: A user on the platform who can buy and sell construction supplies."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

class Product(Base):
    """description: Items available for sale on the marketplace by customers."""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    seller_id = Column(Integer, ForeignKey('customer.id'))
    created_at = Column(DateTime, default=datetime.now)

class Order(Base):
    """description: Orders created by customers for purchasing products."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey('customer.id', ondelete='SET NULL'))
    created_at = Column(DateTime, default=datetime.now)
    total_amount = Column(Float, nullable=False, default=0.0)

class OrderItem(Base):
    """description: Items that are part of an order, linked to a specific product."""
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

class Review(Base):
    """description: Customer reviews for products they have purchased."""
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    customer_id = Column(Integer, ForeignKey('customer.id'))
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

class Category(Base):
    """description: Categories to classify products for easier browsing."""
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)

class ProductCategory(Base):
    """description: Link between products and categories indicating their classification."""
    __tablename__ = 'product_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

class Payment(Base):
    """description: Payment details associated with customer orders."""
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.now)
    method = Column(String(50), nullable=False)  # e.g., Credit Card, PayPal

class Shipping(Base):
    """description: Shipping details for the orders."""
    __tablename__ = 'shipping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    address = Column(Text, nullable=False)  # Shipping address
    delivery_date = Column(DateTime, nullable=True)
    shipping_cost = Column(Float, default=0.0)

class Wishlist(Base):
    """description: Wishlist for customers to save products they intend to purchase later."""
    __tablename__ = 'wishlist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    product_id = Column(Integer, ForeignKey('product.id'))

class Cart(Base):
    """description: Temporary storage for customers while they consider purchasing products."""
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)

class Message(Base):
    """description: Messages exchanged between customers for product information or order details."""
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('customer.id'))
    recipient_id = Column(Integer, ForeignKey('customer.id'))
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.now)

# Create an engine and a session
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Insert some sample data
customers = [
    Customer(name="John Doe", email="john@example.com", password="password123", address="123 Elm St"),
    Customer(name="Jane Smith", email="jane@example.com", password="securepass", address="456 Maple St"),
    Customer(name="Mark Johnson", email="markj@example.com", password="markpass", address="789 Oak St"),
]

products = [
    Product(name="Wooden Planks", description="Quality wooden planks for construction purposes", price=25.75, quantity=100, seller_id=1),
    Product(name="Iron Nails", description="Durable iron nails", price=5.50, quantity=200, seller_id=2),
    Product(name="Concrete Mixer", description="Portable concrete mixer, used", price=300.00, quantity=2, seller_id=3),
]

orders = [
    Order(buyer_id=2, total_amount=52.75),
    Order(buyer_id=1, total_amount=305.50),
]

order_items = [
    OrderItem(order_id=1, product_id=1, quantity=2, price=51.50),
    OrderItem(order_id=1, product_id=2, quantity=1, price=5.50),
    OrderItem(order_id=2, product_id=3, quantity=1, price=300.00),
]

reviews = [
    Review(product_id=1, customer_id=2, rating=4, comment="Good quality wood"),
    Review(product_id=2, customer_id=3, rating=5, comment="The nails are very sturdy"),
]

categories = [
    Category(name="Building Materials", description="Materials for building constructions"),
    Category(name="Tools", description="Various tools for construction work"),
]

product_categories = [
    ProductCategory(product_id=1, category_id=1),
    ProductCategory(product_id=2, category_id=1),
    ProductCategory(product_id=3, category_id=2),
]

payments = [
    Payment(order_id=1, amount=52.75, method="Credit Card"),
    Payment(order_id=2, amount=305.50, method="PayPal"),
]

shippings = [
    Shipping(order_id=1, address="456 Maple St", delivery_date=datetime.now(), shipping_cost=5.00),
    Shipping(order_id=2, address="123 Elm St", delivery_date=datetime.now(), shipping_cost=10.00),
]

wishlists = [
    Wishlist(customer_id=1, product_id=2),
    Wishlist(customer_id=3, product_id=1),
]

carts = [
    Cart(customer_id=1, product_id=3, quantity=1),
    Cart(customer_id=2, product_id=1, quantity=3),
]

messages = [
    Message(sender_id=1, recipient_id=2, content="Hi, is the price negotiable?"),
    Message(sender_id=2, recipient_id=1, content="Hello! The price is fixed."),
]

# Add data to the session
session.add_all(customers + products + orders + order_items + reviews + categories + product_categories + payments + shippings + wishlists + carts + messages)

# Commit the changes
session.commit()
