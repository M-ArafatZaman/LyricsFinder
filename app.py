from apis import GeniusAPI
from apis.SpotifyAPI.playlist import SpotifyPlaylistAPI
from controllers.playlistExtractor import getTrackName
from controllers.lyricsExtractor import getTopLyricsUrl
from controllers.webscraper import scrapeLyricsFromURL
from controllers.loader import Loader
# Types
from appTypes import ReturnedLyrics
from typing import List

class LyricsFinder:

    def __init__(self, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, GENIUS_ACCESS_TOKEN, _print=True) -> None:
        self.SPOTIFY_CLIENT_ID = SPOTIFY_CLIENT_ID
        self.SPOTIFY_CLIENT_SECRET = SPOTIFY_CLIENT_SECRET
        self.GENIUS_ACCESS_TOKEN = GENIUS_ACCESS_TOKEN

        self.print = _print

        # Initialize API
        self.SpotifyAPI = SpotifyPlaylistAPI(self.SPOTIFY_CLIENT_ID, self.SPOTIFY_CLIENT_SECRET, self.print)
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

        result = []

        # Retrieve tracks
        playlistID = self.parseSpotifyURL(playlistURL)
        tracksJSON = self.SpotifyAPI.getTracksFromPlaylistID(playlistID)
        allTracks = tracksJSON['tracks']
        totalTracks = len(allTracks)

        # Initiate loader
        if self.print: 
            searchLoader = Loader(0, f"Searching tracks 0/{totalTracks}")
            searchLoader.start()

        # Iterate through each track
        for i, track in enumerate(allTracks):
            match: bool = False
            keywordsMatched: List[str] = []
            # Get track name
            name = getTrackName(track)

            # Get lyircs, if lyrics is none, continue to the next one
            lyrics = self.getLyrics(name)
            if lyrics == None:
                continue

            # Check if any of the keywords is present in the lyrics
            if keywords in lyrics:
                # The exact keyword is matched
                match = True
                keywordsMatched.append(keywords)

            # If there is still no match, Split keywords at each commas and iterate through keyword
            if not match:            
                for keyword in keywords.split(","):
                    if keyword in lyrics:
                        # A match has been found
                        match = True
                        keywordsMatched.append(keyword)

            # If there is a match
            if match:
                result.append({
                    "name": name,
                    "lyrics": lyrics,
                    "snippets": [""],
                    "keywords": keywordsMatched
                })


            if self.print: searchLoader.update((i+1)/totalTracks, f"Searching tracks {i+1}/{totalTracks}")
        
        searchLoader.close()

        return result

    
    def getLyrics(self, name: str) -> str:
        '''
        This method returns the lyrics of a song name
        '''
        # Search song in genius api
        hits = self.GeniusAPI.searchSongs(name)
        # If there are no hits, return none
        if len(hits) < 1:
            return None

        url = getTopLyricsUrl(hits)
        lyrics = scrapeLyricsFromURL(url)

        return lyrics

        



        
