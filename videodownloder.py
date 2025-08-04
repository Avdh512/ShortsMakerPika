# video_downloader.py

import os
import pandas as pd
import yt_dlp

# CONFIG
INPUT_CSV = r".\tag_search_results.csv"
DOWNLOAD_FOLDER = "downloads"

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " -_").strip()

def download_video(url, filename, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_file = os.path.join(output_path, f"{filename}.%(ext)s")
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',
        'outtmpl': output_file,
        'merge_output_format': 'mp4',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print(f"✅ Downloaded: {filename}")
        except Exception as e:
            print(f"❌ Failed: {filename} - {e}")

def main():
    df = pd.read_csv(INPUT_CSV)
    for idx, row in df.iterrows():
        tag = sanitize_filename(row['search_tag'])[:20]
        title = sanitize_filename(row['title'])[:30]
        filename = f"{tag}_{title}"
        url = row['url']
        print(f"⬇️  [{idx+1}/{len(df)}] Downloading: {filename}")
        download_video(url, filename, DOWNLOAD_FOLDER)

if __name__ == "__main__":
    main()
