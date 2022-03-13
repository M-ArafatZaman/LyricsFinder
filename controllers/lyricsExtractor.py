
from typing import Any


def getTopLyricsUrl(apiResponse):
    '''
    This function works with the "hits" attribute from the genius search API - https://docs.genius.com/#search-h2
    It returns the url in string format of the top most search result
    '''
    # Iterate through each hits
    for hit in apiResponse:
        # If current hit is a song, extract details, or else go next
        if hit['type'] == "song":
           return hit['result']['url'] 
        else:
            continue

    # If no match, return None
    return None