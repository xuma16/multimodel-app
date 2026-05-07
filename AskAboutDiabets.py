import streamlit as st
from datetime import datetime
import Router  # ✅ Uses the router instead of loading models directly

MODEL_BADGE = {
    "greetings": ("🗣️", "#d4edda", "Greetings Model"),
    "diabetes":  ("🩺", "#f0f0f0", "Diabetes Model"),
}


def show():
    st.markdown(
        """
            <style> 
            h1{text-align:center;
                color:brown;
            }
            .center{
                text-align:center;
                color:brown;
                }
            </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class=header"><h1>Hellow Your Welcome</h1></div>'
        '<div class="center">Ask me about diabets<br> Niulize kuhusu kisukari</div>',
        unsafe_allow_html=True
        )

    # ---------------- Load Models via Router ----------------
    try:
        Router.load_models()
    except Exception as e:
        st.error(f"❌ Error loading models: {e}")
        st.stop()

    # ---------------- Description ----------------
    st.write(
        "Ask about diabetes in English or Swahili\n"
        "Uliza kuhusu kisukari kwa Kiingereza au Kiswahili"
    )

    # ---------------- Session State ----------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ---------------- User Input ----------------
    user_input = st.text_input("Type your question here / Andika swali lako hapa:")

    if st.button("Send / Tuma"):
        if user_input.strip():
            try:
                # ✅ Router handles model selection automatically
                response, model_used = Router.predict(user_input)
                timestamp = datetime.now().strftime("%H:%M:%S")

                st.session_state.chat_history.append({
                    "user": user_input,
                    "bot": response,
                    "time": timestamp,
                    "model": model_used,
                })

            except Exception as e:
                st.error(f"Prediction error: {e}")
        else:
            st.warning("Please enter a question / Tafadhali andika swali")

    # ---------------- Chat Display (Newest on Top) ----------------
    st.markdown("### 💬 Chat History")

    for chat in reversed(st.session_state.chat_history):
        icon, color, label = MODEL_BADGE.get(chat["model"], ("🤖", "#f0f0f0", "Model"))

        st.markdown(
            f"""
            <div style =" display:flex; justify-content:flex-end;">
                <div style="
                    background-color:#e6f2ff;
                    padding:10px;
                    border-radius:10px;
                    margin-bottom:5px;
                    text-align: right;
                    display:inline-block;
                    width:fit-content;
                    max-width:70%;
                    word-wrap:break-word;
                ">
                    🧑 <b>You</b> <span style="font-size:10px;color:gray;">[{chat['time']}]</span><br>
                    {chat['user']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="
                background-color:{color};
                padding:10px;
                border-radius:10px;
                margin-bottom:10px;
            ">
                {icon} <b>Bot</b>
                <span style="font-size:10px;color:gray;">[{chat['time']}] &nbsp;•&nbsp; {label}</span><br>
                {chat['bot']}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------- Disclaimer ----------------
    st.markdown(
        '<div class="center">⚠️ For education only. Consult a doctor.</div>',
    unsafe_allow_html=True
    )
