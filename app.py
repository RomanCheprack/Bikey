from flask import Flask, request, render_template
import pandas as pd
from pandas import DataFrame, read_csv
import numpy as np
# from models import ctc, mzm, rm, recycles
import jinja2
import sqlite3

app = Flask(__name__, template_folder='Templates/')
# # print(results)
# if __name__ == '__main__':
#     app.run()


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=['GET'])
@app.route("/home")
def home():

	return render_template('home.html')

@app.route("/e-bikes", methods=['GET'])
def e_bikes():
	conn = get_db_connection() 		
	data = conn.execute("SELECT * FROM 'EMtb'").fetchall()
	conn.close()

	return render_template('e_bikes.html', data = data)

@app.route("/year/<year>", methods=['GET'])
def year_filter(year):
	conn = get_db_connection()
	cursor = conn.execute("""SELECT * FROM 'EMtb' WHERE year == ?""", (year,)).fetchall()	
	conn.close()
	
	return render_template('e_bikes.html', data=cursor)
	
@app.route("/brand/<brand>", methods=['GET', 'POST'])
def brand_filter(brand):
	conn = get_db_connection()
	cursor = conn.execute("""SELECT * FROM 'EMtb' WHERE brand == ?""", (brand,)).fetchall()	
	conn.close()
	
	return render_template('e_bikes.html', data=cursor)

@app.route("/price", methods=['GET',"POST"])
def price_filter():
	upl = int(request.form.get('plow'))
	uph = int(request.form.get('phigh'))
	upl = "{:,}".format(upl)
	uph = "{:,}".format(uph)
	conn = get_db_connection()
	cursor = conn.execute("""SELECT * FROM 'EMtb' WHERE msrp_price >? AND msrp_price <?""", (upl, uph)).fetchall()
	conn.close()

	return render_template('e_bikes.html', data = cursor, upl=upl, uph=uph)

if __name__ == '__main__':
    app.run()