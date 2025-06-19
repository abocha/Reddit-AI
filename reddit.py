import praw

# --- For CLI ---
# import os
# from dotenv import load_dotenv
# load_dotenv()

# CLIENT_ID = os.getenv("CLIENT_ID")
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# USER_AGENT = "ReddditAI:v0.1 (by u/TheCarBun)"
# ----------------

import streamlit as st

CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
USER_AGENT = "ReddditAI:v0.1 (by u/TheCarBun)"

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

if reddit.read_only:
    print(">> Reddit API running in read-only mode.")


def get_subreddit_posts(subreddit_name, limit=10, sort_by='hot'):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    if sort_by == 'hot':
        submissions = subreddit.hot(limit=limit)
    elif sort_by == 'new':
        submissions = subreddit.new(limit=limit)
    elif sort_by == 'top':
        submissions = subreddit.top(limit=limit)
    elif sort_by == 'controversial':
        submissions = subreddit.controversial(limit=limit)
    elif sort_by == 'rising':
        submissions = subreddit.rising(limit=limit)
    else:
        print(f"Warning: Invalid sort_by '{sort_by}'. Defaulting to 'hot'.")
        submissions = subreddit.hot(limit=limit)

    for submission in submissions:
        posts.append({
            "id": submission.id,
            "title": submission.title,
            "score": submission.score,
            "num_comments": submission.num_comments,
            "url": submission.url,
            "author": submission.author.name if submission.author else "deleted",
            "created_utc": submission.created_utc,
            "selftext": submission.selftext if submission.is_self else "",  # Body of text posts
            "is_original_content": submission.is_original_content,
            "over_18": submission.over_18,
            "stickied": submission.stickied,
            "link_flair_text": submission.link_flair_text,
            "upvote_ratio": submission.upvote_ratio
        })

    return posts


def get_post_comments(submission_id: str, limit=0):
    """Fetches comments for a given Reddit post ID

    Args:
        submission_id (str): submission ID or the Reddit post
        limit (int, optional): _description_. Defaults to 0. `limit=None` tries to get all. `limit=0` removes them (only top-level without replies)

    Returns:
        _type_: _description_
    """
    print(">> Fetching comments for submission ID: ", submission_id)

    try:
        print(">> Trying using ID")
        submission = reddit.submission(id=submission_id)
        print(">> Worked using ID")
    except Exception as e:
        print(">> Didn't work")
        print(f">> Error fetching submission for {submission_id}: {e}")

    comments_data = []

    # limit=None tries to get all. limit=0 removes them (only top-level without replies)
    submission.comments.replace_more(limit)

    for comment in submission.comments.list():
        if comment.author is None and comment.body is None:
            continue

        comments_data.append({
            "comment_id": comment.id,
            "submission_id": submission.id,
            "author": comment.author.name if comment.author else "[deleted]",
            "body": comment.body,
            "score": comment.score,
            "created_utc": comment.created_utc,
            "parent_id": comment.parent_id,
            "is_submitter": comment.is_submitter,
            "depth": comment.depth
        })
    print(">> Returning Comment Data")
    return comments_data


def main():
    # subreddit_name = input("Enter subreddit name: ")
    # limit = int(input("Enter no. of posts to fetch: "))
    # sort_by = input(
    #     "Sort by (hot, new, top, controversial, rising): ").strip().lower()

    # posts = get_subreddit_posts(subreddit_name, limit, sort_by)
    # print(posts)
    # submission_id_or_url = input("Enter post ID or URL:")
    # limit = int(input("Enter no. of comments to fetch (0 for all): "))
    # comments = get_post_comments(
    #     submission_id_or_url, limit)
    # print(comments)
    print("RedditAI functions are ready to use..")


if __name__ == "__main__":
    main()
