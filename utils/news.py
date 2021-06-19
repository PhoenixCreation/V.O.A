# for requesting to news.google.com
import requests
# for scraping purposes
from bs4 import BeautifulSoup


# Function returns the list of news
def get_news():
    # on news.google.com, you will have artcles containing string of news
    # But all the su news also have the same article tag which we don't want
    # We just want the main headings
    # struncture of the newses can be loosly defined as per below
    """
    <div class="xrnccd F6Welf R7GTQ keNKEd j7vNaf ..." ...>
        ...
        <article ...>
            <a class="DY5T1d RZIKme">News string(which we want)</a>
        </article>
        <div ...>
            <article ...>
                <a class="DY5T1d RZIKme">News string(which we DON"T want)</a>
            </article>
            <article ...>
                <a class="DY5T1d RZIKme">News string(which we DON"T want)</a>
            </article>
            ...n times
        </div>
    </div>
    <div class="xrnccd F6Welf R7GTQ keNKEd j7vNaf ..." ...>
        ...
        <article ...>
            <a class="DY5T1d RZIKme">News string(which we want)</a>
        </article>
        <div ...>
            <article ...>
                <a class="DY5T1d RZIKme">News string(which we DON"T want)</a>
            </article>
            <article ...>
                <a class="DY5T1d RZIKme">News string(which we DON"T want)</a>
            </article>
            ...n times
        </div>
    </div>
    ...n times, here n is total different news headline
    """

    # The div class name that contains various newses
    outer_div_class = "xrnccd F6Welf R7GTQ keNKEd j7vNaf"
    # The a class name that conatins actually dusplay news string
    inner_a_class = "DY5T1d RZIKme"

    news = []
    try:
        response = requests.get("https://news.google.com").content
        soup = BeautifulSoup(response, features="html.parser")
        divs = soup.find_all(class_=outer_div_class)
        for div in divs:
            # only find first one as it is the new news, not repeatative
            articles = div.find(class_=inner_a_class)
            for article in articles:
                news.append(str(article).strip())
    except:
        news.append("Something went wrong, try again")

    # Return the news list
    return news
