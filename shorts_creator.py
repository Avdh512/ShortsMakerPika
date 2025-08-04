import os
import uuid
import math
from moviepy.editor import VideoFileClip

# CONFIG
DOWNLOAD_FOLDER = "./downloads"
OUTPUT_FOLDER = "./shorts"
CLIP_LENGTH = 35  # seconds

def process_video(file_path, output_path, clip_length=CLIP_LENGTH):
    filename_base = os.path.splitext(os.path.basename(file_path))[0]

    try:
        video = VideoFileClip(file_path)
    except Exception as e:
        print(f"❌ Could not open {file_path}: {e}")
        return

    duration = int(video.duration)
    num_clips = math.ceil(duration / clip_length)

    for i in range(num_clips):
        start = i * clip_length
        end = min(start + clip_length, duration)
        clip = video.subclip(start, end)

        # Resize and pad to vertical 1080x1920
        resized = clip.resize(height=1920 if clip.w > clip.h else 1080)
        final_clip = resized.on_color(
            size=(1080, 1920),
            color=(0, 0, 0),
            pos=("center", "center")
        )

        output_file = os.path.join(
            output_path,
            f"{filename_base}_part{i+1}_{uuid.uuid4().hex[:6]}.mp4"
        )

        try:
            print(f"🎞️  Writing clip {i+1}/{num_clips} for {filename_base}...")
            final_clip.write_videofile(
                output_file,
                codec="libx264",
                audio_codec="aac",
                preset="ultrafast",
                threads=4,
                verbose=True,
                logger='bar'
            )
        except Exception as e:
            print(f"⚠️ Failed to write clip {i+1}: {e}")

    print(f"✅ Done: {filename_base} -> {num_clips} clips")

def main():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    for file in os.listdir(DOWNLOAD_FOLDER):
        if file.endswith(".mp4"):
            file_path = os.path.join(DOWNLOAD_FOLDER, file)
            process_video(file_path, OUTPUT_FOLDER)

if __name__ == "__main__":
    main()
