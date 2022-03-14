from .users import SpotifyUserAPI
import requests, json
from utils.utils import print_DT

class SpotifyPlaylistAPI(SpotifyUserAPI):
    '''
    This class inherits from the parent SpotifyAPI class
    '''
    def __init__(self, clientID, clientSecret, _print=False):
        super().__init__(clientID, clientSecret, _print)

    
    # Get a playlist from the api 
    def getPlaylistByID(self, id):
        '''
        Documentation - https://developer.spotify.com/console/get-playlist/
        '''
        returnData = {
            "status": False,
            "data": {}
        }

        # Even though this endpoint contains tracks, it will only be used to collect basic playlist info.
        endpoint = f'https://api.spotify.com/v1/playlists/{id}'
        headers = self.getBearerHeaders()

        # Send request
        if self.print: print_DT("Retrieving playlist details...")

        response = requests.get(endpoint, headers=headers)
        # Convert response to json
        responseJson = json.loads(response.text)

        # Process response
        if response.status_code != 200:
            # Failed to get playlist details
            if self.print:
                print_DT("Failed to retrieve playlist details.")
                print(f"\tResponse status: {response.status_code}")
                print(f"\tError message: {responseJson['error']['message']}")
            
            return returnData

        else:
            
            if self.print: print_DT(f"Successfully retrieved playlist details => {responseJson['name']} by {responseJson['owner']['display_name']}")

            if self.print: print_DT(f"Retrieving tracks from '{responseJson['name']}'...")

            returnData["status"] = True
            returnData["data"]["name"] = responseJson['name']                       # Playlist name
            returnData["data"]["url"] = responseJson["external_urls"]["spotify"]    # Playlist url
            returnData["data"]["owner"] = responseJson['owner']                     # Owner details
            returnData["data"]["images"] = responseJson['images']

            # This endpoint is used to retrieve all the possible tracks using a recursive method
            tracksEndpoint = f"https://api.spotify.com/v1/playlists/{id}/tracks"
            tracks = self.retrieveTracksFromPlaylists(tracksEndpoint)

            
            if tracks["has_all_tracks"]:
                # All Tracks retrieved successfully
                returnData["data"]["has_all_tracks"] = True
            else:
                returnData["data"]["has_all_tracks"] = False

            # Check if ANY tracks has been retrieved
            if type(tracks["tracks"]) == list:
                returnData["data"]["has_tracks"] = True
                returnData["data"]["tracks"] = tracks["tracks"]
            else:
                returnData["data"]["has_tracks"] = False
                returnData["data"]["tracks"] = None


            return returnData


    def retrieveTracksFromPlaylists(self, endpoint):
        '''
        This method executes the get request to retrieve the playlist
        Since the spotify API only returns a maximum of 100 tracks per API hit,
        it also checks if there are any more tracks left to retrieve
        '''
        trackItems = []

        headers = self.getBearerHeaders()

        # Send request and convert response to json
        response = requests.get(endpoint, headers=headers)
        responseJson = json.loads(response.text)

        # Process response
        if response.status_code != 200:
            # If an error occurs
            if self.print:
                print_DT("Failed to retrieve all tracks.")
                print(f"\tResponse status: {response.status_code}")
                print(f"\tError message: {responseJson['error']['message']}")
            
            return {
                "has_all_tracks": False,
                "tracks": None
            }
        
        else:
            # Successfully received tracks    
            nextEndpoint = responseJson["next"]
            trackItems = responseJson["items"]
            
            if nextEndpoint == None:
                # All tracks has been retrieved
                if self.print: print_DT("All tracks has been retrieved.")

                return {
                    "has_all_tracks": True,
                    "tracks": trackItems
                }
            
            else: 
                nextTracks = self.retrieveTracksFromPlaylists(nextEndpoint)

                # If there ARE tracks from the nextEndpoint, combine them
                totalTracks = trackItems
                if type(nextTracks["tracks"]) == list:
                    totalTracks = trackItems + nextTracks["tracks"]

                if nextTracks["has_all_tracks"] == True:
                    # all next tracks has been successfully retrieved
                    return {
                        "has_all_tracks": True,
                        "tracks": totalTracks
                    }
                
                else:
                    # Not all tracks have been retrieved
                    return {
                        "has_all_tracks": False,
                        "tracks": totalTracks
                    }
