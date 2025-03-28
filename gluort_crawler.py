
import instaloader
from datetime import datetime, timedelta

def crawl_gluort_posts(username, password):
    L = instaloader.Instaloader()
    L.login(username, password)

    yesterday = datetime.now() - timedelta(days=1)
    today = datetime.now()

    posts_data = []

    for post in instaloader.Hashtag.from_name(L.context, "글루어트").get_posts():
        post_date = post.date_local
        if yesterday.date() <= post_date.date() < today.date():
            caption = post.caption if post.caption else "(캡션 없음)"
            link = f"https://www.instagram.com/p/{post.shortcode}/"
            posts_data.append({
                "caption": caption.strip(),
                "link": link,
                "date": post_date.strftime("%Y-%m-%d %H:%M")
            })
        elif post_date.date() < yesterday.date():
            break  # 너무 과거로 가지 않도록 중단

    return posts_data
