import streamlit as st


def layout_header():
    """Displays the main title and description."""
    st.title("📚 Study Mate - Your Learning AI")
    st.write("Upload your study PDF and let AI summarize it and create quizzes for revision.")


def upload_section():
    """Displays file uploader and returns uploaded file."""
    return st.file_uploader("📄 Upload PDF Notes", type=["pdf"])


def quiz_selector():
    """Returns selected quiz type."""
    return st.radio("🧠 Select Quiz Type:", ["Multiple Choice", "Mixed"], index=0)


def action_buttons():
    """Creates horizontal buttons and returns clicked action."""
    col1, col2, col3 = st.columns(3)
    summary = col1.button("📝 Generate Summary")
    quiz = col2.button("🧠 Create Quiz")
    both = col3.button("⚡ Generate Both")
    
    return summary, quiz, both


def show_summary(summary_text):
    """Show summary in UI."""
    st.subheader("📝 Summary")
    st.success("Summary Generated Successfully!")
    st.markdown(summary_text)


def show_quiz(quiz_text):
    """Show quiz in UI."""
    st.subheader("🧠 Quiz")
    st.info("Quiz Ready!")
    st.markdown(quiz_text)


def show_loader(message="Processing..."):
    """Reusable spinner."""
    return st.spinner(message)


def footer():
    """App footer."""
    st.markdown("---")
    st.caption("🚀 Built with ❤️ using Streamlit + Gemini AI")


