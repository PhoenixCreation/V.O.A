# for requesting to google for weather qery
import requests
# for scraping purposes
from bs4 import BeautifulSoup as bs


# Function for retriving weather from google search for weather
# Params:
#   - city(str): city which we we want weather of
#   - date(str): date of which you want to weather of
#                because this is google search this can be anything like tommorow or dd/mm/yyyy
#   - additional_info(boolean): Not in use currently, for future safety
def get_weather(city, date="", additional_info=False) -> str:
    try:
        # creating url and requests instance
        url = "https://www.google.com/search?q="+"weather "+city + " " + date
        html = requests.get(url).content

        # getting raw data
        soup = bs(html, 'html.parser')

        # If we are sending for current weather then send current temp and sky only
        if date == "":
            # this contains the temp of city
            temp = soup.find(
                'div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text

            # this conatains time and sky description
            data = soup.find(
                'div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

            # format the data
            data = data.split('\n')
            sky = data[1]
            return f'Current Temperature of {city} is {temp[:2]} degree celcius and sky is {sky}'

        # If we are sending for whole day data
        else:
            # I honestly don't how I pulled this off so I won't bother xplaining what is happening.
            data = soup.find_all('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'})
            temp = data[len(data) - 1].text
            sky = temp.split("\n")[1]
            temp = temp.split("\n")[2]
            temp = temp.replace("High:", "highest temprature ")
            temp = temp.replace("Low:", "and lowest temprature ")
            return f'Temperature of {city} will be {temp} with {sky} sky on {date}'
    except:
        # If anything goes wrong
        return f'could not find weather for {city}'
