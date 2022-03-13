'''
A python CLI application which searches a spotify playlist for songs that matches the keywords.

Mohammad Arafat Zaman
© 2022
All rights reserved
'''
from apis.SpotifyAPI import SpotifyAPI
from apis.GeniusAPI import GeniusAPI
from controllers.playlistExtractor import getTracks, getTrackNames
from controllers.lyricsExtractor import getTopLyricsUrl
from controllers.webscraper import scrapeLyricsFromURL
from app import LyricsFinder

'''
In the current directory, the client credentials of your spotify developers app,
and an access token of your GENIUS app is stored in a settings.py file. 
It is currently ignored by .gitignore for security reasons.
This is not the most secure way to do it I know, but whatever lol. 
'''
from settings import CLIENT_ID, CLIENT_SECRET, GENIUS_ACCESS_TOKEN


if __name__ == "__main__":
    # 3nEcuRHK22K6RqPdUtBMcG - Subroza slatts
    # 6F0H4bLo9aSNoEd8lyok5i - Quad but arab heat
    # 1dNDQQwOmMkxsGWlngjaDK - Quad's Vibeeee

    """ api = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)
    playlist_json = api.getPlaylistByID("1dNDQQwOmMkxsGWlngjaDK")
    tracks = getTracks(playlist_json) """

    genius = GeniusAPI(GENIUS_ACCESS_TOKEN)


    hits = genius.searchSongs("Kendrick lamar humble")
    url = getTopLyricsUrl(hits)
    lyrics = scrapeLyricsFromURL(url)
    print(lyrics)

    """ app = LyricsFinder(CLIENT_ID, CLIENT_SECRET, GENIUS_ACCESS_TOKEN)

    app.searchPlaylist("https://open.spotify.com/playlist/1dNDQQwOmMkxsGWlngjaDK?si=baf37b5bf291487f", "empty") """



