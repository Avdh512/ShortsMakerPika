import os
import uuid
import math
import pandas as pd
from moviepy.editor import VideoFileClip
import yt_dlp

# CONFIG
INPUT_CSV = r".\url scrape\tag_search_results.csv"
OUTPUT_BASE_FOLDER = r"C:\Users\avdhesh\Desktop\VideoGenerator\Shortsmaker\shorts"
CLIP_LENGTH = 35  # seconds
DOWNLOAD_FOLDER = "downloads"

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " -_").strip()

def download_video(url, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_file = os.path.join(output_path, "original.%(ext)s")
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',
        'outtmpl': output_file,
        'merge_output_format': 'mp4',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(f"❌ Error downloading {url}: {e}")
            return None

    for file in os.listdir(output_path):
        if file.startswith("original") and file.endswith(".mp4"):
            return os.path.join(output_path, file)
    return None

def process_video(file_path, output_path, clip_length=CLIP_LENGTH):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    video = VideoFileClip(file_path)
    duration = int(video.duration)
    num_clips = math.ceil(duration / clip_length)

    for i in range(num_clips):
        start = i * clip_length
        end = min(start + clip_length, duration)
        clip = video.subclip(start, end)

        # Resize and pad to 1080x1920
        resized = clip.resize(height=1920 if clip.w > clip.h else 1080)
        final_clip = resized.on_color(
            size=(1080, 1920),
            color=(0, 0, 0),
            pos=("center", "center")
        )

        output_file = os.path.join(output_path, f"short_{i+1}_{uuid.uuid4().hex[:6]}.mp4")
        final_clip.write_videofile(
            output_file,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=4,
            verbose=False,
            logger=None
        )

    print(f"✅ Processed {num_clips} clips to {output_path}")

def main():
    df = pd.read_csv(INPUT_CSV)
    for idx, row in df.iterrows():
        tag = sanitize_filename(row['search_tag'])
        title = sanitize_filename(row['title'])[:50]
        url = row['url']
        print(f"\n🎬 Processing [{idx+1}/{len(df)}]: {title} ({tag})")

        folder_name = f"{tag}_{title}"
        output_folder = os.path.join(OUTPUT_BASE_FOLDER, folder_name)
        download_path = os.path.join(DOWNLOAD_FOLDER, folder_name)

        video_path = download_video(url, download_path)
        if video_path:
            process_video(video_path, output_folder)
        else:
            print(f"⚠️ Skipped {title} due to download failure.")

if __name__ == "__main__":
    main()
