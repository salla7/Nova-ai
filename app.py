
import streamlit as st
import requests

st.set_page_config(
    page_title="Salah AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Salah AI")
st.caption("مساعد ذكي مستقل الواجهة، يعمل بواسطة نموذج ذكاء اصطناعي حقيقي")

# إعدادات الواجهة
if "messages" not in st.session_state:
    st.session_state.messages = []

# مفتاح API خاص، لا تضعه في الكود
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    API_KEY = ""

with st.sidebar:
    st.header("⚙️ الإعدادات")
    st.write("المحرك: Groq API")
    st.write("اللغة: العربية والفرنسية وغيرها")
    st.write("الذاكرة: المحادثة الحالية")
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("اكتب سؤالك هنا...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not API_KEY:
            answer = (
                "⚙️ خاصنا نربطو مفتاح API باش نخدمو الذكاء الاصطناعي. "
                "الخطوة التالية هي إنشاء مفتاح مجاني من Groq "
                "وإضافته في إعدادات أسرار التطبيق، وليس داخل الكود."
            )
            st.info(answer)
        else:
            try:
                with st.spinner("🤔 كنحلل السؤال ونوجد الجواب..."):
                    response = requests.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "llama-3.3-70b-versatile",
                            "messages": [
                                {
                                    "role": "system",
                                    "content": (
                                        "أنت مساعد ذكاء اصطناعي مفيد وصريح. "
                                        "أجب بلغة المستخدم، واشرح ببساطة، "
                                        "ولا تخترع المعلومات عندما لا تعرفها."
                                    )
                                },
                                *st.session_state.messages
                            ],
                            "temperature": 0.7,
                            "max_tokens": 1200
                        },
                        timeout=60
                    )

                    if response.ok:
                        answer = response.json()["choices"][0][
                            "message"
                        ]["content"]
                        st.markdown(answer)
                    else:
                        answer = (
                            f"وقع خطأ من خدمة الذكاء الاصطناعي "
                            f"({response.status_code}). "
                            "تحقق من المفتاح والموديل وحدود الاستعمال."
                        )
                        st.error(answer)

            except requests.RequestException:
                answer = "تعذر الاتصال بالخدمة. تحقق من الإنترنت وحاول مجدداً."
                st.error(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })
