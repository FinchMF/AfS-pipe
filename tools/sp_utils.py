
################
# DEPENDENCIES #
################

import sys
import requests
import json
import wget

from typing import List, Dict, TypeVar, Any
DataFrame = TypeVar('pandas.core.frame.DataFrame')

import pandas as pd 
# credentials for API access
from tools.gen import Spotify_Credentials

# root for endpoint construction
root = 'https://api.spotify.com/v1'

"""
Set of utilities developed to interact with spotify's database

-----------------------------------------------------------------

The tools are highly modularized in order to be manipulated and arranged as needed

However, there are standard consolidated packaging of these tools 
for anyone who does has no need for customization

"""

##################
# PLAYLIST UTILS #
##################

"""
The following tools allow you to pull a variety of specified data
given that you have obtained a playlist id

"""

def fetch_songs(playlist: str, headers: Dict[str, str]) -> List[ Dict[str, Any] ]:

    """
    returns list of song objects from a given playlist id
    -----------------------------------------------------
    """
    # constructing the endpoint
    base = f'{root}/playlists/'
    end = '/tracks'
    endpoint = f'{base}{playlist}{end}'
    # requesting data from the endpoint
    r = requests.get(endpoint, headers=headers)
    # convert response into a json
    songs = r.json()

    return songs


def fetch_ids(songs: List[Dict[str, Any]]) -> List[str]:

    """
    receives song objects from a playlist and returns track ids 
    -----------------------------------------------------------
    """

    ids = []
    for song in songs['items']:
        # iterate through each song object
        # locate the track id and append it to a list
        ids.append(song['track']['id'])
    
    return ids

def fetch_titles(songs: List[Dict[str, Any]]) -> List[str]:

    """
    recieves song objects from a playlist and returns track names
    -------------------------------------------------------------
    """

    titles = []
    for song in songs['items']:
        # iterate through each song object
        # locate the track name and append it to a list
        titles.append(song['track']['name'])

    return titles

def fetch_album_ids(songs: List[Dict[str, Any]]) -> List[str]:

    """
    recieves song objects from a playlist and returns a track's album id
    --------------------------------------------------------------------
    """

    album_ids = []
    for song in songs['items']:
        # iterate through each song object
        # locate the track album id and append it to a list
        album_ids.append(song['track']['album']['id'])

    return album_ids

def fetch_albums(songs: List[Dict[str, Any]]) -> List[str]:

    """
    receives song objects from a playlist and returns a track's album name
    ----------------------------------------------------------------------
    """

    album_names = []
    for song in songs['items']:
        # iterate through each song object
        # locate the track album name and append it to a list
        album_names.append(song['track']['album']['name'])

    return album_names

def fetch_release_date(songs: List[Dict[str, Any]]) -> List[str]:

    """
    receives song objects from a playlist and returns a track's album release date
    ------------------------------------------------------------------------------
    """

    release_dates = []
    for song in songs['items']:
        # iterate through each song object
        # locate the track album release date and append it to a list
        release_dates.append(song['track']['album']['release_date'])

    return release_dates
    
def fetch_artist_ids(songs: List[Dict[str, Any]]) -> List[str]:

    """
    receives song objects from a playlist and returns a track's artist id
    ---------------------------------------------------------------------
    """

    artist_ids = []
    for song in songs['items']:
        # iterate through each song object
        # locate the track's artist id and append it to a list
        artist_ids.append(song['track']['artists'][0]['id'])

    return artist_ids

def fetch_artist(songs: List[Dict[str, Any]]) -> List[str]:

    """
    recieves song objects from a playlist and returns a track's artist name
    -----------------------------------------------------------------------
    """

    artists = []
    for song in songs['items']:
        # iterate through each song object
        # locate the track's artist name and append it to a list
        artists.append(song['track']['artists'][0]['name'])

    return artists


def fetch_popularity(songs: List[Dict[str, Any]]) -> List[str]:
    
    """
    receives song objects from a playlist and returns a track's popularity #
    ------------------------------------------------------------------------
    """
    popularity = []
    for song in songs['items']:
        # iterate through each song object
        # locate the track popularity and append it to a list
        popularity.append(song['track']['popularity'])

    return popularity


