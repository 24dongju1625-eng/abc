# app.py
import streamlit as st
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo

st.set_page_config(page_title="날짜 알려주기", page_icon="📅", layout="centered")

# -------------------- 감성 배경 테마 -------------------------
BACKGROUND_STYLES = {
    "🌸 핑크 하트 ( : ̗̀ ♡ˎˊ: )": {
        "bg": """
            background: linear-gradient(180deg, #FFE5EF, #FFD3E6);
            background-image: radial-gradient(#FFAAC9 1px, transparent 1px),
                              radial-gradient(#FFC8DE 1px, transparent 1px);
            background-size: 18px 18px;
            background-position: 0 0, 9px 9px;
        """,
        "button_bg": "#FF8AC7",
        "button_text": "#FFFFFF",
        "card_bg": "#FFFFFFDD",
        "card_border": "#FFB3D6",
        "title_color": "#FF4FA0",
        "text_color": "#FF4FA0"
    },

    "✨ 보랏빛 별빛 (✧ ⋆｡°)": {
        "bg": """
            background: linear-gradient(180deg, #F8F3FF, #EDE4FF);
            background-image: radial-gradient(#D6C6FF 1px, transparent 1px),
                              radial-gradient(#E8DDFF 1px, transparent 1px);
            background-size: 22px 22px;
            background-position: 0 0, 11px 11px;
        """,
        "button_bg": "#D9A6FF",
        "button_text": "#FFFFFF",
        "card_bg": "#FFFFFFDD",
        "card_border": "#D1A9FF",
        "title_color": "#A573D7",
        "text_color": "#A573D7"
    },

    "🩵 하늘 파스텔 (₊˚⊹♡)": {
        "bg": """
            background: linear-gradient(180deg, #EAF7FF, #D8EFFF);
            background-image: radial-gradient(#BFE8FF 1px, transparent 1px),
                              radial-gradient(#D2F1FF 1px, transparent 1px);
            background-size: 20px 20px;
            background-position: 0 0, 10px 10px;
        """,
        "button_bg": "#7EC8FF",
        "button_text": "#FFFFFF",
        "card_bg": "#FFFFFFEE",
        "card_border": "#A1D5FF",
        "title_color": "#6EC9F1",
        "text_color": "#6EC9F1"
    }
}

# -------------------- 사이드바 -------------------------
st.sidebar.header("🎀 배경 테마")
selected_bg = st.sidebar.selectbox("테마 선택", list(BACKGROUND_STYLES.keys()))

# -------------------- CSS 적용 (배경 + UI 색상 전체 적용) -------------------------
style = BACKGROUND_STYLES[selected_bg]

st.markdown(f"""
<style>
    html, body, .main, .stApp, .appview-container {{
        {style['bg']}
        background-attachment: fixed;
    }}

    .title {{
        text-align: center;
        font-size: 38px;
        font-weight: 900;
        color: {style['title_color']};
        margin-top: 5px;
        text-shadow: 0 3px 6px rgba(255, 0, 120, 0.2);
    }}

    .card {{
        background: {style['card_bg']};
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 6px 14px rgba(255, 140, 180, 0.25);
        border: 2px solid {style['card_border']};
        margin-bottom: 20px;
    }}

    .stButton>button {{
        background-color: {style['button_bg']} !important;
        color: {style['button_text']} !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 8px 14px !important;
    }}

    .stMarkdown {{
        color: {style['text_color']} !important;
    }}
</style>
""", unsafe_allow_html=True)

# -------------------- 날짜 함수들 -------------------------
WEEKDAY_KOR = ["월요일","화요일","수요일","목요일","금요일","토요일","일요일"]

def now_in_tz(tz):
    return datetime.now(ZoneInfo(tz))

def fmt_datetime(dt):
    wk = WEEKDAY_KOR[dt.weekday()]
    return f"{dt.year}년 {dt.month}월 {dt.day}일 ({wk})  {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"

def fmt_date(d):
    wk = WEEKDAY_KOR[d.weekday()]
    return f"{d.year}년 {d.month}월 {d.day}일 ({wk})"

def day_diff(from_d, to_d):
    return (to_d - from_d).days

# -------------------- 제목 -------------------------
st.markdown("<h1 class='title'>날짜 알려주기</h1>", unsafe_allow_html=True)

now = now_in_tz("Asia/Seoul")

# -------------------- 현재 시간 -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("⏰ 현재 시간")
st.write(f"**{fmt_datetime(now)}**")
st.write(f"ISO: `{now.isoformat()}`")
st.markdown("</div>", unsafe_allow_html=True)

# -------------------- 날짜 선택 -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📅 날짜 선택")

selected = st.date_input("날짜 선택", now.date())

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("오늘"):
        selected = now.date()
with col2:
    if st.button("내일"):
        selected = now.date() + timedelta(days=1)
with col3:
    if st.button("어제"):
        selected = now.date() - timedelta(days=1)

st.write(f"선택한 날짜: **{fmt_date(selected)}**")
st.markdown("</div>", unsafe_allow_html=True)

# -------------------- D-day -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📌 D-Day 계산")

diff = day_diff(now.date(), selected)

if diff == 0:
    st.success("오늘입니다! ✿")
elif diff > 0:
    st.info(f"⏳ **{diff}일 남음**")
else:
    st.warning(f"📍 **{abs(diff)}일 지남**")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------- 구간 계산 -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🗓 기간 계산")

start = st.date_input("시작일", now.date() - timedelta(days=7))
end = st.date_input("종료일", now.date())

if end < start:
    st.error("❌ 종료일이 시작일보다 더 빠릅니다!")
else:
    length = (end - start).days + 1
    st.write(f"총 기간: **{length}일**")
st.markdown("</div>", unsafe_allow_html=True)

# -------------------- 다운로드 -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📥 날짜 정보 다운로드")

download_text = (
    f"현재시간: {fmt_datetime(now)}\n"
    f"선택한 날짜: {fmt_date(selected)}\n"
    f"D-day: {diff}\n"
)

st.download_button(
    "TXT 다운로드",
    data=download_text,
    file_name="date_info.txt",
    mime="text/plain"
)
st.markdown("</div>", unsafe_allow_html=True)
