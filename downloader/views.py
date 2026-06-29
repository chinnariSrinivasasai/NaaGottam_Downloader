import os
import yt_dlp
from pathlib import Path
from django.shortcuts import render
from .forms import MediaForm
from .models import DownloadHistory

BASE_DIR = Path(__file__).resolve().parent.parent
deno_path = os.path.join(BASE_DIR, '.deno', 'bin')
os.environ["PATH"] += os.pathsep + deno_path

def sanitize_cookie_file():
    """Reads the raw cookies.txt and generates a perfectly formatted clean_cookies.txt,
    fixing Python's internal cookiejar assertion errors and stripping extension junk."""
    try:
        with open('cookies.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        with open('clean_cookies.txt', 'w', encoding='utf-8') as f:
            f.write("# Netscape HTTP Cookie File\n\n")
            for line in lines:
                if line.startswith('#') or not line.strip():
                    continue
                
                parts = line.strip('\n').split('\t')
                
                # Valid Netscape format always has exactly 7 columns
                if len(parts) == 7:
                    # 1. Strip out ANY cookie belonging to a third-party extension
                    cookie_name = parts[5]
                    if 'goodTube' in cookie_name or 'ext_name' in cookie_name or 'ext_id' in cookie_name:
                        continue
                        
                    # 2. Fix the Python http.cookiejar AssertionError!
                    # If the domain (Column 0) starts with a dot, Column 1 MUST be TRUE. 
                    # If it doesn't, Column 1 MUST be FALSE.
                    if parts[0].startswith('.'):
                        parts[1] = 'TRUE'
                    else:
                        parts[1] = 'FALSE'
                        
                    # Write the perfectly clean, mathematically valid line
                    f.write('\t'.join(parts) + '\n')
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
            # 2. yt-dlp Extraction logic
            ydl_opts = {
                "format": "best[ext=mp4]/best",
                "quiet": True,
                "noplaylist": True,
                "cookiefile": "clean_cookies.txt", 
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