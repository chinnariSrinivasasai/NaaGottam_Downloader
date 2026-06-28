from django import forms


QUALITY_CHOICES = [
    ("best", "Best Quality"),
    ("1080", "1080p"),
    ("720", "720p"),
    ("480", "480p"),
    ("audio", "Audio Only"),
]


class MediaForm(forms.Form):

    url = forms.URLField(
        label="Media URL",
        max_length=500,
        widget=forms.URLInput(
            attrs={
                "class": "form-input",
                "placeholder": "Paste a media URL",
            }
        ),
    )

    quality = forms.ChoiceField(
        choices=QUALITY_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    download_thumbnail = forms.BooleanField(
        required=False,
        label="Download Thumbnail",
    )

    download_subtitle = forms.BooleanField(
        required=False,
        label="Download Subtitle",
    )