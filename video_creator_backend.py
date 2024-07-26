from fastapi import FastAPI
from pydantic import BaseModel
from utility import (
    fetch_reddit_post,
    generate_speech,
    edit_video,
    transcribe_video,
    add_subtitles_to_video,
    shorten_video_if_needed,
    upload_to_youtube,
    get_current_datetime
)

app = FastAPI()

class PostRequest(BaseModel):
    pass

@app.post("/process_video")
def process_video(request: PostRequest):
    title, content = fetch_reddit_post()
    print("Title:", title)
    print("Content:", content)

    formatted_now = get_current_datetime()

    speech_path = generate_speech(content, f"generated/speech_{formatted_now}.mp3")
    video_path = edit_video(speech_path, "minecraft.mp4", f"generated/intermediate_{formatted_now}.mp4")
    srt_path = transcribe_video(video_path, f"generated/{formatted_now}.srt")
    final_video_path = add_subtitles_to_video(video_path, srt_path, f"generated/final_{formatted_now}.mp4")
    final_short_path = shorten_video_if_needed(final_video_path)

    response = upload_to_youtube(final_short_path, title + " #shorts", f"{content} #aitah #aita #shorts")
    print(response)

    return {"message": "Video processing completed", "response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
