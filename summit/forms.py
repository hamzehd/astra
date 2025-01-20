from typing import Any
from django import forms

from summit.models import Song
from utils.musixmatch_client import MusixmatchClient
from utils.summarize_helpers import summarize_song

class SummarizeForm(forms.Form):
    title = forms.CharField(label='Song Title')
    artist = forms.CharField(label='Artist Name')

    def clean(self) -> dict[str, Any]:
        musixmatch_client = MusixmatchClient()
        song_search = musixmatch_client.search_song(
            self.cleaned_data['title'],
            self.cleaned_data['artist']
            )
        if not song_search:
            self.add_error('title', "Couldn't match to any songs, please double check the input.")
        if "error" in song_search:
            self.add_error('title', song_search["error"])
        return super().clean()


    def save(self, user):
        """
        Saves the form data to create or retrieve a Song object.

        Args:
            user (User): The user requesting the song summary

        Returns:
            Song or QuerySet[Song]: Either a newly created Song object or existing matching Songs
            
        Note:
            If a Song with matching title and artist already exists, returns the QuerySet of matches.
            Otherwise creates and returns a new Song object for the given title and artist.
        """
        song_query = Song.objects.filter(
            input_title=self.cleaned_data['title'],
            input_artist=self.cleaned_data['artist']
            ).exclude(gen_summary='')
        if song_query.exists():
            return song_query
        song = Song.objects.create(
            requested_by=user,
            input_title=self.cleaned_data['title'],
            input_artist=self.cleaned_data['artist']
        )
        updated_song = summarize_song(song)
        return updated_song
