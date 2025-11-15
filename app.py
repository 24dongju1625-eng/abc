# app.py
import streamlit as st
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo

# ---------- 기본 설정 ----------
st.set_page_config(page_title="날짜 알려주는 앱", page_icon="📅", layout="wide")

WEEKDAY_KOR = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

# ---------- 스타일(디자인 업그레이드) ----------
st.markdown(
    """
    <style>
        /* 전체 배경 */
        .main {
            background: #f8f9fc;
        }

        /* 카드 스타일 */
        .card {
            background: white;
            padding: 25px 30px;
            border-radius: 15px;
            box-shadow: 0 0 15px rgba(0,0,0,0.08);
            margin-bottom: 25px;
        }

        /* 제목 스타일 */
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: 800;
            color: #2b4eff;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #555;
            margin-bottom: 25px;
        }

        /* 구분선 스타일 */
        hr {
            border: 0;
            height: 1px;
            background: #d0d7e6;
            margin: 20px 0;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------- 유틸 ----------
def now_in_tz(tz_name: str) -> datetime:
    tz = ZoneInfo(tz_name)
    return datetime.now(tz)

def format_korean(dt: datetime) -> str:
    wk = WEEKDAY_KOR[dt.weekday()]
    return f"{dt.year}년 {dt.month}월 {dt.day}일 ({wk}) {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"

def format_date_korean(d: date) -> str:
    wk = WEEKDAY_KOR[d.weekday()]
    return f"{d.year}년 {d.month}월 {d.day}일 ({wk})"

def diff_days(from_date: date, to_date: date) -> int:
    return (to_date - from_date).days


# ---------- UI ----------
st.markdown("<h1 class='title'>📅 날짜 알려주는 페이지</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>날짜, 요일, D-Day를 깔끔하게 확인하세요!</p>", unsafe_allow_html=True)

# 사이드바
st.sidebar.header("⚙️ 설정")
tz_choice = st.sidebar.selectbox("시간대 선택", [
    "Asia/Seoul", "UTC", "Asia/Tokyo", "Europe/London", "America/New_York"
], index=0)

now = now_in_tz(tz_choice)

# -------------------- 카드 1: 현재 시간 --------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("⏰ 현재 시간")
st.write(f"**{format_korean(now)}**")
st.caption(f"ISO 형식: `{now.isoformat()}`  •  Timezone: `{tz_choice}`")
st.markdown("</div>", unsafe_allow_html=True)

# -------------------- 카드 2: 날짜 선택 --------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📌 날짜 선택")

col1, col2 = st.columns([2, 1])
with col1:
    selected = st.date_input("날짜를 선택하세요", value=now.date())
with col2:
    if st.button("오늘"):
        selected = now.date()
    if st.button("내일"):
        selected = now.date() + timedelta(days=1)
    if st.button("어제"):
        selected = now.date() - timedelta(days=1)

st.write(f"**▶ 선택한 날짜:** {format_date_korean(selected)}")
st.write(f"ISO 형식: `{selected.isoformat()}`")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------- 카드 3: D-Day 계산 --------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📅 D-Day 계산")

days_until = diff_days(now.date(), selected)

if days_until == 0:
    st.success("오늘입니다! 🎉")
elif days_until > 0:
    st.info(f"⏳ **{days_until}일 남았습니다.**")
else:
    st.warning(f"📌 **{abs(days_until)}일 전** 날짜입니다.")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------- 카드 4: 기간 계산 --------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🗓️ 기간 계산")

start = st.date_input("시작일", value=now.date() - timedelta(days=7), key="start")
end = st.date_input("종료일", value=now.date(), key="end")

if end < start:
    st.error("🚫 종료일은 시작일 이후여야 합니다.")
else:
    length = diff_days(start, end) + 1
    st.write(f"📘 **총 {length}일**")
    st.caption(f"{start.isoformat()} → {end.isoformat()}")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------- 카드 5: 다운로드 --------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📥 날짜 정보 다운로드")

download_text = (
    f"현재시간: {now.isoformat()} ({tz_choice})\n"
    f"선택날짜: {selected.isoformat()} ({format_date_korean(selected)})\n"
    f"D-day: {days_until}\n"
)

st.download_button(
    "다운로드 (TXT)",
    data=download_text,
    file_name="date_info.txt",
    mime="text/plain"
)
st.markdown("</div>", unsafe_allow_html=True)
