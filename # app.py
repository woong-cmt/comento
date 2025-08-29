# app.py
import streamlit as st
import requests

# --- 페이지 설정 ---
st.set_page_config(page_title="카카오톡 스타일 챗봇", layout="centered")

# --- CSS (카카오톡 스타일 및 반응형) ---
st.markdown("""
    <style>
    .chat-container {
        max-width: 500px;
        margin: auto;
        padding: 10px;
        background-color: #f9f9f9;
        border-radius: 10px;
    }
    .bubble {
        padding: 10px 15px;
        border-radius: 20px;
        margin-bottom: 10px;
        max-width: 80%;
        word-wrap: break-word;
    }
    .user-bubble {
        background-color: #ffe400;
        text-align: right;
        margin-left: auto;
    }
    .bot-bubble {
        background-color: #f1f1f1;
        text-align: left;
        margin-right: auto;
    }
    @media screen and (max-width: 768px) {
        .chat-container {
            width: 100% !important;
            padding: 5px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- 세션 상태 ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 헤더 ---
st.title("🟡 카카오톡 스타일 AI 챗봇")
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# --- 대화 출력 ---
for msg in st.session_state.chat_history:
    role, text = msg["role"], msg["content"]
    bubble_class = "user-bubble" if role == "user" else "bot-bubble"
    st.markdown(f"<div class='bubble {bubble_class}'>{text}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- 입력창 ---
user_input = st.text_input("메시지를 입력하세요", key="input", label_visibility="collapsed")

if st.button("전송") and user_input:
    # 사용자 메시지 추가
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # PotensDot API 호출 예시
    try:
        response = requests.post(
            "https://api.potens.ai/generate",  # 실제 PotensDot API URL로 교체 필요
            headers={"Authorization": "Bearer YOUR_API_KEY"},  # API 키 교체
            json={"prompt": user_input}
        )
        response_json = response.json()
        ai_answer = response_json.get("response", "응답을 불러오지 못했어요.")
    except Exception as e:
        ai_answer = f"에러 발생: {str(e)}"

    # AI 응답 저장
    st.session_state.chat_history.append({"role": "bot", "content": ai_answer})

    # 입력창 초기화
    st.experimental_rerun()
    
    
# --- 대화 출력 ---
for msg in st.session_state.chat_history:
    role, text = msg["role"], msg["content"]
    bubble_class = "user-bubble" if role == "user" else "bot-bubble"
    st.markdown(f"<div class='bubble {bubble_class}'>{text}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)