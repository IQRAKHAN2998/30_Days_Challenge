import streamlit as st
from dotenv import load_dotenv

from modules.pdf_handler import extract_text_from_pdf
from modules.ai_engine import generate_summary, generate_quiz
from modules.ui_components import (
    layout_header, upload_section, show_summary,
    show_loader, footer
)

load_dotenv()

st.set_page_config(page_title="📚 Study Mate", layout="wide")

layout_header()

uploaded_file = upload_section()


# ---------------- SESSION STATE ----------------
st.session_state.setdefault("pdf_text", None)
st.session_state.setdefault("summary", None)
st.session_state.setdefault("quiz_questions", None)
st.session_state.setdefault("user_answers", {})


# ---------------- AFTER PDF UPLOAD ----------------
if uploaded_file:
    st.success("📄 PDF Uploaded Successfully!")

    if not st.session_state.pdf_text:
        st.session_state.pdf_text = extract_text_from_pdf(uploaded_file)

    if st.button("📝 Generate Summary"):
        with show_loader("Generating Summary..."):
            st.session_state.summary = generate_summary(st.session_state.pdf_text)

    if st.session_state.summary:
        show_summary(st.session_state.summary)

        if st.button("🧠 Generate MCQs"):
            with show_loader("Generating Quiz..."):
                raw_quiz = generate_quiz(st.session_state.pdf_text, "Multiple Choice")

                questions = []
                for block in raw_quiz.split("\n\n"):
                    lines = [l.strip() for l in block.split("\n") if l.strip()]
                    if len(lines) >= 6 and "A)" in block:
                        questions.append({
                            "question": lines[0],
                            "options": lines[1:5],
                            "answer": lines[-1].replace("Answer:", "").strip()
                        })

                st.session_state.quiz_questions = questions


    # --------------- RENDER QUIZ ----------------
    if st.session_state.quiz_questions:

        st.subheader("📝 Quiz Section:")

        for idx, q in enumerate(st.session_state.quiz_questions):
            st.write(f"**{idx+1}. {q['question']}**")

            selected = st.radio(
                f"Choose answer:",
                q["options"],
                key=f"q{idx}"
            )
            st.session_state.user_answers[idx] = selected

        if st.button("✅ Submit Quiz"):
            score = 0

            st.subheader("📌 Results:")

            for i, q in enumerate(st.session_state.quiz_questions):
                user = st.session_state.user_answers.get(i)
                correct = q["answer"]

                user_answer_clean = user.split(")")[0].strip()[0] if user else ""
                correct_clean = correct.strip()

                if user_answer_clean.lower() == correct_clean.lower():
                    st.success(f"✔ Q{i+1}: Correct!")
                    score += 1
                else:
                    st.error(f"❌ Q{i+1}: Wrong — Correct Answer: {correct}")

            st.info(f"🎯 Final Score: {score} / {len(st.session_state.quiz_questions)}")


footer()
