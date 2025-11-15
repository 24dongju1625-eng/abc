# app.py
import streamlit as st
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo

st.set_page_config(page_title="리락쿠마 날짜 페이지", page_icon="🧸", layout="centered")

WEEKDAY_KOR = ["월요일","화요일","수요일","목요일","금요일","토요일","일요일"]

# ------- 스타일 (귀여운 테마) -------
st.markdown("""
<style>

    /* 전체 폰트 & 배경 */
    .main {
        background: #FFF6E9; /* 따뜻한 베이지톤 */
    }

    /* 카드 */
    .card {
        background: #FFFFFFEE;
        padding: 25px 30px;
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        border: 2px solid #FFD8A8;
    }

    /* 제목 */
    .title {
        text-align: center;
        font-size: 38px;
        font-weight: 900;
        color: #D87E4A;
        margin-top: -10px;
    }

    /* 부제 */
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #8B5A2B;
        margin-bottom: 20px;
    }

    /* 리락쿠마 이미지 꾸미기 */
    .rilakkuma-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 180px;
        border-radius: 20px;
        border: 3px solid #FFC48E;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

</style>
""", unsafe_allow_html=True)


# ------- 리락쿠마 이미지 업로드 -------
st.markdown("### 🧸 리락쿠마 이미지 업로드")
uploaded = st.file_uploader("리락쿠마 이미지를 업로드하세요 (png, jpg)", type=["png", "jpg"])

if uploaded:
    st.image(uploaded, caption="귀여운 리락쿠마 🧸", use_column_width=False)
else:
    st.info("리락쿠마 이미지를 올리면 상단에 예쁘게 표시돼요!")


# ------- 제목 -------
st.markdown("<h1 class='title'>🧸 날짜 알려주는 리락쿠마 페이지</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>귀여운 리락쿠마와 함께 날짜를 확인해요!</p>", unsafe_allow_html=True)


# ------- 유틸 -------
def now_in_tz(tz):
    tzinfo = ZoneInfo(tz)
    return datetime.now(tzinfo)

def fmt_datetime(dt):
    wk = WEEKDAY_KOR[dt.weekday()]
    return f"{dt.year}년 {dt.month}월 {dt.day}일 ({wk})  {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"

def fmt_date(d):
    wk = WEEKDAY_KOR[d.weekday()]
    return f"{d.year}년 {d.month}월 {d.day}일 ({wk})"

def diff(a,b):
    return (b - a).days


# ------- 사이드바 -------
st.sidebar.header("⚙️ 설정")
tz = st.sidebar.selectbox("시간대 선택", ["Asia/Seoul","UTC","Asia/Tokyo","Europe/London"], index=0)

now = now_in_tz(tz)


# ---------------- 카드 1 ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("⏰ 현재 시간")
st.write(f"**{fmt_datetime(now)}**")
st.caption(f"ISO: {now.isoformat()}  | timezone: {tz}")
st.markdown("</div>", unsafe_allow_html=True)


# ---------------- 카드 2 ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📅 날짜 선택")

col1, col2 = st.columns([2,1])
with col1:
    selected = st.date_input("날짜 선택", now.date())
with col2:
    if st.button("오늘"):
        selected = now.date()
    if st.button("내일"):
        selected = now.date() + timedelta(days=1)
    if st.button("어제"):
        selected = now.date() - timedelta(days=1)

st.write(f"선택한 날짜: **{fmt_date(selected)}**")
st.markdown("</div>", unsafe_allow_html=True)


# ---------------- 카드 3 ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📌 D-Day 계산")

d = diff(now.date(), selected)

if d == 0:
    st.success("🎉 오늘이에요!!")
elif d > 0:
    st.info(f"⏳ {d}일 남았어요!")
else:
    st.warning(f"📌 {abs(d)}일 지났어요!")

st.markdown("</div>", unsafe_allow_html=True)


# ---------------- 카드 4 ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📘 기간 계산")

s1 = st.date_input("시작일", now.date() - timedelta(days=7), key="s1")
s2 = st.date_input("종료일", now.date(), key="s2")

if s2 < s1:
    st.error("🚫 종료일은 시작일보다 이후여야 해요")
else:
    st.write(f"총 **{diff(s1,s2)+1}일**")
st.markdown("</div>", unsafe_allow_html=True)
