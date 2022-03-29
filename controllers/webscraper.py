import requests, bs4
import time


def scrapeLyricsFromURL(url, cache=True):
    '''
    This function scrapes the genius url for lyrics and returns it.
    '''
    lyrics: str = ""

    params = {}
    # Add a timestamp if cache is false
    if not cache: params["time"] = str(time.time())
    
    response = requests.get(url, params=params)

    # Convert response to bs4 object
    bs4Object = bs4.BeautifulSoup(response.content, "html.parser")

    for each in bs4Object.find_all("div", {"data-lyrics-container": "true"}):
        adjustLines = str(each).replace("\n", "").replace("<br/>", "\n")
        finalLyrics = bs4.BeautifulSoup(adjustLines, "html.parser")
        lyrics += finalLyrics.get_text()
        lyrics += "\n"

    return lyrics



