import praw
import json
import time
import datetime

# Reddit API Credentials
CLIENT_ID = ""
CLIENT_SECRET = ""
USER_AGENT = ""

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

SUBREDDIT_NAME = "machinelearning"
subreddit = reddit.subreddit(SUBREDDIT_NAME)

# Calculate timestamp for last 3 months
current_time = datetime.datetime.utcnow()
three_months_ago = current_time - datetime.timedelta(days=90)
three_months_utc = int(three_months_ago.timestamp())

# Fetch posts from r/machinelearning
posts_data = []

for post in subreddit.new(limit=1000):
    if post.created_utc >= three_months_utc:
        post_info = {
            "id": post.id,
            "title": post.title,
            "selftext": post.selftext,
            "url": post.url,
            "created_utc": post.created_utc,
            "score": post.score,
            "num_comments": post.num_comments,
            "comments": []
        }

        # Fetch comments
        post.comments.replace_more(limit=0)
        for comment in post.comments.list():
            post_info["comments"].append({
                "id": comment.id,
                "author": str(comment.author),
                "body": comment.body,
                "score": comment.score,
                "created_utc": comment.created_utc
            })

        print(post_info)
        posts_data.append(post_info)
        time.sleep(1)


with open("../data/reddit_data.json", "w", encoding="utf-8") as f:
    json.dump(posts_data, f, indent=4)


print(f"✅ Collected {len(posts_data)} posts from r/{SUBREDDIT_NAME}!")


