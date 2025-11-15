# app.py
import streamlit as st
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo

st.set_page_config(page_title="감성 날짜 페이지", page_icon="♡", layout="centered")

# --- 귀여운 카오모지 배경 프리셋 ---
BACKGROUND_STYLES = {
    "🌸 핑크 하트 패턴 ( : ̗̀ ♡ˎˊ: )": """
        background: linear-gradient(180deg, #FFE5EF, #FFD3E6);
        background-image: radial-gradient(#FFAAC9 1px, transparent 1px),
                          radial-gradient(#FFC8DE 1px, transparent 1px);
        background-size: 18px 18px;
        background-position: 0 0, 9px 9px;
    """,

    "✨ 은은한 별빛 패턴 (✧ ⋆｡°)": """
        background: linear-gradient(180deg, #FAF6FF, #F3EDFF);
        background-image: radial-gradient(#D5C2FF 1px, transparent 1px),
                          radial-gradient(#E6D9FF 1px, transparent 1px);
        background-size: 22px 22px;
        background-position: 0 0, 11px 11px;
    """,

    "🩵 하늘색 포근 패턴 (₊˚⊹♡)": """
        background: linear-gradient(180deg, #E9F6FF, #D9EEFF);
        background-image: radial-gradient(#AEE1FF 1px, transparent 1px),
                          radial-gradient(#BEEAFF 1px, transparent 1px);
        background-size: 20px 20px;
        background-position: 0 0, 10px 10px;
    """
}

# --- 사용자 선택 ---
st.sidebar.header("🎀 배경 스타일 선택")
selected_bg = st.sidebar.selectbox("배경 테마", list(BACKGROUND_STYLES.keys()))

# --- 스타일 적용 ---
st.markdown(f"""
<style>
    .main {{
        {BACKGROUND_STYLES[selected_bg]}
        background-attachment: fixed;
    }}

    .title {{
        text-align: center;
        font-size: 42px;
        font-weight: 900;
        color: #FF4FA0;
        text-shadow: 0 3px 6px rgba(255,0,120,0.15);
        margin-top: 10px;
    }}

    .card {{
        background: #FFFFFFDD;
        padding: 22px;
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(255, 150, 190, 0.2);
        border: 2px solid #FFB3D6;
        margin-bottom: 20px;
    }}

    .stButton>button {{
        background-color: #FF8AC7 !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 8px 14px !important;
    }}
</style>
""", unsafe_allow_html=True)


# --- 날짜 기능 ---
WEEKDAY_KOR = ["월요일","화요일","수요일","목요일","금요일","토요일","일요일"]

def now_in_tz(tz):
    return datetime.now(ZoneInfo(tz))

def fmt_datetime(dt):
    wk = WEEKDAY_KOR[dt.weekday()]
    return f"{dt.year}년 {dt.month}월 {dt.day}일 ({wk})  {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"

def fmt_date(d):
    wk = WEEKDAY_KOR[d.weekday()]
    return f"{d.year}년 {d.month}월 {d.day}일 ({wk})"


# --- 메인 UI ---
st.markdown("<h1 class='title'>: ̗̀ ♡ˎˊ:  감성 날짜 페이지  : ̗̀ ♡ˎˊ:</h1>", unsafe_allow_html=True)

now = now_in_tz("Asia/Seoul")

# 카드 1 — 현재 시간
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("⏰ 현재 시간")
st.write(f"**{fmt_datetime(now)}**")
st.markdown("</div>", unsafe_allow_html=True)

# 카드 2 — 날짜 선택
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📅 날짜 선택")

selected = st.date_input("날짜를 선택하세요", now.date())

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

st.write(f"선택된 날짜: **{fmt_date(selected)}**")
st.markdown("</div>", unsafe_allow_html=True)
