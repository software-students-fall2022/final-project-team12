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


def test_register_register_button(app,client):
    url = '/'
    res = client.get(url)
    assert b'Don\'t have an account?' in res.data
    assert b'Register' in res.data
