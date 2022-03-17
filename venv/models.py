from bs4 import BeautifulSoup 
import requests
# import app
import csv
import re
import sqlite3
from pathlib import Path
import pandas as pd

keys = ["brand", "model", "img_link", "link" , "msrp_price", "discount_price", "year"]
years = ["2018", "2019", "2020", "2021", "2022"]
# emtbdb = []

def ctc():
	l = []
	url = "https://www.ctc.co.il/product-category/bikes/e-bikes/e-mtb/"

	result = requests.get(url)
	html = result.content
	soup = BeautifulSoup(html, "html.parser")
	cards = soup.find_all('li', class_="product-warp-item nasa-ver-buttons")

	for card in cards:
		db = {}
		brand = card.find('a', class_="name woocommerce-loop-product__title")["title"]
		brand = brand.split(" ")[0]
		model = card.find('a', class_="name woocommerce-loop-product__title")["title"] 
		y_model = model.strip("Trek")
		model = y_model.rsplit(" ", 1)[0]
		img = card.find('div', class_="main-img")
		img_link = card.find('img', class_="attachment-shop_catalog size-shop_catalog")['data-lazy-src']	
		link = card.find('a', class_="name woocommerce-loop-product__title")['href']
		
		try:	
			price_text = card.find('span', class_="price").text
			split_price = price_text.split("₪")[1].replace(",", "")
			price = int(split_price)
		except IndexError:
			price = price_text
			

		year = y_model.split(" ")[-1]

		if year not in years:
			year = "בקרוב"
		else:
			year

		db["brand"] = brand
		db["model"] = model
		db["img_link"] = img_link
		db["link"] = link
		db["msrp_price"] = price
		db["year"] = year	
		l.append(db)
	# emtbdb.append(l)

	with open('database.csv', 'w', newline='', encoding='utf-8') as file:
		dict_writer = csv.DictWriter(file,keys)
		dict_writer.writeheader()
		dict_writer.writerows(l)
	return

def mzm():
	l = []
	url = "https://www.matzman-merutz.co.il/electric-mountain-bikes"
	result = requests.get(url)
	html = result.content	
	soup = BeautifulSoup(html, "html.parser")
	cards = soup.find_all('div', class_="item text-center")


	for card in cards:
		db = {}
		img_link = card.find('img', class_="img-responsive center-block")["src"]
		img_link = "https://www.matzman-merutz.co.il/" + img_link
	
		brand = card.find('div', class_="firm").text
		model = card.find('h2').text
		if "אופני הרים חשמליים" or "SPECIALIZED" in model:
			model = model.replace("אופני הרים חשמליים", "")
			model = model.replace("SPECIALIZED", "")
		else:
			pass


		price_text = card.find('span', class_= "saleprice").text
		split_price = price_text.split("₪")[0].split("\n")[0].replace(",", "")
		price = int(split_price)

		link = card.find('a')['href']
		link = "https://www.matzman-merutz.co.il/" + link

		year = card.find('div', class_="newOnSite").text
	
		db["brand"] = brand.capitalize()
		db["model"] = model
		db["img_link"] = img_link
		db["link"] = link 
		db["msrp_price"] = price
		db["year"]  = year
		l.append(db)

	with open('database.csv', 'a', newline='', encoding='utf-8') as file:
		dict_writer = csv.DictWriter(file,keys)
		dict_writer.writerows(l)
	return

