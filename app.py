# app.py
import streamlit as st

st.title("날짜 알려주는 페이지")
st.subheader("현재 날짜와 요일을 알려드립니다!.")
# app.py
import streamlit as st
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo

# ---------- 설정 ----------
DEFAULT_TZ = "Asia/Seoul"  # 사용자의 타임존 (요청에 따라 서울로 기본 설정)
WEEKDAY_KOR = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

st.set_page_config(page_title="날짜 알려주는 앱", page_icon="📅", layout="centered")

# ---------- 유틸 ----------
def now_in_tz(tz_name: str) -> datetime:
    tz = ZoneInfo(tz_name)
    return datetime.now(tz)

def format_korean(dt: datetime) -> str:
    # 예: 2025년 11월 15일 (토) 15:30:12
    wk = WEEKDAY_KOR[dt.weekday()]
    return f"{dt.year}년 {dt.month}월 {dt.day}일 ({wk}) {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"

def format_date_korean(d: date) -> str:
    wk = WEEKDAY_KOR[d.weekday()]
    return f"{d.year}년 {d.month}월 {d.day}일 ({wk})"

def diff_days(from_date: date, to_date: date) -> int:
    return (to_date - from_date).days

# ---------- UI ----------
st.title("📅 날짜 알려주는 홈페이지")
st.caption("현재 시간, 선택 날짜의 요일과 D-day(남은/지난 일수)를 확인할 수 있습니다.")

# 사이드바: 타임존 선택 (간단 목록 — 필요하면 더 추가)
st.sidebar.header("설정")
tz_choice = st.sidebar.selectbox("시간대 (timezone)", options=[
    "Asia/Seoul", "UTC", "Asia/Tokyo", "Europe/London", "America/New_York"
], index=0)

# 현재 시간 표시 (초 단위 업데이트는 서버 측이므로 실시간 초단위는 새로고침 필요)
now = now_in_tz(tz_choice)
st.subheader("현재 시간")
st.markdown(f"**{format_korean(now)}**")
st.write(f"표준표기: `{now.isoformat()}` (타임존: `{tz_choice}`)")

st.divider()

# 날짜 선택
st.subheader("날짜 선택")
col1, col2 = st.columns([2,1])
with col1:
    selected = st.date_input("원하는 날짜를 선택하세요", value=now.date())
with col2:
    # 빠른 버튼: 오늘 / 내일 / 어제
    if st.button("오늘"):
        selected = now.date()
    if st.button("내일"):
        selected = now.date() + timedelta(days=1)
    if st.button("어제"):
        selected = now.date() - timedelta(days=1)

# 선택 날짜 정보 출력
st.markdown("**선택한 날짜 정보**")
st.write(f"- 한국식 표기: **{format_date_korean(selected)}**")
st.write(f"- ISO 형식: `{selected.isoformat()}`")
st.write(f"- 요일 (숫자): `{selected.weekday()}` (0=월, 6=일)")

# D-day 계산 (선택 날짜 기준)
days_until = diff_days(now.date(), selected)
if days_until == 0:
    st.success("✅ 선택한 날짜는 **오늘** 입니다.")
elif days_until > 0:
    st.info(f"⏳ 선택한 날짜까지 **{days_until}일 남았습니다**.")
else:
    st.warning(f"📌 선택한 날짜는 **{abs(days_until)}일 전**입니다.")

st.divider()

# 범용 정보 / 추가 기능
st.subheader("추가 도구")
# 시작일/종료일을 골라 기간의 길이 보기
start = st.date_input("기간 시작일", value=now.date() - timedelta(days=7), key="start")
end = st.date_input("기간 종료일", value=now.date(), key="end")
if end < start:
    st.error("기간 종료일은 시작일 이후여야 합니다.")
else:
    length = diff_days(start, end) + 1
    st.write(f"- 선택한 기간 길이: **{length}일** ({start.isoformat()} → {end.isoformat()})")

# 날짜 텍스트로 다운로드 (간단한 파일로 제공)
downloa
