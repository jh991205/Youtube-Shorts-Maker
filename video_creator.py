from moviepy.editor import *
import moviepy.video.fx.all as vfx
import moviepy.video.fx.crop as crop_vid
import random, os
from gtts import gTTS
from dotenv import load_dotenv
import assemblyai as aai
import pysrt
from pydub import AudioSegment
from datetime import datetime
import praw

# Load environment variables
load_dotenv()

# Initialize directories
if not os.path.exists('generated'):
    os.mkdir('generated')

# Get the current date-time for file naming
now = datetime.now()
formatted_now = "2"  # This format removes spaces and colons

reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent=os.getenv('USER_AGENT'),
)

# Access the AITA subreddit
subreddit = reddit.subreddit('AmItheAsshole')

# Fetch the most recent post
post = next(subreddit.new(limit=1))

# Extract title and content from the post
title = post.title
content = post.selftext

# Print the title and content
print("Title:", title)
print("Content:", content)
# Generate speech from text
speech = gTTS(text=content, lang='en', slow=False)
speech_path = "generated/speech.mp3"
speech.save(speech_path)

# Load audio with moviepy and speed up
audio_clip = AudioFileClip(speech_path)
audio_clip = audio_clip.fx(vfx.speedx, 1)

# Export the modified audio
modified_speech_path = "generated/" + formatted_now + "_speech_fast.mp3"
audio_clip.write_audiofile(modified_speech_path)

# Video editing
start_point = random.randint(1, 480)
video_clip = VideoFileClip("minecraft.mp4").subclip(start_point, start_point + audio_clip.duration + 1.3)
final_clip = video_clip.set_audio(audio_clip)

# Resize the video to 9:16 ratio
w, h = final_clip.size
target_ratio = 1080 / 1920
current_ratio = w / h

if current_ratio > target_ratio:
    new_width = int(h * target_ratio)
    x_center = w / 2
    final_clip = crop_vid.crop(final_clip, width=new_width, height=h, x_center=x_center)
else:
    new_height = int(w / target_ratio)
    y_center = h / 2
    final_clip = crop_vid.crop(final_clip, width=w, height=new_height, y_center=y_center)

# Save the intermediate video file
intermediate_video_path = "generated/intermediate.mp4"
final_clip.write_videofile(intermediate_video_path, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)

# Transcription and subtitle generation
aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
transcriber = aai.Transcriber()
transcript = transcriber.transcribe(intermediate_video_path)
srt = transcript.export_subtitles_srt()

# Save the subtitles to a file
srt_path = "generated/" + formatted_now + ".srt"
with open(srt_path, "w") as f:
    f.write(srt)

# Burn subtitles into the video
video = VideoFileClip(intermediate_video_path)
subtitles = pysrt.open(srt_path)

# Create subtitle clips and composite video
subtitle_clips = []
for subtitle in subtitles:
    start_time = subtitle.start.hours * 3600 + subtitle.start.minutes * 60 + subtitle.start.seconds + subtitle.start.milliseconds / 1000
    end_time = subtitle.end.hours * 3600 + subtitle.end.minutes * 60 + subtitle.end.seconds + subtitle.end.milliseconds / 1000
    text_clip = TextClip(subtitle.text, fontsize=36, font='Arial', color='black', bg_color='white',
                         size=(video.size[0]*3/4, None), method='caption')
    text_clip = text_clip.set_start(start_time).set_duration(end_time - start_time)
    text_clip = text_clip.set_position(('center', 'center'))  # Centered horizontally and vertically
    subtitle_clips.append(text_clip)

final_video = CompositeVideoClip([video] + subtitle_clips)

# Write the final video with subtitles
final_video_path = "generated/final.mp4"
print(final_video_path)
final_video.write_videofile(final_video_path, codec='libx264', remove_temp=True)

# Cleanup intermediate files
os.remove(intermediate_video_path)
os.remove(modified_speech_path)
os.remove(srt_path)
os.remove(speech_path)

final_video_check = VideoFileClip(final_video_path)

if final_video_check.duration > 58:
    final_short_clip = final_video_check.subclip(0, 58)
    final_short_path = "generated/final_short.mp4"
    final_short_clip.write_videofile(final_short_path, codec='libx264', remove_temp=True)
    print("Shortened video created:", final_short_path)
else:
    print("No need to shorten the video.")

final_video_check.close()
final_video.close()
final_short_clip.close()