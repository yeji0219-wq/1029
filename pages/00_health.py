import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="증상 체커",
    page_icon="💊",
    layout="centered",
)

# -----------------------------
# UI 스타일
# -----------------------------
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #2E86C1;
            font-size: 38px;
            font-weight: bold;
        }
        .result-box {
            background-color: #E8F8F5;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 16px;
        }
        .warning-box {
            background-color: #FADBD8;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">💊 증상 체커</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;color:#117A65;">간단한 증상 입력으로 질환 가능성과 조치 방법을 확인하세요.</p>', unsafe_allow_html=True)

# -----------------------------
# 만성질환 선택
# -----------------------------
st.header("🏥 평소에 가지고 있는 질환이 있나요?")
chronic_conditions = st.multiselect(
    "해당되는 질환을 선택하세요 (없다면 비워두세요)",
    ["당뇨병", "고혈압", "천식", "심장질환"]
)

# -----------------------------
# 증상 입력
# -----------------------------
st.header("🤒 증상 입력")
symptoms = st.multiselect(
    "현재 느끼는 증상을 선택하세요:",
    ["기침", "발열", "두통", "피로감", "목 통증", "복통", "구토", "콧물", "근육통", "호흡곤란", "의식 저하"]
)
other_symptom = st.text_input("기타 증상을 자유롭게 입력하세요:")

# -----------------------------
# 규칙 기반 진단
# -----------------------------
def diagnose(symptoms):
    rules = {
        "감기": ["기침", "콧물", "목 통증", "발열"],
        "독감": ["발열", "기침", "근육통", "피로감"],
        "소화불량": ["복통", "구토"],
        "편두통": ["두통", "피로감"],
        "호흡기 질환": ["기침", "호흡곤란"]
    }
    severe = ["호흡곤란", "의식 저하", "심한 복통", "고열 지속"]

    possible_diseases = []
    for disease, rule in rules.items():
        match = sum(symptom in symptoms for symptom in rule)
        if match >= 2:
            possible_diseases.append(disease)

    is_severe = any(s in symptoms for s in severe)

    if not possible_diseases:
        result = "명확한 질환을 판단하기 어렵습니다."
    else:
        result = f"가능한 질환: {', '.join(possible_diseases)}"

    return result, is_severe

# -----------------------------
# 관련 약 추천
# -----------------------------
def recommend_medication(disease_list):
    meds = {
        "감기": ["해열진통제(예: 타이레놀)", "기침약(예: 코푸시럽)"],
        "독감": ["해열제", "충분한 수분 섭취"],
        "소화불량": ["제산제(예: 겔포스)", "가벼운 식사 유지"],
        "편두통": ["진통제(예: 이부프로펜)", "조용한 환경에서 휴식"],
        "호흡기 질환": ["기침약", "가습기 사용, 수분 섭취"]
    }
    rec = []
    for d in disease_list:
        if d in meds:
            rec.extend(meds[d])
    return list(set(rec))

# -----------------------------
# 만성질환 행동요령
# -----------------------------
def chronic_guidelines(chronic_conditions, symptoms):
    tips = []
    if "당뇨병" in chronic_conditions:
        tips.append("⚠️ 당뇨 환자는 저혈당 증상(어지럼, 식은땀 등)에 주의하고 식사를 거르지 마세요.")
    if "천식" in chronic_conditions and "호흡곤란" in symptoms:
        tips.append("⚠️ 천식 환자는 증상이 심해지면 즉시 흡입제를 사용하고, 완화되지 않으면 병원을 방문하세요.")
    if "고혈압" in chronic_conditions and "두통" in symptoms:
        tips.append("⚠️ 혈압을 측정해보세요. 평소보다 높다면 안정을 취하고 병원에 연락하세요.")
    if "심장질환" in chronic_conditions and "호흡곤란" in symptoms:
        tips.append("⚠️ 심장 관련 증상일 수 있습니다. 증상이 지속되면 즉시 응급실로 가세요.")
    return tips

# -----------------------------
# 진단 실행
# -----------------------------
if st.button("🔍 진단하기"):
    all_symptoms = symptoms + ([other_symptom] if other_symptom else [])
    result, severe = diagnose(all_symptoms)

    st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
    st.info("💡 참고: 본 서비스는 참고용 정보이며, 정확한 진단은 의료진과 상담하세요.")

    # 약 추천
    if "가능한 질환" in result:
        disease_list = [d.strip() for d in result.replace("가능한 질환:", "").split(",")]
        meds = recommend_medication(disease_list)
        if meds:
            st.subheader("💊 관련 약 추천")
            for m in meds:
                st.write(f"- {m}")

    # 만성질환 행동요령
    if chronic_conditions:
        tips = chronic_guidelines(chronic_conditions, symptoms)
        if tips:
            st.subheader("⚕️ 만성질환자 행동요령")
            for t in tips:
                st.markdown(f"- {t}")

    # 심각 증상 시 병원 예약 제안
    if severe:
        st.markdown('<div class="warning-box"><b>🚨 심각한 증상이 감지되었습니다.</b><br>근처 병원 예약을 도와드릴까요?</div>', unsafe_allow_html=True)
        if st.button("🏥 병원 예약하러 가기"):
            st.write("➡️ [네이버 지도 병원 검색 바로가기](https://map.naver.com/v5/search/병원)")

    # 결과 저장
    log = pd.DataFrame({
        "datetime": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "symptoms": [", ".join(all_symptoms)],
        "result": [result],
        "chronic_conditions": [", ".join(chronic_conditions)]
    })

    try:
        existing = pd.read_csv("diagnosis_log.csv")
        updated = pd.concat([existing, log], ignore_index=True)
    except FileNotFoundError:
        updated = log

    updated.to_csv("diagnosis_log.csv", index=False)
    st.success("✅ 진단 결과가 기록되었습니다.")

# -----------------------------
# 푸터
# -----------------------------
st.markdown("---")
st.caption("© 2025 증상 체커 | 사회적 약자를 위한 건강 도우미 프로젝트")
