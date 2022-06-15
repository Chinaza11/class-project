# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 16:44:02 2020

@author: Chinaza Nnamdi
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
from sklearn import *
import pickle
import requests
import json
import geopandas as gpd
import reverse_geocoder
import re
from shapely.geometry import Point, Polygon
import descartes
import joblib
from numpy import *


app = Flask(__name__)


#This code is for accessing the homepage (moving further from here would be easy because of the filter option)
@app.route('/')
def home():
    return render_template('home.html')

#This code is for accessing the homepage (moving further from here would be easy because of the filter option)
@app.route('/first', methods = ['POST', 'GET'])
def first():
    home = request.args.get("home")
    if home == "add_section_form":
        return redirect("/add/section")
    elif home == "template1":
        return redirect("/form/")
    elif home == "dashboard":
        return redirect("/dashboard")


#This code is for adding data manually to the database
@app.route("/add/section", methods=['GET'])
def add_section_form():
    with sqlite3.connect('mydb.db') as con:
        pd.read_sql('select * from treatments', con)
        toReturn=  r'''
<form action='/add/section' method="POST">
    <label for="treatments_name">Treatment:</label>
	  <select name="treatments_name" id="treatments_name">
    <option value="Untreated check">Untreated check</option>
    <option value="Dominus">Dominus</option>
    <option value="Telone">Telone</option>
    <option value="Resistant variety">Resistant variety</option>
    <option value="Pic 60">Pic 60</option>
    <option value="Paladin">Paladin</option>
  </select>
  <br><br>
  <label for="year">Year:</label>
	<select name="year" id="year">
    <option value="2019">2019</option>
    <option value="2020">2020</option>
    </select>
  <br><br>
  <label for="replicate">Replicate:</label>
	<select name="replicate" id="replicate">
    <option value="1">1</option>
    <option value="2">2</option>
    <option value="3">3</option>
    <option value="4">4</option>
    </select>
  <br><br>
	<label for="root_knot_nematode_planting">Root knot nematode planting:</label>
	<input type="number" id="root_knot_nematode_planting" name="root_knot_nematode_planting" min="0" max="1000"><br><br>
    <label for="root_knot_nematode_midseason">Root knot nematode midseason:</label>
	<input type="number" id="root_knot_nematode_midseason" name="root_knot_nematode_midseason" min="0" max="1000"><br><br>
    <label for="root_knot_nematode_end_of_season">Root knot nematode end of season:</label>
	<input type="number" id="root_knot_nematode_end_of_season" name="root_knot_nematode_end_of_season" min="0" max="1000"><br><br>
    <label for="weed">Weed:</label>
	<input type="number" id="weed" name="weed" min="0" max="1000"><br><br>
    <label for="vigor_rating">Vigor rating (0 - 10):</label>
	<input type="number" id="vigor_rating" name="vigor_rating" min="0" max="10"><br><br>
    <label for="gall_rating">Gall rating (0 - 5):</label>
	<input type="number" id="gall_rating" name="gall_rating" min="0" max="5"><br><br>
    <label for="fruit_yield">Fruit yield:</label>
	<input type="number" id="fruit_yield" name="fruit_yield" min="0" max="1000"><br><br>
    <label for="southern_blight">Southern blight:</label>
	<input type="number" id="southern_blight" name="southern_blight" min="0" max="100"><br><br>
    <label for="latitude">Latitude:</label>
	<select name="latitude" id="latitude">
    <option value="31.502951">UGA Black Shank Farm</option>
    <option value="33.8868">UGA Hort Farm</option>
    </select>
    <label for="longitude">Longitude:</label>
	<select name="longitude" id="longitude">
    <option value="-83.545263">UGA Black Shank Farm</option>
    <option value="-83.421349">UGA Hort Farm</option>
    </select>
  <input type="submit" value="Submit">
</form>

        '''
    return toReturn

