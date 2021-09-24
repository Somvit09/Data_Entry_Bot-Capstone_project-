from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import time
# using Beautifulsoup to scrape data from the particuler site
WEBSITE_one = 'https://www.makaan.com/listings?beds=1&baths=1plus&budget=0,15000&listingType=rent&pageType=LISTINGS_PROPERTY_URLS&cityName=Kolkata&suburbName=kolkata%20south&cityId=16&suburbId=10038&templateId=MAKAAN_SUBURB_LISTING_RENT'
response = requests.get(WEBSITE_one).text
soup = BeautifulSoup(response, "html.parser")
# selecting links of the details of the houses
all_links = []
all_places = []
all_prices = []
l = soup.select(".title-line a")
links = []
for i in l:
    links.append(i["href"])
for i in range(len(links)):
    if i < 20:
        all_links.append(links[i])
# for detecting places
a = soup.select(".locName a")
for i in a:
    all_places.append(i["data-link-name"])
# for detecting prices
p = soup.select(".val")
prices = []
for i in p:
    prices.append(i.getText())
for i in prices:
    if i == "1 ":
        prices.remove("1 ")
    if i == "":
        prices.remove("")
    if i == "Furnished":
        prices.remove("Furnished")
    if i == "Unfurnished":
        prices.remove("Unfurnished")
    if i == "Semi-Furnished":
        prices.remove("Semi-Furnished")
count = 1
while count < len(prices):
    all_prices.append(prices[count])
    count += 3

# using selenium to use the above data to fill the google form

# PATH WILL BE YOUR LOCATION ON YOUR PC
driver_path = "F:\Development\chromedriver.exe"
# send info to a google form

for i in range(len(all_links)):
    driver = webdriver.Chrome(executable_path=driver_path)
    WEBSITE_two = "https://forms.gle/dLLsQJT7gXFN772a8"
    driver.get(WEBSITE_two)

    time.sleep(3)

    address = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.send_keys(all_places[i])
    price = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.send_keys(all_prices[i])
    link = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.send_keys(all_links[i])
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()
    driver.quit()