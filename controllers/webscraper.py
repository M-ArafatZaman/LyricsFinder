import requests, bs4


def scrapeLyricsFromURL(url):
    '''
    This function scrapes the genius url for lyrics and returns it.
    '''
    
    response = requests.get(url)

    # Convert response to bs4 object
    bs4Object = bs4.BeautifulSoup(response.content, "html.parser")
    
    # Lyrics div
    divLyrics = bs4Object.find("div", id="lyrics-root")
    adjustLines = str(divLyrics).replace("\n", "").replace("<br/>", "\n")
    finalLyrics = bs4.BeautifulSoup(adjustLines, "html.parser")
    
    return finalLyrics.get_text()


