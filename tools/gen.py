
################
# DEPENDENCIES #
################

import requests
from typing import Dict
from tools.config import creds as config 
# if you have spotify API keys make a Dict[str, str] in a config file
# place in same directory as gen.py

"""
Access API Credentials and necessary tokens

--------------------------------------------

The tokens have a window of credibilty. After 3600 seconds (1 hour)
the tokens expire - this is addressed with exceptions on outer functionality

"""


class Spotify_Credentials:

    def __init__(self, verbose: bool = False):

        """
        intitialize object with credentials 
        """
        # set api keys
        self.client_id = config['client_id']
        self.client_secret = config['client_secret']
        # set print verbosity
        self.verbose = verbose
   
    def get_tokens(self: 'Spotify_Credentials') -> Dict[str, str]:

        """
        fetching tokens
        """
        # setting credentials
        grant_type = 'client_credentials'
        body_params = {'grant_type' : grant_type}
        url='https://accounts.spotify.com/api/token'
        # reaching verification endpoint
        response=requests.post(url, data=body_params, auth=(self.client_id, self.client_secret)) 
        response.text
        # setting token
        token = eval(response.text)
        # left here in case you're using jupyter and want to view a print of the tokens
        if self.verbose:
            print('Full Token Data')
            print(token)
            print('\n')
            print('token needed:', token.get('access_token'))
        
        return token

    def get_access(self: 'Spotify_Credentials') -> str:

        """
        request access and generate tokens
        """
        # develop tokens
        return self.get_tokens().get('access_token')

    def get_headers(self: 'Spotify_Credentials') -> Dict[str, str]:

        """
        set headers with get_access functionality and legitmize request
        """
        # verify authorization
        headers = {'Authorization': f'Bearer {self.get_access()}'}

        return headers

