# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 17, 2024 19:12:38
# Database: sqlite:////tmp/tmp.TYfPPHnnkl/Builders/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Category(SAFRSBaseX, Base):
    """
    description: Categories to classify products for easier browsing.
    """
    __tablename__ = 'category'
    _s_collection_name = 'Category'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductCategoryList : Mapped[List["ProductCategory"]] = relationship(back_populates="category")



class Customer(SAFRSBaseX, Base):
    """
    description: A user on the platform who can buy and sell construction supplies.
    """
    __tablename__ = 'customer'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    address = Column(Text)
    created_at = Column(DateTime)

    # parent relationships (access parent)

    # child relationships (access children)
    MessageList : Mapped[List["Message"]] = relationship(foreign_keys='[Message.recipient_id]', back_populates="recipient")
    senderMessageList : Mapped[List["Message"]] = relationship(foreign_keys='[Message.sender_id]', back_populates="sender")
    OrderList : Mapped[List["Order"]] = relationship(back_populates="buyer")
    ProductList : Mapped[List["Product"]] = relationship(back_populates="seller")
    CartList : Mapped[List["Cart"]] = relationship(back_populates="customer")
    ReviewList : Mapped[List["Review"]] = relationship(back_populates="customer")
    WishlistList : Mapped[List["Wishlist"]] = relationship(back_populates="customer")



class Message(SAFRSBaseX, Base):
    """
    description: Messages exchanged between customers for product information or order details.
    """
    __tablename__ = 'message'
    _s_collection_name = 'Message'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    sender_id = Column(ForeignKey('customer.id'))
    recipient_id = Column(ForeignKey('customer.id'))
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime)

    # parent relationships (access parent)
    recipient : Mapped["Customer"] = relationship(foreign_keys='[Message.recipient_id]', back_populates=("MessageList"))
    sender : Mapped["Customer"] = relationship(foreign_keys='[Message.sender_id]', back_populates=("senderMessageList"))

    # child relationships (access children)



class Order(SAFRSBaseX, Base):
    """
    description: Orders created by customers for purchasing products.
    """
    __tablename__ = 'order'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    buyer_id = Column(ForeignKey('customer.id', ondelete='SET NULL'))
    created_at = Column(DateTime)
    total_amount = Column(Float, nullable=False)

    # parent relationships (access parent)
    buyer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="order")
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="order")
    ShippingList : Mapped[List["Shipping"]] = relationship(back_populates="order")



class Product(SAFRSBaseX, Base):
    """
    description: Items available for sale on the marketplace by customers.
    """
    __tablename__ = 'product'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    seller_id = Column(ForeignKey('customer.id'))
    created_at = Column(DateTime)

    # parent relationships (access parent)
    seller : Mapped["Customer"] = relationship(back_populates=("ProductList"))

    # child relationships (access children)
    CartList : Mapped[List["Cart"]] = relationship(back_populates="product")
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="product")
    ProductCategoryList : Mapped[List["ProductCategory"]] = relationship(back_populates="product")
    ReviewList : Mapped[List["Review"]] = relationship(back_populates="product")
    WishlistList : Mapped[List["Wishlist"]] = relationship(back_populates="product")



class Cart(SAFRSBaseX, Base):
    """
    description: Temporary storage for customers while they consider purchasing products.
    """
    __tablename__ = 'cart'
    _s_collection_name = 'Cart'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'))
    product_id = Column(ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("CartList"))
    product : Mapped["Product"] = relationship(back_populates=("CartList"))

    # child relationships (access children)



class OrderItem(SAFRSBaseX, Base):
    """
    description: Items that are part of an order, linked to a specific product.
    """
    __tablename__ = 'order_item'
    _s_collection_name = 'OrderItem'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'))
    product_id = Column(ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("OrderItemList"))
    product : Mapped["Product"] = relationship(back_populates=("OrderItemList"))

    # child relationships (access children)



class Payment(SAFRSBaseX, Base):
    """
    description: Payment details associated with customer orders.
    """
    __tablename__ = 'payment'
    _s_collection_name = 'Payment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'))
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime)
    method = Column(String(50), nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)



class ProductCategory(SAFRSBaseX, Base):
    """
    description: Link between products and categories indicating their classification.
    """
    __tablename__ = 'product_category'
    _s_collection_name = 'ProductCategory'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('product.id'))
    category_id = Column(ForeignKey('category.id'))

    # parent relationships (access parent)
    category : Mapped["Category"] = relationship(back_populates=("ProductCategoryList"))
    product : Mapped["Product"] = relationship(back_populates=("ProductCategoryList"))

    # child relationships (access children)



class Review(SAFRSBaseX, Base):
    """
    description: Customer reviews for products they have purchased.
    """
    __tablename__ = 'review'
    _s_collection_name = 'Review'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('product.id'))
    customer_id = Column(ForeignKey('customer.id'))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("ReviewList"))
    product : Mapped["Product"] = relationship(back_populates=("ReviewList"))

    # child relationships (access children)



class Shipping(SAFRSBaseX, Base):
    """
    description: Shipping details for the orders.
    """
    __tablename__ = 'shipping'
    _s_collection_name = 'Shipping'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'))
    address = Column(Text, nullable=False)
    delivery_date = Column(DateTime)
    shipping_cost = Column(Float)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("ShippingList"))

    # child relationships (access children)



class Wishlist(SAFRSBaseX, Base):
    """
    description: Wishlist for customers to save products they intend to purchase later.
    """
    __tablename__ = 'wishlist'
    _s_collection_name = 'Wishlist'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'))
    product_id = Column(ForeignKey('product.id'))

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("WishlistList"))
    product : Mapped["Product"] = relationship(back_populates=("WishlistList"))

    # child relationships (access children)
