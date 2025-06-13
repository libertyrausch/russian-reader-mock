import streamlit as st
import random

st.set_page_config(page_title="Russian Reading App", layout="wide")

# Mock data: A few sample Russian passages with questions
sample_passages = [
    {
        "passage": "Анна проснулась рано утром. За окном светило солнце, и птицы пели свои утренние песни. Сегодня у неё был важный день — первое собеседование на работу.",
        "qa": [
            {"question": "Почему день был важным для Анны?", "correct_answer": "У неё было собеседование на работу."},
            {"question": "Что делали птицы за окном?", "correct_answer": "Они пели свои утренние песни."},
        ]
    },
    {
        "passage": "Иван всегда мечтал поехать в Санкт-Петербург. Он читал о его красивых дворцах, мостах и белых ночах. Летом он наконец-то купил билет и отправился в путь.",
        "qa": [
            {"question": "Куда хотел поехать Иван?", "correct_answer": "В Санкт-Петербург."},
            {"question": "Почему Иван интересовался этим городом?", "correct_answer": "Из-за дворцов, мостов и белых ночей."},
        ]
    },
    {
        "passage": "Оля и её брат пошли в парк. Они катались на велосипедах, ели мороженое и играли с собакой. Это был один из самых весёлых дней лета.",
        "qa": [
            {"question": "С кем пошла Оля в парк?", "correct_answer": "С братом."},
            {"question": "Что они делали в парке?", "correct_answer": "Катались на велосипедах, ели мороженое и играли с собакой."},
        ]
    },
]

# Load passage if not already present
if "qa_block" not in st.session_state:
    st.session_state.qa_block = random.choice(sample_passages)
    st.session_state.score = 0
    st.session_state.total = 0

# Function to simulate getting a new passage
def load_new_passage():
    st.session_state.qa_block = random.choice(sample_passages)
    st.session_state.feedback = {}
    st.session_state.score = 0
    st.session_state.total = 0

st.title("🇷🇺 Russian Reading Practice App (Mock Mode)")

st.markdown("Click the button below to load a random Russian reading passage with AI-style questions.")

# New passage button
if st.button("📖 Load New Passage"):
    load_new_passage()

# Show passage
st.subheader("📜 Passage")
st.write(st.session_state.qa_block["passage"])

# Show questions
st.subheader("❓ Questions")
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

for i, qa in enumerate(st.session_state.qa_block["qa"]):
    user_answer = st.text_input(f"Q{i+1}: {qa['question']}", key=f"answer_{i}")

    if user_answer and f"feedback_{i}" not in st.session_state.feedback:
        correct = qa["correct_answer"].strip().lower()
        given = user_answer.strip().lower()

        is_correct = correct == given
        feedback_msg = "✅ Correct!" if is_correct else f"❌ Incorrect. Correct answer: {qa['correct_answer']}"
        st.session_state.feedback[f"feedback_{i}"] = feedback_msg

        if is_correct:
            st.session_state.score += 1
        st.session_state.total += 1

    if f"feedback_{i}" in st.session_state.feedback:
        st.write(st.session_state.feedback[f"feedback_{i}"])

# Show score
if st.session_state.total > 0:
    st.success(f"🎯 Score: {st.session_state.score} / {st.session_state.total}")
