
import streamlit as st
from gluort_crawler import crawl_gluort_posts
from gluort_emailer import send_email
from datetime import datetime

st.set_page_config(page_title="글루어트 인스타그램 키워드 알림봇", layout="centered")
st.title("📷 글루어트 인스타그램 키워드 알림봇")

st.write("어제부터 오늘까지 #글루어트 태그 게시물을 수집하고 이메일로 발송합니다.")

other_email = st.text_input("📬 같이 받을 사람 이메일 주소 (선택)", placeholder="예: teammate@company.com")
send_to_others = st.checkbox("⬜ 위 이메일에도 리포트 보내기")

if st.button("🔍 지금 크롤링 실행하기"):
    username = st.secrets["INSTAGRAM_USER"]
    password = st.secrets["INSTAGRAM_PASS"]
    from_email = st.secrets["EMAIL_ADDRESS"]
    email_pw = st.secrets["EMAIL_PASSWORD"]

    posts = crawl_gluort_posts(username, password)

    if posts:
        today = datetime.now().strftime('%Y.%m.%d')
        body = f"[글루어트 인스타 리포트] {today}\n\n"
        for p in posts:
            body += f"- {p['caption']}\n{p['link']}\n\n"

        subject = f"[글루어트] {today} 인스타 키워드 리포트"

        send_email(subject, body, "parkminji@drdiary.co.kr", from_email, email_pw)
        st.success("📩 민지님 메일로 발송 완료!")

        if send_to_others and other_email:
            send_email(subject, body, other_email, from_email, email_pw)
            st.info(f"📬 추가 수신자({other_email})에게도 발송 완료!")
    else:
        st.warning("❌ 어제~오늘 사이의 게시물이 없습니다.")
