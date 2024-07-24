import os
import random
from datetime import datetime
from moviepy.editor import *
import moviepy.video.fx.all as vfx
import moviepy.video.fx.crop as crop_vid
from gtts import gTTS
import assemblyai as aai
import pysrt
import praw
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google.auth.transport.requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_current_datetime():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def fetch_reddit_post():
    reddit = praw.Reddit(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        user_agent=os.getenv('USER_AGENT'),
    )
    subreddit = reddit.subreddit('AmItheAsshole')
    post = next(subreddit.new(limit=1))
    return post.title, post.selftext

def generate_speech(content, output_path):
    speech = gTTS(text=content, lang='en', slow=False)
    speech.save(output_path)
    return output_path

def edit_video(audio_path, video_path, output_path):
    audio_clip = AudioFileClip(audio_path).fx(vfx.speedx, 1)
    start_point = random.randint(1, 480)
    video_clip = VideoFileClip("minecraft.mp4").subclip(start_point, start_point + audio_clip.duration + 1.3)
    final_clip = video_clip.set_audio(audio_clip)

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

    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
    return output_path

def transcribe_video(video_path, srt_output_path):
    aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(video_path)
    srt = transcript.export_subtitles_srt()

    with open(srt_output_path, "w") as f:
        f.write(srt)
    return srt_output_path

def add_subtitles_to_video(video_path, srt_path, output_path):
    video = VideoFileClip(video_path)
    subtitles = pysrt.open(srt_path)

    subtitle_clips = []
    for subtitle in subtitles:
        start_time = subtitle.start.hours * 3600 + subtitle.start.minutes * 60 + subtitle.start.seconds + subtitle.start.milliseconds / 1000
        end_time = subtitle.end.hours * 3600 + subtitle.end.minutes * 60 + subtitle.end.seconds + subtitle.end.milliseconds / 1000
        text_clip = TextClip(subtitle.text, fontsize=36, font='Arial', color='black', bg_color='white', size=(video.size[0]*3/4, None), method='caption')
        text_clip = text_clip.set_start(start_time).set_duration(end_time - start_time)
        text_clip = text_clip.set_position(('center', 'center'))
        subtitle_clips.append(text_clip)

    final_video = CompositeVideoClip([video] + subtitle_clips)
    final_video.write_videofile(output_path, codec='libx264', remove_temp=True)
    return output_path

def shorten_video_if_needed(video_path, max_duration=58):
    video_clip = VideoFileClip(video_path)
    if video_clip.duration > max_duration:
        final_short_clip = video_clip.subclip(0, max_duration)
        final_short_path = video_path.replace(".mp4", "_short.mp4")
        final_short_clip.write_videofile(final_short_path, codec='libx264', remove_temp=True)
        final_short_clip.close()
        return final_short_path
    video_clip.close()
    return video_path

def get_authenticated_service():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "secret.json"
    credentials_file = 'credentials.json'

    credentials = None
    if os.path.exists(credentials_file):
        with open(credentials_file, 'r') as file:
            credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(json.load(file), scopes=["https://www.googleapis.com/auth/youtube.upload"])

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes=["https://www.googleapis.com/auth/youtube.upload"])
            credentials = flow.run_local_server(port=0)

        with open(credentials_file, 'w') as file:
            file.write(credentials.to_json())

    return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

def upload_to_youtube(video_path, title, description):
    youtube = get_authenticated_service()
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": description,
                "title": title,
                "defaultLanguage": "en",
            },
            "status": {
                "privacyStatus": "public",
                "madeForKids": False
            }
        },
        media_body=googleapiclient.http.MediaFileUpload(video_path)
    )
    response = request.execute()
    return response