def rm():
	l = []
	url = "https://www.rosen-meents.co.il/%d7%90%d7%95%d7%a4%d7%a0%d7%99-%d7%94%d7%a8%d7%99%d7%9d-%d7%97%d7%a9%d7%9e%d7%9c%d7%99%d7%99%d7%9d-E-MTB"
	result = requests.get(url)
	html = result.content
	soup = BeautifulSoup(html, "html.parser")
	cards = soup.find_all('div', class_="col-md-4 col-sm-6 col-xs-6")

	for card in cards:
		db = {}
		brand = card.find('div', class_="product-box-top__title").text
		if "MERIDA" in brand:
			model = brand.replace("MERIDA", "")
			brand = "Merida"
		elif "ROCKY MOUNTAIN" in brand:	
			model = brand.replace("ROCKY MOUNTAIN", "")	
			brand = "Rocky Mountain"	

		if "אופני הרים חשמליים" or "אופני" in model:
			model = model.replace("אופני הרים חשמליים", "")
			model = model.replace("אופני", "")
		else:
			pass
		
		img_link = "https://www.rosen-meents.co.il/" + card.find('img', class_="product-box-top__image-item")["data-src"]
		link = card.find('a')['href']
		link = "https://www.rosen-meents.co.il/" + link
		
		try:
			price_text = card.find('span', class_="product-item-price__price-changer").text
			# print(price_text)
			split_price = price_text.split("₪")[0].replace(",", "")
			discount_price = card.find('span', class_="product-box_price-extra-change").text
			trimmed_discount_price = discount_price.replace(",", "")
			msrp_price = int(split_price)
			# print(type(msrp_price))
			discount_price = int(discount_price)
		except:
			msrp_price = price_text
			discount_price = None

		year = card.find('div', class_="product-box-top__title").text
		
		if years[0] in year:
			year = 2018
			model = model.replace("2018", "")
		elif years[1] in year:
			year = 2019
			model = model.replace("2019", "")
		elif years[2] in year:
			year = 2020
			model = model.replace("2020", "")
		elif years[3] in year:
			year = 2021
			model = model.replace("2021", "")
		elif years[4] in year:
			year = 2022
			model = model.replace("2022", "")
		else:
			year = None

		db["brand"] = brand
		db["model"] = model
		db["img_link"] = img_link
		db["msrp_price"] = msrp_price
		# print(type(msrp_price))
		db["discount_price"] = discount_price
		# print(type(discount_price))
		db["link"] = link 
		db["year"]  = year
		l.append(db)
	
	with open('database.csv', 'a', newline='', encoding='utf-8') as file:
		dict_writer = csv.DictWriter(file,keys)
		dict_writer.writerows(l)
	return

def recycles():
	l = []
	url = "https://www.recycles.co.il/e_bike_mtb-%D7%90%D7%95%D7%A4%D7%A0%D7%99_%D7%94%D7%A8%D7%99%D7%9D_%D7%97%D7%A9%D7%9E%D7%9C%D7%99%D7%99%D7%9D"
	result = requests.get(url)
	html = result.content
	soup = BeautifulSoup(html, "html.parser")
	cards = soup.find_all('div', class_="item col-xs-6 col-sm-4")

	for card in cards:
		db = {}

		brand = card.find('div', class_="h2").text
		y_model = card.find('h3').text
		model = y_model.split(' ', 1)[1]
		img_link = card.find('img')['src']
		img_link = "https://www.recycles.co.il/" + img_link 
		link = card.find('a')['href']
		link = "https://www.recycles.co.il/" + link

		try:
			price_text = card.find('span').text
			split_price = price_text.split("₪")[0].replace(",", "")
			price = int(split_price)
		except:
			price = price_text

		year = "20" + y_model.split(" ", 1)[0].strip("'")

		db["brand"] = brand
		db["model"] = model
		db["img_link"] = img_link
		db["msrp_price"] = price
		db["link"] = link 
		db["year"]  = year
		l.append(db)
	# emtbdb.append(l)
	with open('database.csv', 'a', newline='', encoding='utf-8') as file:
		dict_writer = csv.DictWriter(file,keys)
		dict_writer.writerows(l)
	return


Path('database.db').touch()

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS EMtb (brand TEXT, model TEXT, img_link TEXT, msrp_price INT, discount_price INT, link TEXT, year);''')

df = pd.read_csv('database.csv')
df.to_sql("EMtb", conn, if_exists='replace', index=False) 

conn.commit()
conn.close()