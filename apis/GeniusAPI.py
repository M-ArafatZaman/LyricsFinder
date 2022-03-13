import requests, json
from utils.utils import print_DT

class GeniusAPI:
    '''
    This class connects to the genius API using just a "semi-public" access token so it can only access endpoints
    which are not private. 
    '''
    def __init__(self, access_token):
        self.access_token = access_token


    def searchSongs(self, searchTerm):
        '''
        This method searches for songs using the searchTerm from the genius API.
        Documentation - https://docs.genius.com/#search-h2
        '''
        endpoint = "https://api.genius.com/search"
        params = {
            "q": searchTerm
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        # Send request
        response = requests.get(endpoint, params=params, headers=headers)
        responseJson = json.loads(response.text)

        if response.status_code != 200:
            # Failed request
            print_DT(f"Failed to retrieve song '{searchTerm}'.")
            print(f"\tResponse status: {response.status_code}")
            print(f"\tError message: {responseJson['meta']['message']}")
            raise Exception(f"Failed to retrieve song '{searchTerm}'.")
        else:
            # Successfully retrieved song
            
            return responseJson["response"]["hits"]
