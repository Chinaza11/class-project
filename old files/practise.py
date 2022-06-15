# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 14:16:29 2020

@author: nnamd
"""
from flask import Flask, request, render_template, redirect, url_for
from datetime import *
import pytz
import plotly.express as px
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64
import sqlite3
import os
from os.path import join, dirname, realpath

app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)