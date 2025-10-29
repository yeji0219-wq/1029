import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from urllib.parse import quote

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="증상 체커 v5.1", page_icon="💊", layout="centered")

# 세션 상태 초기화
if "health_data" not in st.session_state:
    st.session_state["health_data"] = pd.DataFrame(columns=["날짜", "혈압", "혈당"])

# -----------------------------
# 제목
# -----------------------------
st.markdown(
    """
    <h1 style='text-align:center;color:#2E86C1;'>💊 증상 체커 v5.1</h1>
    <p style='text-align:center;color:#117A65;'>누구나 쉽게 증상을 확인하고 건강을 관리할 수 있도록</p>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# 건강 모니터링
# -----------------------------
st.header("🩺 건강 모니터링")
with st.expander("혈압·혈당 기록하기", expanded=True):
    bp = st.number_input("혈압 (mmHg)", min_value=60, max_value=200, step=1, key="bp")
    sugar = st.number_input("혈당 (mg/dL)", min_value=50, max_value=400, step=1, key="sugar")
    if st.button("📈 기록 저장"):
        new_entry = pd.DataFrame({
            "날짜": [datetime.now().strftime("%Y-%m-%d %H:%M")],
            "혈압": [bp],
            "혈당": [sugar]
        })
        st.session_state["health_data"] = pd.concat(
            [st.session_state["health_data"], new_entry], ignore_index=True
        )
        st.success("✅ 기록이 저장되었습니다.")

if not st.session_state["health_data"].empty:
    st.subheader("📊 내 건강 추세")
    st.line_chart(st.session_state["health_data"].set_index("날짜")[["혈압", "혈당"]])
    st.caption("최근 측정 추세를 확인해보세요.")

# -----------------------------
# 증상 입력
# -----------------------------
st.header("🤒 증상 입력")
symptoms = st.multiselect(
    "현재 느끼는 증상을 선택하세요:",
    ["기침", "발열", "두통", "피로감", "목 통증", "복통", "구토", "콧물", "근육통", "호흡곤란", "의식 저하"],
)

# -----------------------------
# 규칙 기반 진단
# -----------------------------
def diagnose(symptoms):
    rules = {
        "감기": ["기침", "콧물", "목 통증", "발열"],
        "독감": ["발열", "기침", "근육통", "피로감"],
        "소화불량": ["복통", "구토"],
        "편두통": ["두통", "피로감"],
        "호흡기 질환": ["기침", "호흡곤란"],
    }
    severe = ["호흡곤란", "의식 저하", "고열 지속"]

    possible = [d for d, rule in rules.items() if sum(s in symptoms for s in rule) >= 2]
    is_severe = any(s in symptoms for s in severe)

    return (possible if possible else ["판단 어려움"]), is_severe


if st.button("🔍 진단하기"):
    result, severe = diagnose(symptoms)
    st.success(f"💊 가능한 질환: {', '.join(result)}")

    if severe:
        st.error("🚨 심각한 증상이 감지되었습니다. 즉시 병원 방문을 권장합니다.")
    else:
        st.info("💡 증상이 경미하다면 충분한 휴식과 수분 섭취를 하세요.")

# -----------------------------
# 문자 알림 시스템 (시뮬레이션)
# -----------------------------
st.header("📱 보호자 문자 알림")
st.write("심각한 증상 발생 시 보호자에게 도움을 요청할 수 있습니다.")
guardian_number = st.text_input("보호자 전화번호 (예: 010-1234-5678)")
alert_msg = st.text_area("보낼 메시지", "현재 건강 상태가 좋지 않아 도움을 요청합니다.")

if st.button("📤 문자 전송 시뮬레이션"):
    if guardian_number:
        st.success(f"📨 {guardian_number} 에 메시지가 전송되었습니다 (시뮬레이션).")
    else:
        st.warning("전화번호를 입력해주세요.")

# -----------------------------
# 비의료 지원 연결
# -----------------------------
st.header("🤝 비의료 지원 연결")
st.markdown(
    """
    건강 외에도 도움이 필요한 분들을 위한 지원 기관 정보입니다:

    - 🥣 **무료 급식소 안내:** [대한적십자사 무료급식 정보](https://www.redcross.or.kr/)
    - 🏘 **복지서비스:** [복지로 - 복지서비스 검색](https://www.bokjiro.go.kr/)
    - 🧠 **심리상담 지원:** 정신건강상담전화 ☎️ 1577-0199  
    - 💬 **청소년 상담:** ☎️ 1388 (24시간)  
    - 💼 **노인·저소득층 복지:** [보건복지부 복지정보](https://www.mohw.go.kr/)
    """
)

# -----------------------------
# 오프라인 모드: 데이터 다운로드
# -----------------------------
st.header("💾 내 건강 데이터 저장")
st.download_button(
    label="📥 CSV 파일로 저장",
    data=st.session_state["health_data"].to_csv(index=False).encode("utf-8"),
    file_name="health_data.csv",
    mime="text/csv",
)

st.markdown("---")
st.caption("© 2025 증상 체커 v5.1 | 모두를 위한 건강 동반자 플랫폼")
