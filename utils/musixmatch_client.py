import requests

from django.conf import settings


class MusixmatchClient:
    BASE_URL = "https://api.musixmatch.com/ws/1.1/"
    api_key = settings.MUSIXMATCH_API_KEY
    
    def __init__(self):
        """
        Initialize the Musixmatch client with an API key.
        """
        if not self.api_key:
            raise ValueError("API key is required.")

    def search_song(self, title, artist):
        """
        Search for a song using its title and artist name.
        
        Args:
            title (str): The title of the song.
            artist (str): The artist's name.
        
        Returns:
            dict: The JSON response containing song details.
        """
        endpoint = f"{self.BASE_URL}track.search"
        params = {
            "q_track": title,
            "q_artist": artist,
            "apikey": self.api_key,
            "s_track_rating": "desc",
            "f_has_lyrics": 1  # Filter for songs with lyrics
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            # Check if the request went through (200 HTTP)
            if data.get("message", {}).get("header", {}).get("status_code") == 200:
                # Check if there are any available findings
                if data.get("message", {}).get("header", {}).get("available") > 0:
                    track_list = data.get("message", {}).get("body", {}).get("track_list", [])
                    commontrack_id = track_list[0]["track"]["commontrack_id"]
                    return self.get_lyrics(commontrack_id)
                else:
                     return {"error": "Unable to find the requested song", "details": data}   
            else:
                return {"error": "Failed to retrieve song data", "details": data}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_lyrics(self, track_id):
        """
        Search for a song using its title and artist name.
        
        Args:
            track_id (str): String represenation of Track ID on MusixMatch.
        
        Returns:
            string: The lyrics response from the API.
        """
        endpoint = f"{self.BASE_URL}track.lyrics.get"
        params = {
            "commontrack_id": track_id,
            "apikey": self.api_key,
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            if data.get("message", {}).get("header", {}).get("status_code") == 200:
                lyrics_list = data.get("message", {}).get("body", {}).get("lyrics", [])
                if lyrics_list:
                    lyrics = lyrics_list["lyrics_body"]
                else: 
                    return {"error": "Failed to retrieve song lyrics", "details": data}

                return lyrics
            else:
                return {"error": "Failed to retrieve song lyrics", "details": data}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}