from decimal import InvalidContext
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as urlreq
import logging as lg
#import pprint
import requests
#lg.basicConfig(filename="scraper_logs.txt",level=lg.INFO,format="%(asctime)s:%(levelname)s: %(message)s")

class rev_scraper:
    def __init__(self,website,searchstring):
        self.website = website
        self.searchstring = searchstring
        
    def flipkart_scraper(self):
        lg.info("flipkart Scraper method called")
        try:
            link = "https://www.flipkart.com/search?q="
            search_link = link + self.searchstring
            # fetching page
            #fetch_page = urlreq(search_link)
            fetch_page = requests.get(search_link)
            fetch_page.encoding = 'utf-8'
            #raw_page = fetch_page.read()
            html_page = bs(fetch_page.text,'html.parser')
            product_boxes = html_page.find_all('div',{'class':'_1AtVbE col-12-12'})
            #deleting first three boxes
            del product_boxes[:3]
            #getting the third product url and opening in new window.
            current = product_boxes[0]
            url_product = "https://www.flipkart.com" + current.div.div.div.a['href']
            get_current_page = urlreq(url_product)
            raw_mode = get_current_page.read()
            html_mode = bs(raw_mode,'html.parser')
            
            
            
            #getting all the review tags
            review_tags = html_mode.find_all("div",{"class":"_16PBlm"})
            ratings = []
            names = []
            comments = []
            headers = []
            try:
                for commentbox in review_tags:
                    try:
                        rating = commentbox.div.div.find_all('div',{'class':'_3LWZlK _1BLPMq'})[0].text
                        ratings.append(rating)
                       
                    except:
                        ratings.append("None")

                    try:
                        name = commentbox.div.div.find_all('p',{'class':'_2sc7ZR _2V5EHH'})[0].text
                        names.append(name)
                    except:
                        names.append("None")

                    try:
                        review = commentbox.div.div.find_all('div',{'class':''})
                        comment = review[0].div.text
                        comments.append(comment)
                    except:
                        comments.append("None")
                    try:
                        header = commentbox.div.div.p.text
                        headers.append(header)
                    except:
                        headers.append("None")
                
                return names,ratings,headers,comments
            except Exception as e:
                lg.exception(e,"----Exception raised while looping through reviews")         
        
        except:
            lg.exception(InvalidContext("website name is not Flipkart, cant call this mehtod"))
            
            
        
        
        