#This code is for adding data manually to the database
@app.route("/add/section", methods=['POST'])
def add_section():
    treatments_name = request.form['treatments_name']
    year = request.form['year']
    replicate = request.form['replicate']
    root_knot_nematode_planting = request.form['root_knot_nematode_planting']
    root_knot_nematode_midseason = request.form['root_knot_nematode_midseason']
    root_knot_nematode_end_of_season = request.form['root_knot_nematode_end_of_season']
    weed = request.form['weed']
    vigor_rating = request.form['vigor_rating']
    gall_rating = request.form['gall_rating']
    fruit_yield = request.form['fruit_yield']
    southern_blight = request.form['southern_blight']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    with sqlite3.connect('mydb.db') as con:
        cur = con.cursor()
        cur.execute(f'insert into treatments (treatments_name,year,replicate,root_knot_nematode_planting,root_knot_nematode_midseason,root_knot_nematode_end_of_season,weed,vigor_rating,gall_rating,fruit_yield,southern_blight,latitude,longitude) values ("{treatments_name}",{year},{replicate},{root_knot_nematode_planting},{root_knot_nematode_midseason},{root_knot_nematode_end_of_season},{weed},{vigor_rating},{gall_rating},{fruit_yield},{southern_blight},{latitude},{longitude})')
        con.commit()
        cur.close()
    return redirect("/view/section/")

#This code is for viewing data added to the database
@app.route("/view/section/", methods=['GET'])
def view_section():
    with sqlite3.connect('mydb.db') as con:
         df = pd.read_sql('select * from treatments', con)
         toReturn =""
         for i, row in df.iterrows():
            toReturn += f'{row["treatments_id"]} {row["treatments_name"]} {row["year"]} {row["replicate"]} {row["root_knot_nematode_planting"]} {row["root_knot_nematode_midseason"]} {row["root_knot_nematode_end_of_season"]} {row["weed"]} {row["vigor_rating"]} {row["gall_rating"]} {row["fruit_yield"]} {row["southern_blight"]} {row["latitude"]} {row["longitude"]} <br>'
         return toReturn
 
#This code is for adding data to the database via a form        
@app.route("/form/", methods=['GET'])
def template1():
    return render_template("baba.html", page_title="Data upload", page_header="Data upload", page_message="Upload new file")

#This code is for adding data to the database via a form
@app.route("/form/submit", methods=['POST'])
def form_submission():
    error = None
    if request.form['password'] == 'info8000':
        f = request.files['file']
        if f.filename != '':
            csvData = pd.read_csv(f)
            with sqlite3.connect('mydb.db') as con:
                cur = con.cursor()
                for i,row in csvData.iterrows():
                        sql = "insert into treatments (treatments_name,year,replicate,root_knot_nematode_planting,root_knot_nematode_midseason,root_knot_nematode_end_of_season,weed,vigor_rating,gall_rating,fruit_yield,southern_blight,latitude,longitude) values (?,?,?,?,?,?,?,?,?,?,?,?,?)"
                        value = [(row["treatments_name"], row["year"], row["replicate"], row["root_knot_nematode_planting"], row["root_knot_nematode_midseason"], row["root_knot_nematode_end_of_season"], row["weed"], row["vigor_rating"], row["gall_rating"], row["fruit_yield"], row["southern_blight"], row["latitude"], row["longitude"])]
                        cur.executemany(sql, value)
                con.commit()
                cur.close()
        return redirect("/view/section/")
    else:
        return 'Access denied. Please try again.'

#This code is for viewing the dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

#This code is for viewing the dashboard
@app.route('/verify', methods = ['POST', 'GET'])
def verify():
    dashboard = request.args.get("dashboard")
    if dashboard == "sumstat":
        return redirect("/sumstat/")
    elif dashboard == "plot1":
        return redirect("/plot/means1/")
    elif dashboard == "plot2":
        return redirect("/plot/means2/")
    elif dashboard == "sumstat_year":
        return redirect("/sumstat/year/")
    elif dashboard == "geo":
        return redirect("/geo/")
    elif dashboard == "pred_section_form":
        return redirect("/pred/supply")
    elif dashboard == "ml_new":
        return redirect("/ml/new/")

