from apis import SpotifyAPI, GeniusAPI
from controllers.playlistExtractor import getTracks, getTrackNames
from controllers.lyricsExtractor import getTopLyricsUrl
from controllers.webscraper import scrapeLyricsFromURL
from controllers.loader import Loader
from time import sleep

class LyricsFinder:

    def __init__(self, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, GENIUS_ACCESS_TOKEN, _print=True) -> None:
        self.SPOTIFY_CLIENT_ID = SPOTIFY_CLIENT_ID
        self.SPOTIFY_CLIENT_SECRET = SPOTIFY_CLIENT_SECRET
        self.GENIUS_ACCESS_TOKEN = GENIUS_ACCESS_TOKEN

        self.print = _print

        # Initialize API
        self.SpotifyAPI = SpotifyAPI.SpotifyAPI(self.SPOTIFY_CLIENT_ID, self.SPOTIFY_CLIENT_SECRET)
        self.GeniusAPI = GeniusAPI.GeniusAPI(self.GENIUS_ACCESS_TOKEN)

    
    def parseSpotifyURL(self, url: str) -> str:
        '''
        This method parses a spotify url and returns the id
        Example URL = "https://open.spotify.com/playlist/1dNDQQwOmMkxsGWlngjaDK?si=aaa06e88ddd449a2"
        Return = 1dNDQQwOmMkxsGWlngjaDK
        '''
        DOMAIN = "https://open.spotify.com/playlist/"
        EXAMPLE_ID = "37i9dQZF1DWYnx77Gg1Rgu"
        # All ids are 22 chars long

        # pre_id is before the id in the url
        pre_id = url[:len(DOMAIN)]

        if pre_id != DOMAIN:
            raise Exception("Not a valid spotify playlist URL.")

        id_ = url[len(DOMAIN):]
        
        return id_[:len(EXAMPLE_ID)]


    def searchPlaylist(self, playlistURL: str, keywords: str):
        '''
        This method searches the playlist url through the Spotify API, 
        then uses the GeniusAPI to get the lyrics and searches for keywords
        '''
        playlistID = self.parseSpotifyURL(playlistURL)
        playlistJSON = self.SpotifyAPI.getPlaylistByID(playlistID)
        tracksJSON = getTracks(playlistJSON)
        trackNames = getTrackNames(tracksJSON)
        totalTracks = len(trackNames)

        # Initiate loader
        if self.print: 
            searchLoader = Loader(0, f"Searching tracks 0/{totalTracks}")
            searchLoader.start()
        # Iterate through each in trackname
        for i, name in enumerate(trackNames):
            # Search song in genius api
            hits = self.GeniusAPI.searchSongs(name)
            url = getTopLyricsUrl(hits)
            lyrics = scrapeLyricsFromURL(url)
            if self.print: searchLoader.update((i+1)/totalTracks, f"Searching tracks {i+1}/{totalTracks}")
        
        searchLoader.close()



        
