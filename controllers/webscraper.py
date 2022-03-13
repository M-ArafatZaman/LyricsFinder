import requests, bs4

x = '''
<div>something random</div>
<div class="SongPageGriddesktop__TwoColumn-sc-1px5b71-1 hfRKjb Lyrics__Root-sc-1ynbvzw-1 kZmmHP" font-size="largeReading" id="lyrics-root">
    <h2 class="TextLabel-sc-8kw9oj-0 Lyrics__Title-sc-1ynbvzw-0 hHEDka" font-weight="light">
    HUMBLE. Lyrics
    </h2>
    <div class="Lyrics__Container-sc-1ynbvzw-6 jYfhrf" data-lyrics-container="true">
    [Intro]
    <br/>
    <a class="ReferentFragmentVariantdesktop__ClickTarget-sc-1837hky-0 dkZkek" href="/11593050/Kendrick-lamar-humble/Nobody-pray-for-me-it-been-that-day-for-me-way-yeah-yeah">
    <span class="ReferentFragmentVariantdesktop__Highlight-sc-1837hky-1 jShaMP">
    Nobody pray for me
    <br/>
    It been that day for me
    <br/>
    Way (Yeah, yeah)
    </span>
    </a>
    <span style="position:absolute;opacity:0;width:0;height:0;pointer-events:none;z-index:-1" tabindex="0">
    </span>
    <span>
    <span style="position:absolute;opacity:0;width:0;height:0;pointer-events:none;z-index:-1" tabindex="0">
    </span>
    <span style="position:absolute;opacity:0;width:0;height:0;pointer-events:none;z-index:-1" tabindex="0">
    </span>
    </span>
    <br/>
    <br/>
    [Verse 1]
    <br/>
    </div>

    <div data-lyrics-container="false">
    lol wtf
    </div>
</div>
'''

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


