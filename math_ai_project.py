from sympy import symbols, Eq, solve, sympify, diff, latex
import numpy as np
import matplotlib.pyplot as plt
import re
from gtts import gTTS
import os

# =====================
# إعداد الصفحة
# =====================
st.set_page_config(page_title="Math AI Project", layout="wide")
st.title("🧮 Math AI – مشروع علمي ذكي")

x = symbols("x")
mode = st.radio("اختر وضع الاستخدام:", ["👩‍🎓 وضع تعليمي", "👩‍🔬 وضع متقدم"])

# =====================
# تحويل الصياغة الرياضية
# =====================
def convert_math_to_python(text):
    text = re.sub(r'\^(\d+)', r'**\1', text)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)
    return text.replace(" ", "")

# =====================
# إنشاء ملف صوتي
# =====================
def create_audio(text):
    if os.path.exists("solution_audio.mp3"):
        os.remove("solution_audio.mp3")
    tts = gTTS(text=text, lang='ar')
    tts.save("solution_audio.mp3")
    return "solution_audio.mp3"

# =====================
# Tabs
# =====================
tab1, tab2, tab3 = st.tabs([
    "🔢 العمليات الحسابية",
    "📐 حل المعادلات",
    "📊 رسم الدوال"
])

# ------------------------------------------------
# Tab 1: العمليات الحسابية
# ------------------------------------------------
with tab1:
    st.header("🔢 العمليات الحسابية")

    a = st.number_input("الرقم الأول", value=0.0)
    b = st.number_input("الرقم الثاني", value=0.0)
    op = st.selectbox("العملية", ["جمع", "طرح", "ضرب", "قسمة"])

    if st.button("احسب"):
        if op == "قسمة" and b == 0:
            st.error("❌ لا يمكن القسمة على صفر")
        else:
            result = {
                "جمع": a + b,
                "طرح": a - b,
                "ضرب": a * b,
                "قسمة": a / b
            }[op]
            st.success(f"✅ النتيجة = {result}")

# ------------------------------------------------
# Tab 2: حل المعادلات + صوت
# ------------------------------------------------
with tab2:
    st.header("📐 حل المعادلات")

    eq_input = st.text_input("أدخل المعادلة (مثال: x^2 - 4x + 3 = 0)")

    if st.button("حل المعادلة"):
        if "=" not in eq_input:
            st.error("❌ يجب كتابة المعادلة وبها =")
        else:
            try:
                eq_text = convert_math_to_python(eq_input)
                left, right = eq_text.split("=")
                equation = Eq(sympify(left), sympify(right))
                solutions = solve(equation, x)

                st.subheader("الحلول")
                for s in solutions:
                    st.latex(f"x = {latex(s)}")

                # شرح نصي
                explanation = "هذه معادلة رياضية. "
                explanation += "قمنا بنقل الحدود إلى طرف واحد. "
                explanation += "ثم قمنا بحل المعادلة. "
                for s in solutions:
                    explanation += f"قيمة اكس تساوي {s}. "

                if mode == "👩‍🎓 وضع تعليمي":
                    st.info(explanation)

                if st.button("🎧 تشغيل الشرح الصوتي"):
                    audio = create_audio(explanation)
                    st.audio(audio, format="audio/mp3")

            except Exception as e:
                st.error(f"❌ خطأ في الحل: {e}")

# ------------------------------------------------
# Tab 3: رسم الدوال
# ------------------------------------------------
with tab3:
    st.header("📊 رسم الدوال")

    func_text = st.text_input("أدخل الدالة (مثال: x^2 - 4x + 3)")
    x_min, x_max = st.slider("نطاق x", -10, 10, (-5, 5))

    if st.button("ارسم"):
        try:
            f = sympify(convert_math_to_python(func_text))
            xs = np.linspace(x_min, x_max, 400)
            ys = [float(f.subs(x, v)) for v in xs]

            fig, ax = plt.subplots()
            ax.plot(xs, ys)
            ax.axhline(0)
            ax.axvline(0)
            ax.grid(True)

            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ خطأ في الدالة: {e}")
