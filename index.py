'''
A python CLI application which searches a spotify playlist for songs that matches the keywords.

Mohammad Arafat Zaman
© 2022
All rights reserved
'''
from app import LyricsFinder
from controllers.webscraper import scrapeLyricsFromURL
import json

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
    # 0EXoQPnNMvYKnGp3hyhTQj - Smol playlist - https://open.spotify.com/playlist/0EXoQPnNMvYKnGp3hyhTQj?si=558511c0b3884667
    # 1erDdxiOr53sQ7SMefPWsw - LyricsFinder - https://open.spotify.com/playlist/1erDdxiOr53sQ7SMefPWsw?si=2d8d40153e764517

    app = LyricsFinder(CLIENT_ID, CLIENT_SECRET, GENIUS_ACCESS_TOKEN, True, False)

    #playlist = app.SpotifyAPI.getPlaylistByID("0EXoQPnNMvYKnGp3hyhTQj")
    #print(json.dumps(playlist, indent=4))

    #playlistDetails = app.SpotifyAPI.getPlaylistDetailsByID("3nEcuRHK22K6RqPdUtBMcG")
    #print(json.dumps(playlistDetails, indent=4))

    #playlistTracks = app.SpotifyAPI.getTracksFromPlaylistID("0EXoQPnNMvYKnGp3hyhTQj")

    #userData = app.SpotifyAPI.getUserByID("u9urf67p3ekua3gixkbnleilr")
    #print(json.dumps(userData, indent=4))
    

    searchReturn = app.searchPlaylist("https://open.spotify.com/playlist/1erDdxiOr53sQ7SMefPWsw?si=93bfa1d02ffe4372", "empty")
    print(json.dumps(searchReturn, indent=4))

    #lyrics = app.getLyrics("juice wrld hate the other side")
    #s = app.generateSnippet(lyrics, "hate the other side")
    #print(s)

    #geniusHits = app.GeniusAPI.searchSongs("juice wrld empty")
    #print(json.dumps(geniusHits, indent=4))

    #geniusLyrics = scrapeLyricsFromURL("https://genius.com/Juice-wrld-empty-lyrics")
    #print(geniusLyrics)




