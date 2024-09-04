import praw

reddit = praw.Reddit(
    client_id='',
    client_secret='',
    user_agent='',
)

# Access the AITA subreddit
subreddit = reddit.subreddit('AmItheAsshole')

# Fetch recent posts
for submission in subreddit.new(limit=1):
    print("Content:", submission.selftext)  # Print the content of the post
    print("\n---\n")

