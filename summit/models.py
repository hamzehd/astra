from django.contrib.auth.models import AbstractUser
from django.db import models



class TimeMixin(models.Model):
    """
    A mixin model that adds created_at and updated_at timestamp fields.

    Attributes:
        created_at (DateTimeField): Automatically set when object is first created
        updated_at (DateTimeField): Automatically updated whenever object is saved
    """
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class User(AbstractUser, TimeMixin):
    """
    Custom user model that extends Django's AbstractUser and includes timestamp fields.
    Inherits all standard Django user fields (username, password, email, etc.) and adds
    created_at/updated_at tracking through TimeMixin.

    The model uses email as the primary identifier for authentication rather than username.
    It provides a __str__ method that returns either the user's full name or email.

    Attributes:
        All fields inherited from AbstractUser including:
            username (CharField): Required. 150 characters or fewer.
            first_name (CharField): Optional. 150 characters or fewer.
            last_name (CharField): Optional. 150 characters or fewer.
            email (EmailField): Required. Must be unique.
            is_staff (BooleanField): Designates whether user can access admin site.
            is_active (BooleanField): Designates whether user account is active.
            date_joined (DateTimeField): When the user account was created.
            
        From TimeMixin:
            created_at (DateTimeField): When this user record was created
            updated_at (DateTimeField): When this user record was last modified
    """

    def __str__(self):
        """Returns the user's email when invoked through string representation."""
        return self.email



class Song(TimeMixin):
    """
    Represents a song with its title, artist, and AI-generated analysis details.

    Attributes:
        input_title (CharField): The title of the song
        input_artist (CharField): The artist who performed the song
        gen_summary (CharField): AI-generated summary of the song
        countries_mentioned (CharField): Countries referenced in the song
        llm_api_request_id (CharField): ID of the LLM API request that generated the analysis
    """
    input_title = models.CharField(max_length=128)
    input_artist = models.CharField(max_length=128)
    gen_summary = models.CharField(max_length=512, verbose_name='Generated Summary')
    countries_mentioned = models.CharField(max_length=512, verbose_name='Countries Mentioned')
    llm_api_request_id = models.CharField(max_length=512, verbose_name='LLM API Request ID')
    requested_by = models.ForeignKey("summit.User", verbose_name="Requested By", on_delete=models.CASCADE)

    def __str__(self):
        """Returns a string representation of the song, formatted as 'title by artist'."""
        return f"{self.input_title} by {self.input_artist} from {self.requested_by}"
