import praw

reddit = praw.Reddit(
    client_id='pv_iMAfGPgH_QQTtmXrjWg',
    client_secret='ign69Nww_VXwEbQhpgG_g_UXUOFJOA',
    user_agent='script:reddit.aita.extractor:v1.0 (by /u/JD)',
)

# Access the AITA subreddit
subreddit = reddit.subreddit('AmItheAsshole')

# Fetch recent posts
for submission in subreddit.new(limit=1):
    print("Content:", submission.selftext)  # Print the content of the post
    print("\n---\n")

