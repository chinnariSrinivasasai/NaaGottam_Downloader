import yt_dlp
from django.shortcuts import render
from .forms import MediaForm
from .models import DownloadHistory

def home(request):
    submitted_data = None
    extracted_info = None
    error_message = None

    if request.method == "POST":
        form = MediaForm(request.POST)

        if form.is_valid():
            submitted_data = form.cleaned_data

            # Save the download intent to your local database
            DownloadHistory.objects.create(
                url=submitted_data["url"],
                quality=submitted_data["quality"],
                download_thumbnail=submitted_data["download_thumbnail"],
                download_subtitle=submitted_data["download_subtitle"],
            )

            # Local-optimized yt-dlp configuration
            ydl_opts = {
                "format": "best[ext=mp4]/best",
                "quiet": True,
                "noplaylist": True,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(submitted_data["url"], download=False)

                    extracted_info = {
                        "title": info.get("title", "Unknown Title"),
                        "thumbnail": info.get("thumbnail") if submitted_data["download_thumbnail"] else None,
                        "download_url": info.get("url"),
                    }
            except Exception as e:
                error_message = f"Failed: {str(e)}"

    else:
        form = MediaForm()

    return render(
        request,
        "downloader/index.html",
        {
            "form": form,
            "submitted_data": submitted_data,
            "extracted_info": extracted_info,
            "error_message": error_message,
        },
    )