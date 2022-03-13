# Static typing
from dataclasses import dataclass
from typing import List

# Type interfaces
@dataclass
class TRACK:
    name: str
    artists: str
    trackID: str


def getTracks(apiResponse) -> List[TRACK]:
    '''
    This function works with a response from the playlist API response.
    Example - https://developer.spotify.com/console/get-playlist/

    It provides with a more simplified json object from the behemoth response from the original API
    '''
    tracks = apiResponse
    tracks_extracted = []

    # Iterate through each tracks
    for song in tracks:
        artists = []

        # Iterate through artists
        for artist in song["track"]["artists"]:
            artists.append(artist["name"])
        
        trackName = song["track"]["name"]
        trackID = song["track"]["id"]

        tracks_extracted.append({
            "name": trackName,
            "artists": artists,
            "trackID": trackID
        })

    return tracks_extracted


def getTrackNames(getTracksResponse) -> List[str]:
    '''
    This function returns the string name of a track from the reponse provided by the getTracks() functions
    '''
    names = []
    for each in getTracksResponse:
        names.append(f"{each['name']} - {', '.join(each['artists'])}")
    
    return names

