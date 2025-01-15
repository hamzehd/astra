from django import forms

from summit.models import Song

class SummarizeForm(forms.Form):
    title = forms.CharField(label='Song Title')
    artist = forms.CharField(label='Artist Name')


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
            )
        if song_query.exists():
            return song_query
        song = Song.objects.create(
            requested_by=user,
            input_title=self.cleaned_data['input_title']
        )
        return song
