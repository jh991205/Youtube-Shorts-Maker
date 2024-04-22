import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", scopes)
    credentials = flow.run_console()

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",  # "22" is for People & Blogs, choose as appropriate
                "description": "Here's a new YouTube Short!",
                "title": "My First Short",
                "tags": ["shorts", "example", "demo"]  # Tags help with discoverability
            },
            "status": {
                "privacyStatus": "public"  # Shorts are usually public for maximum reach
            }
        },

        media_body=googleapiclient.http.MediaFileUpload("short_video.mp4", resumable=True)
    )
    response = request.execute()

    print("Uploaded Short's ID:", response['id'])
    print(response)

if __name__ == "__main__":
    main()
