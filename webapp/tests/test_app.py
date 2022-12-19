from app import test_database, test_username, test_recipeid
import json
import unittest
import sys
from flask import Flask, render_template, request, redirect, url_for, make_response, session
from dotenv import load_dotenv
import os
import pymongo
import datetime
from bson.objectid import ObjectId
# appending the directory of mod.py
# in the sys.path list
sys.path.append('./../')


def test_index_status(app, client):
    res = client.get('/')
    assert res.status_code == 200


def test_index_data(app, client):
    url = '/'
    res = client.get(url)
    assert b'Welcome to Cook Book' in res.data


def test_index_data_2(app, client):
    url = '/'
    res = client.get(url)
    assert b'The best recipe collection app in the world' in res.data


def test_login_button(app, client):
    url = '/'
    res = client.get(url)
    assert b'Log In' in res.data


def test_register_register_button(app, client):
    url = '/'
    res = client.get(url)
    assert b'Don\'t have an account?' in res.data
    assert b'Register' in res.data


def test_login_status(app, client):
    res = client.get('/login')
    assert res.status_code == 200


def test_login_username(app, client):
    url = '/login'
    res = client.get(url)
    assert b'Username' in res.data


def test_login_heading(app, client):
    url = '/login'
    res = client.get(url)
    assert b'Login' in res.data


def test_login_warning(app, client):
    url = '/login'
    res = client.get(url)
    assert b"We'll never share your username with anyone." in res.data


def test_login_password(app, client):
    url = '/login'
    res = client.get(url)
    assert b'Password' in res.data


def test_login_register_button(app, client):
    url = '/login'
    res = client.get(url)
    assert b'Register instead' in res.data


def test_register_login_button(app, client):
    url = '/register'
    res = client.get(url)
    assert b'Login instead' in res.data


def test_register_status(app, client):
    url = '/register'
    res = client.get(url)
    assert b'Username' in res.data


def test_register_heading(app, client):
    url = '/register'
    res = client.get(url)
    assert b'Register' in res.data


def test_register_warning(app, client):
    url = '/register'
    res = client.get(url)
    assert b"We'll never share your username with anyone." in res.data


def test_register_password(app, client):
    url = '/register'
    res = client.get(url)
    assert b'Password' in res.data


def test_browse_status(app, client):
    res = client.get('/browse')
    assert res.status_code == 200


def test_browse_item_peresence(app, client):  # check for items in db
    db = test_database()
    url = '/browse'
    res = client.get(url)
    for item in db.recipes.find({}):
        assert item['title'].encode('utf-8') in res.data


def test_browse_title(app, client):
    url = '/browse'
    res = client.get(url)
    assert b'Browse' in res.data


def test_browse_navbar(app, client):
    url = '/browse'
    res = client.get(url)
    assert b'Browse' in res.data
    assert b'My Recipes' in res.data
    assert b'Add New Recipe' in res.data
    assert b'Saved Recipes' in res.data
    assert b'Log Out' in res.data


def test_add_recipe_status(app, client):
    res = client.get('/recipe-add')
    assert res.status_code == 200
