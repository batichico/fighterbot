import telebot
from telebot import types
import json


from os import environ

import os, sys
from PIL import Image

from tradeosFunc import *

from datetime import datetime, date, time,timedelta
import pymysql
import requests
import urllib

import subprocess


with open('extra_data/extra.json') as f:
    extra = json.load(f)

# with open('responses.json') as f:
    # responses = json.load(f)

bot = telebot.TeleBot(extra['token'])