def fetch_preview_links(songs: List[Dict[str, Any]]) -> List[str]:

    """
    receives song objects from a playlist and returns a track's preview url
    ------------------------------------------------------------------------
    a preview url links to an endpoint of at max 30s of the track
     -  not all tracks have this available - but many do
    """

    previews = []
    for song in songs['items']:
        # iterate through each song object
        # locate the track's preview link and append it to a list
        previews.append(song['track']['preview_url'])

    return previews

def fetch_playlist_songs_data(songs: List[Dict[str, Any]]) -> List[ Dict[str, str] ]:

    """
    recieves song objects from a playlist and returns track's filtered data
    ------------------------------------------------------------------------
    the data object generated is filtered to capture:
        - track
            - id
            - title
        - tracks album
            - id
            - name
        - track release date
        - artist
            - id
            - name
        - track popularity
        - preview url

    this function aggregates the singular functions above into a single filter
    """

    filtered_data = []
    # iterate through list of song objects
    for song in songs['items']:
        # capture filtered data
        data = {

            'id': song['track']['id'],
            'title': song['track']['name'],
            'album_id': song['track']['album']['id'],
            'album_name': song['track']['album']['name'],
            'release_date': song['track']['album']['release_date'],
            'artist_id': song['track']['artists'][0]['id'],
            'artist_name': song['track']['artists'][0]['name'],
            'track_popularity': song['track']['popularity'],
            'preview_url': song['track']['preview_url']
        }
        # make new list of filtered objects
        filtered_data.append(data)

    return filtered_data



################
# ARTIST UTILS #
################


def fetch_artist_albums(artist_id: str, headers: Dict[str, str]) -> Dict[str, str]:

    """
    returns album object with album name as key 
    and album id as value
    given an artist id
    """
    # constructing endpoint
    base = f'{root}/artists/'
    end = '/albums'
    endpoint = f'{base}{artist_id}{end}' 
    # making request
    r = requests.get(endpoint, headers=headers)
    # convert response to json
    artist_albums = r.json()

    albums = {}
    # iterate through returned artist objects (named here as artist_album objects)
    for album in artist_albums['items']:
        # assign album name as key and album id as value
       albums[album['name']] = album['id']


    return albums


def fetch_album_tracks(album_id: str, headers: Dict[str, str], filtered: bool = False) -> List[Dict[str, str]]:

    """
    returns track information from a given album id
    ------------------------------------------------

    option to filter or receive full album object from spotify payload (defualt is Not Filtered)
    
    if Filtered:
        - returns a list of track objects
    if Not Filtered:
        - returns the full album object

    """
    # construct endpoint
    base = f'{root}/albums/'
    end = '/tracks'
    endpoint = f'{base}{album_id}{end}'
    # make request
    r = requests.get(endpoint, headers=headers)
    # convert reponse to json
    album_tracks = r.json()
    # choose to filter if selective info is desired
    if filtered:
        # set list
        track_list = [] 
        # iterate though album object
        for track in album_tracks['items']:
            # build a track object per track
            tracks = {}
            tracks[track['name']] = track['id']
            tracks[track['artists'][0]['name']] = track['artists'][0]['id']
            tracks['preview_url'] = track['preview_url']
            tracks['track_number'] = track['track_number']
            # and append to list
            track_list.append(tracks)

        return track_list

    else:
        # otherwise return the whole album object
        return album_tracks


def fetch_artist_genres(artist_id: str, headers: Dict[str, str]) -> Dict[str, str]:

    """
    returns artist object with:
        - artist name
        - artist id
        - artist genre
    """
    # construct endppoint
    base = f'{root}/v1/artists/'
    endpoint = f'{base}{artist_id}'
    # make request
    r = requests.get(endpoint, headers=headers)
    # convert response to json
    artists_data = r.json()
    # filtered desired artist information
    artist_info = {

        'id': artists_data['id'],
        'artist': artists_data['name'],
        'genres': artists_data['genres']
    }

    return artist_info