#This code is for accessing the plots
@app.route("/plot/means1/")
def plot1():
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        df = pd.read_sql('select * from treatments',con)
        df1 = df.groupby(['treatments_name']).mean()
        df1 = df1.drop(['treatments_id', 'year', 'replicate'], axis=1)
        df1 = df1.reset_index()
        fig = px.bar(df1, x='treatments_name', y='root_knot_nematode_planting')
        a = fig.to_html(full_html=False, default_height=500, default_width=500)
        fig = px.bar(df1, x='treatments_name', y='root_knot_nematode_midseason')
        b = fig.to_html(full_html=False, default_height=500, default_width=500)
        fig = px.bar(df1, x='treatments_name', y='root_knot_nematode_end_of_season')
        c = fig.to_html(full_html=False, default_height=500, default_width=500)
        fig = px.bar(df1, x='treatments_name', y='weed')
        d = fig.to_html(full_html=False, default_height=500, default_width=500)
        con.commit()
        cur.close()
        return '{}{}{}{}'.format(a,b,c,d)

#This code is for accessing the plots
@app.route("/plot/means2/")
def plot2():
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        df = pd.read_sql('select * from treatments',con)
        df1 = df.groupby(['treatments_name']).mean()
        df1 = df1.drop(['treatments_id', 'year', 'replicate'], axis=1)
        df1 = df1.reset_index()
        fig1 = px.bar(df1, x='treatments_name', y='vigor_rating')
        e = fig1.to_html(full_html=False, default_height=500, default_width=500)
        fig = px.bar(df1, x='treatments_name', y='gall_rating')
        f = fig.to_html(full_html=False, default_height=500, default_width=500)
        fig = px.bar(df1, x='treatments_name', y='fruit_yield')
        g = fig.to_html(full_html=False, default_height=500, default_width=500)
        fig = px.bar(df1, x='treatments_name', y='southern_blight')
        h = fig.to_html(full_html=False, default_height=500, default_width=500)
        con.commit()
        cur.close()
        return '{}{}{}{}'.format(e,f,g,h)

#This code is for accessing the sumstat
@app.route("/sumstat/")
def sumstat():
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        df = pd.read_sql('select * from treatments',con)
        df1 = df.groupby('treatments_name').describe()
        df1 = df1.drop(['treatments_id', 'year','replicate', 'latitude', 'longitude'], axis=1)
        df1 = df1.reset_index()
        con.commit()
        cur.close()
        return df1.to_html()

#This code is for accessing the sumstat
@app.route("/sumstat/year/")
def sumstat_year():
        con = sqlite3.connect('mydb.db')
        cur = con.cursor()
        df = pd.read_sql('select * from treatments',con)
        df1 = df.groupby(['treatments_name', 'year']).describe()
        df1 = df1.drop(['treatments_id', 'replicate','latitude','longitude'], axis=1)
        df1 = df1.reset_index()
        con.commit()
        cur.close()
        return df1.to_html()
    
#This code is for accessing the geographical data
@app.route("/geo/")
def geo():
    df_states = gpd.read_file('gz_2010_us_040_00_500k/')
    df_states = df_states.to_crs("epsg:4326")
    df_states = df_states.query("STATE in ['13']")
    
    con = sqlite3.connect('mydb.db')
    df_loc = pd.read_sql('select * from treatments',con)
    crs = {'init': 'epsg:4326'}
    geometry = [Point(xy) for xy in zip(df_loc["longitude"], df_loc["latitude"])]
    geo_df = gpd.GeoDataFrame(df_loc, crs=crs, geometry=geometry)
    fig,ax = plt.subplots(figsize = (15,15))
    df_states.plot(ax=ax, alpha=0.4, color="grey")
    geo_df.plot(ax=ax, markersize=20, color="red", marker="o", label="Field location")
    plt.title("Map of Georgia", fontsize=50, color="blue")
    plt.legend(prop={'size':15})
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String="data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    c = rf'''<img src="{pngImageB64String}"/>'''
    con.close()
    return '{}'.format(c)




