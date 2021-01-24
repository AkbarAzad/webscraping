
from bs4 import BeautifulSoup
import requests
import lxml

Print_title = True

#Forexlive
url = "http://www.forexlive.com/SessionWraps" #put URL here
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data,"lxml") #Doing it like this prevents some weird error

if Print_title == True:
    print ("FOREXLIVE LATEST SESSION WRAPS")

a =  soup.body.article.ul.find_all("li")
for item in a:
    if "orderboard" not in item.text:
        if "trade ideas thread" not in item.text:
            print (item.text)