################
# SEARCH UTILS #
################

def search(headers: Dict[str, str], q: str, content: str ='album,track,artist', limit: int = 30, offset: int = 0) -> Dict[str, str]:

    """
    searchs for desired content by genre or word search and returns content's name, id and type

    --------------------------------------------------------------------------------------------

    recieves:
        - authentifcation headers
        - query (can be a genre, name, title etc)
        - content (playlist, album, track, artist)
        - limit (amount of objects returned per content type)
        - offset (pagnation)

    returns a filtered data object containing:
        - data type (playlist, artist, track, album)
        - data id
        - data name
    """

    
    # --- STEP 1 --- #
    
    # construct endpoint
    base = f'{root}/search'
    query = f'?q={str(q)}'
    search_type = f'&type={content}'
    limit = f'&limit={limit}'
    # contatiner for filterd data objects as result of search requests
    result_data = []
    # container for endpoints to make search requests
    endpoints = []

    # --- STEP 2 --- #

    # pagnation
    if offset == 0:
        # no pagnation set - construct a single search endpoint
        endpoint = f'{base}{query}&offset={offset}{limit}{search_type}'
        endpoints.append(endpoint)

    else:
        # pagnation set
        for off in range(0, offset):
            # iterate through amount of paging offsets and construct search endpoint for each
            endpoint = f'{base}{query}&offset={off}{limit}{search_type}'
            # append to endpoints container
            endpoints.append(endpoint)

    # --- STEP 3 --- #
    
    for end in endpoints:
        # iterate though endpoints container and make request
        r = requests.get(end, headers=headers)
        # convert response to json
        search_data = r.json()

        for k, v in search_data.items():
            # iterate through each search response
            for i in search_data[k]['items']:
                # filter for specifc results
                data = {

                    'type': i['type'],
                    'id': i['id'],
                    'name': i['name']
                }
                # append to result data container
                result_data.append(data)

    return result_data


def collect_result_ids(result_data: List[Dict[str, str]]) -> (List[str], List[str], List[str], List[str]):

    """
    recieves search data and returns ids for each data type
    --------------------------------------------------------

    The function will return empty lists for each type not contained in the search data
    """
    # set lists
    song_ids = []
    album_ids = []
    artist_ids = []
    playlist_ids = []
    # iterate through the search data
    for data in result_data:
        # check for track types and extract id
        if data['type'] == 'track':

            song_ids.append(data['id'])
        # check for album types and extract id
        if data['type'] == 'album':

            album_ids.append(data['id'])
        # check for artist types and extract id
        if data['type'] == 'artist':

            artist_ids.append(data['id'])
        # check for playlist types and extract id
        if data['type'] == 'playlist':

            playlist_ids.append(data['id'])

    return song_ids, album_ids, artist_ids, playlist_ids


def collect_search_songs(ids: List[str], headers: Dict[str, str]) -> List[Dict[str, Any]]:

    """
    recieves list of song ids and returns a list of song objects
    """
    # set base for endpoint
    base = f'{root}/tracks/'
    # set container for song objects
    songs = []
    for i in ids:
        # iterate through track ids and compelte constructing endpoint
        endpoint = f'{base}{i}'
        # make request
        r = requests.get(endpoint, headers=headers)
        # convert reponse to json
        song = r.json()
        # add to songs container
        songs.append(song)

    return songs


###############################
# HIGH LEVEL FEATURE ANALYSIS #
###############################


def fetch_feature_links(ids: List[str]) -> List[str]:

    """
    recevies a list of song ids and returnes a list a audio feature analysis endpoints
    """
    # set base of endpoint
    base =  f'{root}/audio-features/'
    # set container
    id_links = []
    for i in ids:
        # iterate through song ids finish audio feature analysis endpoint and add to container
        id_links.append(f'{base}{str(i)}')

    return id_links


