from summit.models import Song
from utils.musixmatch_client import MusixmatchClient
from utils.openapi_client import analyze_song_lyrics


def summarize_song(song: Song):
    # Retrieve Lyrics from musixmatch
    musixmatch_client = MusixmatchClient()
    song_lyrics = musixmatch_client.search_song(song.input_title, song.input_artist)
    
    # Analyze Lyrics through OpenAI GPT
    lyrics_response = analyze_song_lyrics(song_lyrics)
    # Convert to Python JSON Object
    
    # Update Song Record
    song.gen_summary = lyrics_response['summary']
    song.countries_mentioned = ' '.join(lyrics_response['countries']) if lyrics_response['countries'] else 'N/A'
    song.llm_api_request_id = lyrics_response['request_id']
    song.save()
    return song