# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

# Open and read the HTML file with utf-8 encoding
with open("templates/snippets/tagweed.html","r" ,errors='ignore') as file:
    html = file.read()

# Create a BeautifulSoup object
soup = BeautifulSoup(html, "html.parser")

# Find all h2 tags and extract their text
divs = soup.find_all("div",{"class":"video-con active-con"})
for div in divs:
    # print(div["video"])
    # print(div.find("img")["src"])
    # print(div.find("div",{"class":"title mx-2"}).text)