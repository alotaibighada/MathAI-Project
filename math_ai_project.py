import streamlit as st
from sympy import symbols, Eq, solve, sympify, latex, lambdify
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import re
from gtts import gTTS
import os
import arabic_reshaper
from bidi.algorithm import get_display

# =====================
# إعداد الخط العربي
# =====================
rcParams['font.family'] = 'DejaVu Sans'
rcParams['axes.unicode_minus'] = False

# =====================
# إعداد الصفحة
# =====================
st.set_page_config(page_title="Math AI Project", layout="wide")
st.title("🧮 مشروع Math AI – النسخة النهائية")

x = symbols("x")
mode = st.radio("اختر وضع الاستخدام:", ["👩‍🎓 وضع تعليمي", "👩‍🔬 وضع متقدم"])

# =====================
# دوال مساعدة
# =====================
def convert_math_to_python(text):
    text = text.replace(" ", "")
    text = text.replace("^", "**")

    # 2x → 2*x
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)

    # x2 → x*2
    text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', text)

    # x(x+1) → x*(x+1)
    text = re.sub(r'([a-zA-Z])\(', r'\1*(', text)

    # )( → )*(
    text = re.sub(r'\)\(', r')*(', text)

    return text

def arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

def create_audio(text):
    if os.path.exists("solution_audio.mp3"):
        os.remove("solution_audio.mp3")
    tts = gTTS(text=text, lang="ar")
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
# Tab 2: حل المعادلات + الشرح الصوتي
# ------------------------------------------------
with tab2:
    st.header("📐 حل المعادلات خطوة بخطوة")

    eq_input = st.text_input("أدخل المعادلة (مثال: x^2-4x+3 = 0)")

    if st.button("حل المعادلة"):
        if "=" not in eq_input:
            st.error("❌ يجب أن تحتوي المعادلة على =")
        else:
            try:
                eq_text = convert_math_to_python(eq_input)
                left, right = eq_text.split("=")
                equation = Eq(sympify(left), sympify(right))
                solutions = solve(equation, x)

                st.subheader("🔹 الحلول")
                for s in solutions:
                    st.latex(f"x = {latex(s)}")

                explanation_lines = [
                    "هذه معادلة رياضية.",
                    "قمنا بإعادة كتابة المعادلة بصيغة مناسبة للبرنامج.",
                    "ثم قمنا بحل المعادلة خطوة بخطوة."
                ]

                for s in solutions:
                    explanation_lines.append(f"قيمة اكس تساوي {s}")

                explanation_text = " ".join(explanation_lines)

                if mode == "👩‍🎓 وضع تعليمي":
                    st.subheader("🧠 شرح الحل")
                    for line in explanation_lines:
                        st.write("•", line)

                if st.button("🎧 تشغيل الشرح الصوتي"):
                    audio_file = create_audio(explanation_text)
                    st.audio(audio_file, format="audio/mp3")

            except Exception as e:
                st.error(f"❌ خطأ في الحل: {e}")

# ------------------------------------------------
# Tab 3: رسم الدوال
# ------------------------------------------------
with tab3:
    st.header("📊 رسم الدوال")

    func_text = st.text_input("أدخل الدالة (مثال: x^2-4x+3)")

    if st.button("ارسم الدالة"):
        try:
            f_sym = sympify(convert_math_to_python(func_text))
            f = lambdify(x, f_sym, "numpy")

            roots = solve(Eq(f_sym, 0), x)
            real_roots = [float(r) for r in roots if r.is_real]

            x_min = min(real_roots) - 5 if real_roots else -10
            x_max = max(real_roots) + 5 if real_roots else 10

            xs = np.linspace(x_min, x_max, 400)
            ys = f(xs)

            fig, ax = plt.subplots()
            ax.plot(xs, ys, linewidth=2, label=arabic_text("الدالة"))
            ax.axhline(0, color="black")
            ax.axvline(0, color="black")
            ax.grid(True, linestyle="--", alpha=0.7)

            for r in real_roots:
                ax.plot(r, 0, 'ro')
                ax.text(r, 0, f"{r}", fontsize=9)

            ax.set_title(arabic_text(f"رسم الدالة: {func_text}"))
            ax.set_xlabel(arabic_text("س"))
            ax.set_ylabel(arabic_text("ص"))
            ax.legend()
            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ خطأ في الرسم: {e}")