def fetch_audio_features(id_links: List[str], headers: Dict[str,str]) -> List[Dict[str, Any]]:

    """
    recieved list of endpoints and returns list of audio feature objects
    """
    # set container
    feature_data = []

    for id_ in id_links:
        # iterate through endpoints and make request
        r = requests.get(id_, headers=headers)
        # receive content of response
        data = r.content
        # append json converted data to container
        feature_data.append(json.loads(data))

    return feature_data


def _feature_dataframe(songs: List[Dict[str, Any]], headers: Dict[str, str]) -> DataFrame:

    """
    receives list of song objects and return song meta data in dataframe
    --------------------------------------------------------------------

    the feature dataframe is constructed from a join between:
         - track meta data
         - track audio features

    """
    # collect all song ids
    ids = fetch_ids(songs)
    # collect all song meta data
    metas = fetch_playlist_songs_data(songs)
    # generate endpoints from song ids to request song audio features
    links = fetch_feature_links(ids)
    # collect song audio features
    features = fetch_audio_features(links, headers)
    # remove unneeded columns from feature dataframe
    rmv_list = ['type', 'url', 'track_href', 'analysis_url']
    [[feature.pop(key) for key in rmv_list if key in feature] for feature in features]
    # construct data frames from track's meta and audio feature data
    meta_df = pd.DataFrame(metas)
    feature_df = pd.DataFrame(features)
    # join dataframes on song ids
    return meta_df.join(feature_df.set_index('id'), on='id')


def extract_playlist_song_features(playlist: str, headers: Dict[str, str]) -> DataFrame:

    """
    recieves playlist id and returns 
    meta and audio feature dataframe for each track in playlist
    """
    # calls fetch song function on playlist and headers passed
    songs = fetch_songs(playlist, headers) 
    # calls freature dataframe function on fetched songs and headers passed
    df = _feature_dataframe(songs, headers)

    return df

########################
# FETCH AUDIO WAV FORM #
########################

def collect_audio(preview_url: str, outfname: str) -> None:

    """
    recieves download endpoint and collects wav form of track
    """

    wget.download(preview_url, out=outfname, bar=None)


##########################   
# MULTI FUNCTION OBJECTS #
##########################

class Spoti:

    def __init__(self):
        """
        initialize Spoti object and retireve credible headers for API requests
        """
        self.headers = Spotify_Credentials().get_headers()


    def extract(self: 'Spoti', playlist: str) -> DataFrame:

        """
        recieves playlist and calls audio feature extraction function
        """

        return extract_playlist_song_features(playlist=playlist, headers=self.headers)

    def search(self: 'Spoti', genre: str, offset: int = 10, verbose: bool = True) -> DataFrame:

        """
        receives genre and offset indicator
        returns meta and audio features of track from playlists of given genre
        
        """
        # check for terminal 
        if verbose:
            print('Begin Query...')
        # search for playlists of given genre
        # default limit in seach is set to 30 at line 349
        # offset is variable
        data = search(q=genre, content='playlist', offset=offset, headers=self.headers)
        if verbose:
            print('Data Queried...')
        # set container for dataframes
        dfs = []
        ix = 0
        for d in data:
            # iterate through playlist data objects
            ix += 1
            z = (f'Search and Filter Data: {round(ix/len(data)*100, 2)} % Complete')

            try:
                # extract tracks meta and audio feature from playlist
                frames = self.extract(playlist=d['id'])
                # added extracted to dataframe to dataframe container
                dfs.append(frames)
                if verbose:
                    sys.stdout.write('\r'+z)

            except:
                # if and exception arises continue
                # the error that will arise here deals with credentials 
                # and is resolved through continuing - credentials will be reinstated
                if verbose:
                    sys.stdout.write('\r'+z)
                continue

        try:
            # concatenate list of dataframes
            df = pd.concat(dfs, ignore_index=True)
            # and return contentated frames
            return df

        except:
            # if an exception arises due to onle one dataframe being present
            if len(dfs) == 1:
                # return that dataframe alone
                return dfs[0] 

    @staticmethod
    def collect_wav(endpoint: str, out: str) -> None:

        """
        download audio wav form if available
        """

        collect_audio(preview_url=endpoint, outfname=out)
        





    