from bs4 import BeautifulSoup as bs
import requests


def get_weather(city, date="", additional_info=False) -> str:
    if date.lower() == "today":
        date = ""
    try:
        # creating url and requests instance
        url = "https://www.google.com/search?q="+"weather "+city + " " + date
        html = requests.get(url).content

        # getting raw data
        soup = bs(html, 'html.parser')
        if date == "":
            temp = soup.find(
                'div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text

            # this conatains time and sky description
            data = soup.find(
                'div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

            # format the data
            data = data.split('\n')
            sky = data[1]
            return f'Current Temperature of {city} is {temp[:2]} degree celcius and sky is {sky}'
        else:
            data = soup.find_all('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'})
            temp = data[len(data) - 1].text
            sky = temp.split("\n")[1]
            temp = temp.split("\n")[2]
            temp = temp.replace("°C", " degree celcius ")
            temp = temp.replace("High:", "highest temprature ")
            temp = temp.replace("Low:", "and lowest temprature ")
            return f'Temperature of {city} will be {temp} with {sky} sky on {date}'
    except:
        return f'could not find weather for {city}'
    finally:
        pass
