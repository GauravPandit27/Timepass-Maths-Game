import streamlit as st
import random

# --- Session state setup ---
default_state = {
    "level": None,
    "lives": 3,
    "hints": 3,
    "skips": 3,
    "question": "",
    "answer": None,
    "game_started": False,
    "score": 0,
    "user_input": "",
    "answered_correctly": False
}

for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Function: Generate question based on level ---
def generate_question(level):
    if level == "Easy":
        num1, num2 = random.randint(1, 10), random.randint(1, 10)
        op = random.choice(["+", "-"])
    elif level == "Medium":
        num1, num2 = random.randint(5, 50), random.randint(5, 50)
        op = random.choice(["+", "-", "*"])
    else:  # Hard
        op = random.choice(["+", "-", "*", "/"])
        if op == "/":
            num2 = random.randint(1, 10)
            answer = random.randint(1, 10)
            num1 = num2 * answer
        else:
            num1, num2 = random.randint(10, 100), random.randint(10, 100)

    question = f"{num1} {op} {num2}"
    return question, round(eval(question))

# --- Title ---
st.title("🧮 Math Abyassus: Saee Deshpande")

# --- Level Selection ---
if not st.session_state["game_started"]:
    st.session_state["level"] = st.selectbox("Select your level:", ["Easy", "Medium", "Hard"])
    if st.button("Start Game 🎮"):
        st.session_state["game_started"] = True
        st.session_state["question"], st.session_state["answer"] = generate_question(st.session_state["level"])
        st.session_state["score"] = 0
        st.session_state["lives"] = 3
        st.session_state["hints"] = 3
        st.session_state["skips"] = 3
        st.session_state["answered_correctly"] = False
        st.session_state["user_input"] = ""

# --- Game Area ---
if st.session_state["game_started"] and st.session_state["lives"] > 0:

    st.markdown(f"### ❤️ Lives: `{st.session_state.lives}` | 💡 Hints: `{st.session_state.hints}` | ⏭️ Skips: `{st.session_state.skips}`")
    st.markdown(f"### 🧠 Solve: `{st.session_state.question}`")

    if not st.session_state["answered_correctly"]:
        with st.form(key="answer_form", clear_on_submit=True):
            user_input = st.text_input("Your Answer:", key="user_input_field")
            submitted = st.form_submit_button("Submit")

            if submitted:
                try:
                    user_answer = int(user_input)
                    if user_answer == st.session_state["answer"]:
                        st.success("✅ Correct!")
                        st.session_state["score"] += 1
                        st.session_state["answered_correctly"] = True
                        st.balloons()
                    else:
                        st.session_state["lives"] -= 1
                        st.rerun()
                except:
                    st.warning("⚠️ Please enter a valid number!")

    # Show "Next Question" if answered correctly
    if st.session_state["answered_correctly"]:
        if st.button("➡️ Next Question"):
            st.session_state["question"], st.session_state["answer"] = generate_question(st.session_state["level"])
            st.session_state["answered_correctly"] = False
            st.rerun()

    # Hint and Skip Buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Hint 💡"):
            if st.session_state["hints"] > 0:
                st.info(f"Hint: The answer is `{st.session_state['answer']}`")
                st.session_state["hints"] -= 1
            else:
                st.warning("No hints left!")

    with col2:
        if st.button("Skip ⏭️"):
            if st.session_state["skips"] > 0:
                st.session_state["question"], st.session_state["answer"] = generate_question(st.session_state["level"])
                st.session_state["skips"] -= 1
                st.session_state["answered_correctly"] = False
                st.rerun()
            else:
                st.warning("No skips left!")

# --- Game Over ---
if st.session_state["lives"] == 0:
    st.markdown("## ☠️ Game Over! Better luck next time.")
    st.markdown(f"**🏆 Final Score:** `{st.session_state['score']}`")
    if st.button("Play Again 🔁"):
        for key in default_state.keys():
            st.session_state[key] = default_state[key]
        st.rerun()