#This code is for inputing data in a new database (in order to make predictions)
@app.route("/pred/supply", methods=['GET'])
def pred_section_form():
    with sqlite3.connect('pred.db') as con:
        pd.read_sql('select * from treatments', con)
        toReturn=  r'''
<form action='/pred/supply' method="POST">
    <label for="treatments_name">Treatment:</label>
	  <select name="treatments_name" id="treatments_name">
    <option value="Untreated check">Untreated check</option>
    <option value="Dominus">Dominus</option>
    <option value="Telone">Telone</option>
    <option value="Resistant variety">Resistant variety</option>
    <option value="Pic 60">Pic 60</option>
    <option value="Paladin">Paladin</option>
  </select>
  <br><br>
  <label for="year">Year:</label>
	<select name="year" id="year">
    <option value="2019">2019</option>
    <option value="2020">2020</option>
    </select>
  <br><br>
  <label for="replicate">Replicate:</label>
	<select name="replicate" id="replicate">
    <option value="1">1</option>
    <option value="2">2</option>
    <option value="3">3</option>
    <option value="4">4</option>
    </select>
  <br><br>
	<label for="root_knot_nematode_planting">Root knot nematode planting:</label>
	<input type="number" id="root_knot_nematode_planting" name="root_knot_nematode_planting" min="0" max="1000"><br><br>
    <label for="root_knot_nematode_midseason">Root knot nematode midseason:</label>
	<input type="number" id="root_knot_nematode_midseason" name="root_knot_nematode_midseason" min="0" max="1000"><br><br>
    <label for="root_knot_nematode_end_of_season">Root knot nematode end of season:</label>
	<input type="number" id="root_knot_nematode_end_of_season" name="root_knot_nematode_end_of_season" min="0" max="1000"><br><br>
    <label for="weed">Weed:</label>
	<input type="number" id="weed" name="weed" min="0" max="1000"><br><br>
    <label for="vigor_rating">Vigor rating (0 - 10):</label>
	<input type="number" id="vigor_rating" name="vigor_rating" min="0" max="10"><br><br>
    <label for="gall_rating">Gall rating (0 - 5):</label>
	<input type="number" id="gall_rating" name="gall_rating" min="0" max="5"><br><br>
    <label for="fruit_yield">Fruit yield:</label>
	<input type="number" id="fruit_yield" name="fruit_yield" min="0" max="1000"><br><br>
    <label for="southern_blight">Southern blight:</label>
	<input type="number" id="southern_blight" name="southern_blight" min="0" max="100"><br><br>
    <label for="latitude">Latitude:</label>
	<select name="latitude" id="latitude">
    <option value="31.502951">UGA Black Shank Farm</option>
    <option value="33.8868">UGA Hort Farm</option>
    </select>
    <label for="longitude">Longitude:</label>
	<select name="longitude" id="longitude">
    <option value="-83.545263">UGA Black Shank Farm</option>
    <option value="-83.421349">UGA Hort Farm</option>
    </select><br><br>
    <label for="dominus">Dominus:</label>
	<select name="dominus" id="dominus">
    <option value="1">Yes</option>
    <option value="0">No</option>
    </select><br><br>
     <label for="paladin">Paladin:</label>
	<select name="paladin" id="paladin">
    <option value="1">Yes</option>
    <option value="0">No</option>
    </select><br><br>
     <label for="pic_60">Pic 60:</label>
	<select name="pic_60" id="pic_60">
    <option value="1">Yes</option>
    <option value="0">No</option>
    </select><br><br>
     <label for="resistant_variety">Resistant Variety:</label>
	<select name="resistant_variety" id="resistant_variety">
    <option value="1">Yes</option>
    <option value="0">No</option>
    </select><br><br>
    <label for="telone">Telone:</label>
	<select name="telone" id="telone">
    <option value="1">Yes</option>
    <option value="0">No</option>
    </select><br><br>
    <label for="untreated_check">Untreated Check:</label>
	<select name="untreated_check" id="untreated_check">
    <option value="1">Yes</option>
    <option value="0">No</option>
    </select><br><br>
  <input type="submit" value="Predict">
</form>
        '''
    return toReturn


