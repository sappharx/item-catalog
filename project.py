__author__ = 'vincent'

from flask import Flask, jsonify, request, redirect, render_template, url_for
from flask import session as login_session

app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User


# Connect to Database and create database session
engine = create_engine('sqlite:///items.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# JSON APIs to view Category Information =======================================
@app.route('/category/<int:category_id>/list/JSON')
def categoryListJSON(category_id):
    """Returns a JSON object with a list of all items contained within a category"""
    # category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(ListItems=[i.serialize for i in items])


@app.route('/category/<int:category_id>/list/<int:item_id>/JSON')
def listItemJSON(category_id, item_id):
    """Returns a JSON object that contains the data for one item"""
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


@app.route('/category/JSON')
def categoriesJSON():
    """Returns a JSON object with a list of all categories"""
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


################################################################################

# Web page APIs to display application content =================================

# show all categories
@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    if 'username' not in login_session:
        return render_template('publiccategories.html', categories=categories)
    else:
        return render_template('categories.html', categories=categories)

################################################################################
