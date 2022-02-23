from flask import Flask,render_template,request,jsonify
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from my_scrap_module import rev_scraper
from flask_cors import CORS, cross_origin
import logging as lg
#lg.basicConfig(filename="flask_app_logs.txt",level=lg.INFO,format="%(asctime)s:%(levelname)s: %(message)s")
#Mongodb atlas credentials. but lets work in compass for this project
#mynosql2022
#abhishekm94

#database name 
#collection_name = "Rev_Scrap_flipkart"
#dbn = 'scraper_db'
#flipkart_search_url = "https://www.flipkart.com/search?q="
#flipkart_url = "https://www.flipkart.com"

#initialize flask app 
app = Flask(__name__)
CORS(app)

@app.route('/')
@cross_origin()
def index():
    return render_template("index.html")

#initialize route as per request type
@app.route('/scrap',methods=['POST'])
@cross_origin()
def result():
    if request.method == 'POST':
        #getting the input and removing all spaces
        searchstring = request.form['content'].replace(" ","")
        #searchstring = 'iphone12'

        scraper = rev_scraper('flipkart',searchstring=searchstring)
        try:
            names,ratings,headers,comments = scraper.flipkart_scraper()
                
        except Exception as e:
            lg.error(e,'Review are not getting rendered.')
                
                #inserting data into mongodb
        filename = searchstring + ".csv"
        fw = open(filename, "w")
        headers = "Product, Customer Name, Rating, Heading, Comment \n"
        fw.write(headers)
        reviews = []
        try:
            for i in range(len(names)):
                data = {
                "product": searchstring,
                "Name": names[i],
                "ratings": ratings[i],
                "headers": headers[i],
                "comments": comments[i]
                }
                
                reviews.append(data)
                #obj.upload_data(data = reviews)
                        
                    
        except Exception as e:
            lg.error(e,"Error occured while inseritng data in db")
        #return render_template('results.html',review_list)
        
        return render_template('reasults.html',reviews=reviews)
        
    else:
        return render_template('index.html')
        
    
if __name__ == "__main__":
    app.run(debug=True)
    