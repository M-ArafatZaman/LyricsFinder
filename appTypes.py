from typing import List, Sequence, Optional, Union
from dataclasses import dataclass

@dataclass 
class ImageType:
    '''
    Data type for profile pictures
    Usually used with lists. Eg List[Image]
    '''
    height: int 
    url: str 
    width: int

@dataclass
class SnippetType:
    keyword: str
    snippet: str

@dataclass
class ArtistType:
    name: str

@dataclass
class ReturnedLyrics:
    '''
    Data type for the songs returned whose lyrics matches the keyword
    '''
    name: str
    lyrics: str
    snippets: Sequence[SnippetType]
    imageURL: str
    artists: str
    url: str
    previewURL: str
    geniusURL: str

# ===================== LOAD PLAYLIST TYPES ============================== # 


@dataclass
class ReturnedPlaylistDetails:
    '''
    Data type for the load playlist API call which returns playlist details and all track songs
    '''

    @dataclass
    class PlaylistOwner:
        '''
        Data type for the owner of the playlist
        '''
        name: str 
        url: str 
        images: List[ImageType]

    @dataclass
    class ExternalUrl:
        spotify: str

    @dataclass 
    class Followers:
        total: int

    @dataclass 
    class Tracks:
        total: int 

    external_urls: ExternalUrl
    description: str
    name: str 
    images: Sequence[ImageType]
    owner: PlaylistOwner 
    followers: Followers 
    tracks: Tracks 

@dataclass 
class ReturnedPlaylistTracks:
    '''
    This is the json response from get tracks api endpoint, which represents each tracks
    '''
    @dataclass 
    class TrackType:
        
        @dataclass 
        class AlbumType:
            images = Sequence[ImageType]

        @dataclass 
        class ExternalUrlType:
            spotify: str 


        album: AlbumType
        artists: Sequence[ArtistType]
        external_urls: ExternalUrlType
        name: str 
        preview_url: Union[str, ]

    track: TrackType

@dataclass 
class ApiResponseLoadPlaylist:

    @dataclass 
    class DataResponse:
        playlist: ReturnedPlaylistDetails 
        has_all_tracks: bool 
        items: Sequence[ReturnedPlaylistTracks]

    status: int 
    data: Optional[DataResponse]

