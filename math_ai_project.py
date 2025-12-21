import streamlit as st
from sympy import symbols, Eq, solve, sympify, latex, lambdify
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import re
import arabic_reshaper
from bidi.algorithm import get_display

# =====================
# إعداد الخط العربي في Matplotlib
# =====================
rcParams['font.family'] = 'Arial'
rcParams['axes.unicode_minus'] = False

# =====================
# إعداد الصفحة
# =====================
st.set_page_config(page_title="Math AI Project", layout="wide")
st.title("🧮 مشروع Math AI – نسخة مصححة")

x = symbols("x")
mode = st.radio("اختر وضع الاستخدام:", ["👩‍🎓 وضع تعليمي", "👩‍🔬 وضع متقدم"])

# =====================
# تحويل الصياغة الرياضية البسيطة
# =====================
def convert_math_to_python(text):
    text = text.replace(" ", "")
    text = text.replace("^", "**")
    # التعامل مع الضرب الضمني مثل 2x → 2*x
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)
    text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', text)
    text = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', text)
    return text

# =====================
# دالة لإظهار النصوص العربية في الرسم
# =====================
def arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

# =====================
# قائمة الدوال الإنجليزية الجاهزة
# =====================
english_functions = [
    "None",
    "sqrt(x)",
    "sin(x)",
    "cos(x)",
    "tan(x)",
    "log(x)",
    "exp(x)",
    "Abs(x)"
]

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
    if st.button("احسب", key="calc"):
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
# Tab 2: حل المعادلات
# ------------------------------------------------
with tab2:
    st.header("📐 حل المعادلات خطوة خطوة")
    eq_input = st.text_input("أدخل المعادلة (مثال: x^2 - 4*x + 3 = 0)")

    func_choice = st.selectbox("أو اختر دالة جاهزة", english_functions)

    if func_choice != "None":
        eq_input = func_choice + " = 0"

    if st.button("حل المعادلة", key="solve"):
        try:
            if "=" not in eq_input:
                st.error("❌ يجب كتابة المعادلة وبها =")
            else:
                eq_text = convert_math_to_python(eq_input)
                left, right = eq_text.split("=")
                equation = Eq(sympify(left), sympify(right))
                solutions = solve(equation, x)

                st.subheader("خطوات الحل:")
                if mode == "👩‍🎓 وضع تعليمي":
                    st.markdown(f"1️⃣ تم إدخال المعادلة: `{eq_input}`")
                    st.markdown(f"2️⃣ تحويل المعادلة لصيغة Python: `{eq_text}`")
                    st.markdown("3️⃣ إنشاء كائن Sympy للمساواة:")
                    st.latex(latex(equation))
                    st.markdown("4️⃣ حل المعادلة باستخدام solve()")
                else:
                    st.markdown(f"✅ حل المعادلة: `{eq_input}`")

                for i, s in enumerate(solutions, start=1):
                    st.markdown(f"5.{i}️⃣ الحل: x = {s}")

                st.subheader("الحلول النهائية")
                for s in solutions:
                    st.latex(f"x = {latex(s)}")
        except Exception as e:
            st.error(f"❌ خطأ في حل المعادلة: {e}")

# ------------------------------------------------
# Tab 3: رسم الدوال
# ------------------------------------------------
with tab3:
    st.header("📊 رسم الدوال")
    func_text = st.text_input("أدخل الدالة (مثال: x^2 - 4*x + 3)")

    func_choice_plot = st.selectbox("أو اختر دالة جاهزة للرسم", english_functions)

    if func_choice_plot != "None":
        func_text = func_choice_plot

    if st.button("ارسم", key="plot"):
        try:
            f_sym = sympify(convert_math_to_python(func_text))
            f = lambdify(x, f_sym, "numpy")

            roots = solve(Eq(f_sym, 0), x)
            roots_real = []
            for r in roots:
                try:
                    val = float(r.evalf())
                    roots_real.append(val)
                except:
                    pass

            x_min = min(roots_real)-5 if roots_real else -10
            x_max = max(roots_real)+5 if roots_real else 10
            xs = np.linspace(x_min, x_max, 400)
            ys = f(xs)

            fig, ax = plt.subplots()
            ax.plot(xs, ys, linewidth=2, label=arabic_text(str(func_text)))
            ax.axhline(0, color="black")
            ax.axvline(0, color="black")
            ax.grid(True, linestyle="--", alpha=0.7)

            seen = set()
            for r in roots_real:
                if r not in seen:
                    ax.plot(r, 0, 'ro', label=arabic_text(f'الجذر x={r}'))
                    seen.add(r)

            ax.set_title(arabic_text(f"رسم الدالة: {func_text}"), fontsize=14)
            ax.set_xlabel(arabic_text("س"), fontsize=12)
            ax.set_ylabel(arabic_text("ص"), fontsize=12)
            ax.legend(fontsize=10)
            fig.tight_layout()

            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ خطأ في الدالة: {e}")
