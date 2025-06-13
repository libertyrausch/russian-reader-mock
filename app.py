import streamlit as st
import random

st.set_page_config(page_title="📚 Russian Reading Trainer", layout="wide")
st.title("📖 Russian Reading Comprehension Trainer")

# --- Initialize progress tracking in session state ---
if "completed_passages" not in st.session_state:
    st.session_state.completed_passages = 0
if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "current_passage_index" not in st.session_state:
    st.session_state.current_passage_index = 0
if "go_next" not in st.session_state:
    st.session_state.go_next = False

# --- Custom CSS for larger fonts and side progress bar ---
st.markdown("""
    <style>
    .question-text {
        font-size: 20px !important;
        font-weight: 600;
    }
    .stRadio > div > label,
    .stSelectbox label, 
    .stTextInput label,
    .stSelectbox div {
        font-size: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Full-length passages (500+ words each) with unique questions ---
from passages_data import passages_data

if st.session_state.current_passage_index >= len(passages_data):
    st.success("🎉 Вы завершили все доступные тексты!")
    st.stop()

current = passages_data[st.session_state.current_passage_index]

col1, col2 = st.columns([4, 1])

with col1:
    st.subheader("📘 Прочитайте текст:")
    st.write(current["text"])

    responses = {}
    for idx, q in enumerate(current["questions"]):
        key = f"q{idx}"
        st.markdown(f"<div class='question-text'>❓ {q['question']}</div>", unsafe_allow_html=True)

        if q["type"] == "true_false":
            responses[key] = st.radio("Ваш ответ:", ["Правда", "Ложь"], key=key, index=None)
        elif q["type"] == "multiple_choice":
            responses[key] = st.radio("Выберите один вариант:", q["options"], key=key, index=None)
        elif q["type"] == "matching":
            responses[key] = st.selectbox("Её значение:", q["options"], key=key, index=None)
        elif q["type"] == "short_answer":
            responses[key] = st.text_input("Ваш ответ:", key=key)

    if st.button("✅ Проверить ответы") and not st.session_state.answered:
        score = 0
        for idx, q in enumerate(current["questions"]):
            key = f"q{idx}"
            ans = responses[key]
            if q["type"] in ["true_false", "multiple_choice", "matching"]:
                if ans == q["answer"]:
                    st.success(f"✅ Верно! {q['explanation']}")
                    score += 1
                elif ans:
                    st.error(f"❌ Неверно. {q['explanation']}")
            elif q["type"] == "short_answer":
                if any(kw in ans.lower() for kw in q["keywords"]):
                    st.success(f"✅ Верно! {q['explanation']}")
                    score += 1
                elif ans:
                    st.error(f"❌ Неверно. {q['explanation']}")

        st.session_state.correct_answers += score
        st.session_state.answered = True
        st.session_state.go_next = True

    if st.session_state.answered and st.session_state.go_next:
        if st.button("➡️ Следующий текст"):
            st.session_state.answered = False
            st.session_state.go_next = False
            st.session_state.completed_passages += 1
            st.session_state.current_passage_index += 1
            for i in range(len(current["questions"])):
                st.session_state.pop(f"q{i}", None)
            st.rerun()

with col2:
    st.markdown("## 🧭 Прогресс")
    st.markdown(f"📘 Текстов пройдено: **{st.session_state.completed_passages}**")
    st.markdown(f"✅ Правильных ответов: **{st.session_state.correct_answers}**")
    total_questions = st.session_state.completed_passages * 4
    if total_questions:
        accuracy = st.session_state.correct_answers / total_questions * 100
        st.markdown(f"🎯 Точность: **{accuracy:.1f}%**")
