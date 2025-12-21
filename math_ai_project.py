import streamlit as st
from sympy import symbols, Eq, solve, sympify, diff, latex
import numpy as np
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display
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
    text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', text)
    return text.replace(" ", "")

# =====================
# إنشاء ملف صوتي (يدعم جميع الأجهزة)
# =====================
def create_audio(text):
    tts = gTTS(text=text, lang='ar')
    file_name = "solution_audio.mp3"
    tts.save(file_name)
    return file_name

# =====================
# Tabs
# =====================
tab1, tab2, tab3 = st.tabs([
    "🔢 العمليات الحسابية",
    "📐 حل المعادلات",
    "📊 رسم وتحليل الدوال"
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

            if mode == "👩‍🎓 وضع تعليمي":
                st.info("💡 تم تطبيق العملية الحسابية مباشرة على الرقمين المدخلين")

# ------------------------------------------------
# Tab 2: حل المعادلات + شرح صوتي (يدعم كل الأجهزة)
# ------------------------------------------------
with tab2:
    st.header("📐 حل المعادلات خطوة بخطوة")

    eq_input = st.text_input("أدخل المعادلة (مثال: x^2 - 4x + 3 = 0)")

    if st.button("حل المعادلة"):
        try:
            eq_text = convert_math_to_python(eq_input)
            left, right = eq_text.split("=")
            equation = Eq(sympify(left), sympify(right))
            solutions = solve(equation, x)

            # عرض المعادلة
            st.subheader("🔹 المعادلة")
            st.latex(eq_input)

            # النقل للطرف الواحد
            moved = sympify(left) - sympify(right)
            st.subheader("🔹 بعد النقل")
            st.latex(Eq(moved, 0))

            # الحلول
            st.subheader("🔹 الحلول النهائية")
            for s in solutions:
                st.latex(f"x = {latex(s)}")

            # شرح نصي
            explanation_lines = []
            degree = moved.as_poly(x).degree()

            if degree == 2:
                explanation_lines.append("هذه معادلة تربيعية من الدرجة الثانية.")
                explanation_lines.append("قمنا بنقل جميع الحدود إلى طرف واحد.")
                explanation_lines.append("ثم قمنا بحل المعادلة جبريًا.")
            elif degree == 1:
                explanation_lines.append("هذه معادلة خطية من الدرجة الأولى.")
                explanation_lines.append("قمنا بعزل المتغير اكس للحصول على الحل.")

            explanation_lines.append("القيم التي تحقق المعادلة هي:")
            for s in solutions:
                explanation_lines.append(f"قيمة اكس تساوي {s}")

            if mode == "👩‍🎓 وضع تعليمي":
                st.subheader("🧠 شرح الحل")
                for line in explanation_lines:
                    st.write(line)

            # نص الشرح الصوتي
            audio_text = " ".join(explanation_lines)

            # زر إنشاء وتشغيل الصوت
            if st.button("🎧 تشغيل الشرح الصوتي"):
                audio_file = create_audio(audio_text)
                st.audio(audio_file, format="audio/mp3")

        except:
            st.error("❌ تأكدي من كتابة المعادلة بشكل صحيح")

# ------------------------------------------------
# Tab 3: رسم وتحليل الدوال
# ------------------------------------------------
with tab3:
    st.header("📊 رسم وتحليل الدوال")

    func_text = st.text_input("أدخل الدالة (مثال: x^2 - 4x + 3)")
    x_min, x_max = st.slider("نطاق x", -10, 10, (-5, 5))
    y_min, y_max = st.slider("نطاق y", -10, 10, (-5, 5))

    if st.button("ارسم الدالة"):
        try:
            func_sympy = convert_math_to_python(func_text)
            f = sympify(func_sympy)

            xs = np.linspace(x_min, x_max, 400)
            ys = [float(f.subs(x, v)) for v in xs]

            fig, ax = plt.subplots()
            ax.plot(xs, ys)
            ax.axhline(0)
            ax.axvline(0)
            ax.grid(True)

            title = get_display(
                arabic_reshaper.reshape(f"رسم الدالة: {func_text}")
            )
            ax.set_title(title)
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)

            st.pyplot(fig)

            roots = solve(f, x)
            real_roots = [r for r in roots if r.is_real]
            st.subheader("📍 نقاط التقاطع مع محور x")
            st.write(real_roots)

        except Exception as e:
            st.error(f"❌ خطأ في الدالة: {e}")