#This code is for inputing data in a new database (in order to make predictions)
@app.route("/pred/supply", methods=['POST'])
def pred_section():
    treatments_name = request.form['treatments_name']
    year = request.form['year']
    replicate = request.form['replicate']
    root_knot_nematode_planting = request.form['root_knot_nematode_planting']
    root_knot_nematode_midseason = request.form['root_knot_nematode_midseason']
    root_knot_nematode_end_of_season = request.form['root_knot_nematode_end_of_season']
    weed = request.form['weed']
    vigor_rating = request.form['vigor_rating']
    gall_rating = request.form['gall_rating']
    fruit_yield = request.form['fruit_yield']
    southern_blight = request.form['southern_blight']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    dominus = request.form['dominus']
    paladin = request.form['paladin']
    pic_60 = request.form['pic_60']
    resistant_variety = request.form['resistant_variety']
    telone = request.form['telone']
    untreated_check = request.form['untreated_check']
    with sqlite3.connect('pred.db') as con:
        cur = con.cursor()
        cur.execute(f'insert into treatments (treatments_name,year,replicate,root_knot_nematode_planting,root_knot_nematode_midseason,root_knot_nematode_end_of_season,weed,vigor_rating,gall_rating,fruit_yield,southern_blight,latitude,longitude,dominus,paladin,pic_60,resistant_variety,telone,untreated_check) values ("{treatments_name}",{year},{replicate},{root_knot_nematode_planting},{root_knot_nematode_midseason},{root_knot_nematode_end_of_season},{weed},{vigor_rating},{gall_rating},{fruit_yield},{southern_blight},{latitude},{longitude},{dominus},{paladin},{pic_60},{resistant_variety},{telone},{untreated_check})')
        con.commit()
        cur.close()
    return redirect("/view/pred/")

#This code is for viewing data added to the new database (prediction will be done on this new data)
@app.route("/view/pred/", methods=['GET'])
def view_pred():
    with sqlite3.connect('pred.db') as con:
         df = pd.read_sql('select * from treatments', con)
         toReturn =""
         for i, row in df.iterrows():
            toReturn += f'{row["treatments_id"]} {row["treatments_name"]} {row["year"]} {row["replicate"]} {row["root_knot_nematode_planting"]} {row["root_knot_nematode_midseason"]} {row["root_knot_nematode_end_of_season"]} {row["weed"]} {row["vigor_rating"]} {row["gall_rating"]} {row["fruit_yield"]} {row["southern_blight"]} {row["latitude"]} {row["longitude"]} {row["dominus"]} {row["paladin"]} {row["pic_60"]} {row["resistant_variety"]} {row["telone"]} {row["untreated_check"]}<br>'
         return toReturn
     
#This code is for making predictions to the new data added to the database based on model built from previously uploaded data      
@app.route("/ml/new/")
def ml_new():
    filename = 'finalized_model.sav'

    loaded_model = joblib.load(filename)
    
    con = sqlite3.connect('pred.db')
    df_p = pd.read_sql('select * from treatments',con)
    df_p = df_p [['root_knot_nematode_planting', 'root_knot_nematode_midseason', 'root_knot_nematode_end_of_season', 'weed', 'vigor_rating', 'gall_rating', 'fruit_yield', 'southern_blight', 'dominus', 'paladin', 'pic_60', 'resistant_variety', 'telone', 'untreated_check']]
    df_p = df_p.set_index('root_knot_nematode_planting')
    predictions = loaded_model.predict(df_p)
    results =  pd.DataFrame(predictions,columns=['Predict'])
    
    con.commit()
    con.close()
    
    return results.to_html()

if __name__ == '__main__':
    app.run(debug=True)