import json
from apis import GeniusAPI
from apis.SpotifyAPI.playlist import SpotifyPlaylistAPI
from controllers.playlistExtractor import getTrackName
from controllers.lyricsExtractor import getTopLyricsUrl
from controllers.webscraper import scrapeLyricsFromURL
from controllers.loader import Loader
# Types
from appTypes import ReturnedLyrics, SnippetType
from typing import List

class LyricsFinder:

    def __init__(self, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, GENIUS_ACCESS_TOKEN, _print=True, cache=True) -> None:
        self.SPOTIFY_CLIENT_ID = SPOTIFY_CLIENT_ID
        self.SPOTIFY_CLIENT_SECRET = SPOTIFY_CLIENT_SECRET
        self.GENIUS_ACCESS_TOKEN = GENIUS_ACCESS_TOKEN
        self.cache = cache

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
            return None

        id_ = url[len(DOMAIN):]
        
        return id_[:len(EXAMPLE_ID)]


    def searchPlaylist(self, playlistURL: str, keywords: str) -> List[ReturnedLyrics]:
        '''
        This method searches the playlist url through the Spotify API, 
        then uses the GeniusAPI to get the lyrics and searches for keywords
        '''

        result = []

        # Retrieve tracks
        playlistID = self.parseSpotifyURL(playlistURL)
        if playlistID == None:
            return None
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

            # Check if the keyword phrase is present in the lyrics
            if keywords.lower() in lyrics.lower():
                # The exact keyword is matched
                match = True
                keywordsMatched.append(keywords)

            # If there is still no match, Split keywords at each commas and iterate through keyword
            if not match:            
                for keyword in keywords.split(","):
                    if keyword.lower() in lyrics.lower():
                        # A match has been found
                        match = True
                        keywordsMatched.append(keyword)

            # If there is a match
            if match:
                '''
                Preparing return values
                '''
                snippet: List[SnippetType] = []
                # For each keyword(s) matched, generate a snippet
                for eachKeyword in keywordsMatched:
                    snippet.append({
                        "keyword": eachKeyword,
                        "snippet": self.generateSnippet(lyrics, eachKeyword)
                    })
                
                # Get image of song (Album cover for now)
                albumImages = track["track"]["album"]["images"]
                imageURL = None
                if len(albumImages) >= 0:
                    imageURL = albumImages[0]["url"]

                # Prepare artist name
                artistsArr = []
                for artist in track["track"]["artists"]:
                    artistsArr.append(artist["name"])
                artists = ', '.join(artistsArr)

                result.append({
                    "name": track["track"]["name"],
                    "lyrics": lyrics,
                    "snippets": snippet,
                    "imageURL": imageURL,
                    "artists": artists,
                    "url": track["track"]["external_urls"]["spotify"],
                    "previewURL": track["track"]["preview_url"]
                })


            if self.print: searchLoader.update((i+1)/totalTracks, f"Searching tracks {i+1}/{totalTracks}")
        
        if self.print: searchLoader.close()

        return result

    
    def getLyrics(self, name: str) -> str:
        '''
        This method returns the lyrics of a song name
        '''
        # Search song in genius api
        hits = self.GeniusAPI.searchSongs(name, self.cache)
        # If there are no hits, return none
        if len(hits) < 1:
            return None

        url = getTopLyricsUrl(hits)
        lyrics = scrapeLyricsFromURL(url, self.cache)

        return lyrics


    def generateSnippet(self, lyrics: str, keyword: str) -> str:
        '''
        This function generates snippets from lyrics from a keyword (or phrase)
        '''

        if keyword.lower() not in lyrics.lower():
            return None

        snippet = ""

        # Split lyrics at each instances of "\n"
        lines = lyrics.split("\n")

        # Iterate through each line
        for i, currentLine in enumerate(lines):
            # Check current line
            if keyword.lower() in currentLine.lower():
                prevLine = None
                nextLine = None
                # Get previous and next index only if it is within range
                if (i - 1) >= 0:
                    prevLine = lines[i-1]
                if (i + 1) < len(lines):
                    nextLine = lines[i+1]

                # If both [ and ] is present in line, OR it is empty, remove it from snippet.
                # This is to remove lines like "[Chorus]", "[Verse 1]" etc. 
                if ("[" in prevLine and "]" in prevLine) or (len(prevLine) == 0):
                    prevLine = None
                if ("[" in nextLine and "]" in nextLine) or (len(nextLine) == 0):
                    nextLine = None
                
                # Make snippet
                if prevLine:
                    snippet += f"{prevLine}\n"
                snippet += f"{currentLine}\n"
                if nextLine:
                    snippet += f"{nextLine}"

                break
        
        return snippet

                



        
