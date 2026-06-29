import os
import yt_dlp
from django.shortcuts import render
from .forms import MediaForm
from .models import DownloadHistory

def sanitize_cookie_file():
    """Reads the raw cookies.txt and generates a perfectly formatted clean_cookies.txt,
    completely stripping out broken extension-specific internal variables."""
    try:
        with open('cookies.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        with open('clean_cookies.txt', 'w', encoding='utf-8') as f:
            f.write("# Netscape HTTP Cookie File\n\n")
            for line in lines:
                # Skip comments or empty lines to avoid duplicates
                if line.startswith('#') or not line.strip():
                    continue
                
                # CRITICAL: Drop any lines containing extension junk like 'goodTube_'
                if 'goodTube_' in line:
                    continue
                    
                # Ensure the line has exactly 7 valid Netscape columns
                if len(line.split('\t')) == 7:
                    f.write(line)
    except FileNotFoundError:
        pass
# --------------------------------

def home(request):
    submitted_data = None
    extracted_info = None
    error_message = None

    if request.method == "POST":
        form = MediaForm(request.POST)

        if form.is_valid():
            submitted_data = form.cleaned_data

            DownloadHistory.objects.create(
                url=submitted_data["url"],
                quality=submitted_data["quality"],
                download_thumbnail=submitted_data["download_thumbnail"],
                download_subtitle=submitted_data["download_subtitle"],
            )

            # 1. RUN THE CLEANER BEFORE yt-dlp
            sanitize_cookie_file()

            # 2. yt-dlp Extraction logic
            ydl_opts = {
                "format": "best[ext=mp4]/best",
                "quiet": True,
                "noplaylist": True,
                "cookiefile": "clean_cookies.txt", # Use the newly cleaned file!
                "impersonate": "chrome",           # Tells the server to act exactly like Chrome
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