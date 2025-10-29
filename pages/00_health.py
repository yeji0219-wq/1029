import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="증상 체커",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="expanded",
)

# -----------------------------
# UI 스타일
# -----------------------------
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #2E86C1;
            font-size: 36px;
            font-weight: bold;
        }
        .sub-title {
            text-align: center;
            color: #117A65;
            font-size: 18px;
            margin-bottom: 20px;
        }
        .result-box {
            background-color: #E8F8F5;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">💊 증상 체커</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">간단한 증상 입력으로 가능한 질환을 확인해보세요</p>', unsafe_allow_html=True)

# -----------------------------
# 증상 입력
# -----------------------------
st.header("👩‍⚕️ 증상 선택")
symptoms = st.multiselect(
    "아래에서 현재 증상을 선택하세요:",
    ["기침", "발열", "두통", "피로감", "목 통증", "복통", "구토", "콧물", "근육통", "호흡곤란"]
)

other_symptom = st.text_input("기타 증상이 있다면 입력하세요:")

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

    possible_diseases = []
    for disease, rule in rules.items():
        match_count = sum(symptom in symptoms for symptom in rule)
        if match_count >= 2:  # 최소 2개 이상 일치할 때만 진단 후보로 추가
            possible_diseases.append(disease)

    if not possible_diseases:
        return "명확한 질환을 판단하기 어렵습니다. 증상이 지속되면 병원을 방문하세요."
    else:
        return f"가능한 질환: {', '.join(possible_diseases)}"

# -----------------------------
# 진단 버튼
# -----------------------------
if st.button("🔍 진단하기"):
    all_symptoms = symptoms + ([other_symptom] if other_symptom else [])
    result = diagnose(all_symptoms)

    st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
    st.info("💡 참고: 본 서비스는 의료 진단이 아닌 참고용 정보입니다. 증상이 심하면 반드시 병원을 방문하세요.")

    # -----------------------------
    # 결과 로그 저장
    # -----------------------------
    log = pd.DataFrame({
        "datetime": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "symptoms": [", ".join(all_symptoms)],
        "result": [result]
    })
    try:
        existing = pd.read_csv("diagnosis_log.csv")
        updated = pd.concat([existing, log], ignore_index=True)
    except FileNotFoundError:
        updated = log

    updated.to_csv("diagnosis_log.csv", index=False)
    st.success("✅ 진단 결과가 기록되었습니다.")

# -----------------------------
# 다국어 지원 (영어)
# -----------------------------
with st.sidebar:
    st.header("🌐 언어 / Language")
    lang = st.radio("언어 선택:", ["한국어", "English"])

    if lang == "English":
        st.markdown("""
        ### 💊 Symptom Checker  
        Enter your symptoms and get a possible diagnosis based on simple rules.  
        (For reference only — visit a hospital for medical advice.)
        """)

        st.write("""
        Symptoms covered: cough, fever, headache, fatigue, sore throat, stomach pain, vomiting, runny nose, muscle pain, shortness of breath.
        """)

        st.write("Developed with ❤️ for accessible healthcare.")
    else:
        st.markdown("""
        ### 💊 증상 체커  
        입력된 증상을 바탕으로 간단한 진단 결과를 제공합니다.  
        (참고용이며, 정확한 진단은 병원에서 받아야 합니다.)
        """)

# -----------------------------
# 푸터
# -----------------------------
st.markdown("---")
st.caption("© 2025 증상 체커 | 사회적 약자를 위한 건강 도우미 프로젝트")
