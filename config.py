# -*# -*- coding: utf-8 -*-
import telebot
from os import environ
from os import listdir
from os.path import isfile, join
import os, sys
import json
import requests
from telebot import types
from datetime import datetime, date, time,timedelta
# import pymysql
from PIL import Image
# import pymysql
import urllib
import subprocess

import calendar
from threading import Thread
from random import randrange
import time # Librería para hacer que el programa que controla el bot no se acabe.
from pathlib import Path
import logging

from collections import OrderedDict

extra = None
with open('extra_data/extra.json') as f:
    extra = json.load(f)
# responses = {x.split('.')[0]:json.load(open('app/responses/{}'.format(x), encoding='utf-8'), object_pairs_hook=OrderedDict) for x in os.listdir('app/responses')}



# with open('responses.json') as f:
    # responses = json.load(f)

bot = telebot.TeleBot(extra['token'])


###################################################  NEW FUNCTIONS  ###################################################