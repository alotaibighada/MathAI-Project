import streamlit as st
from sympy import symbols, Eq, solve, sympify, latex, expand, lambdify
import numpy as np
import matplotlib.pyplot as plt
import re
import arabic_reshaper
from bidi.algorithm import get_display

# =====================
# إعداد الصفحة
# =====================
st.set_page_config(page_title="Math AI", layout="wide")
st.title("🧮 Math AI – مساعد الرياضيات التعليمي")

x = symbols("x")

# =====================
# دالة تصحيح العربية للرسم
# =====================
def arabic_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# =====================
# تحويل الصيغة الرياضية
# x^2-4x+3 → x**2-4*x+3
# =====================
def convert_math_to_python(text):
    text = text.replace(" ", "")
    text = text.replace("^", "**")
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)
    text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', text)
    return text

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

    a = st.number_input("العدد الأول", value=0.0)
    b = st.number_input("العدد الثاني", value=0.0)

    operation = st.selectbox("اختر العملية", ["جمع", "طرح", "ضرب", "قسمة"])

    if st.button("احسب"):
        if operation == "قسمة" and b == 0:
            st.error("❌ لا يمكن القسمة على صفر")
        else:
            result = {
                "جمع": a + b,
                "طرح": a - b,
                "ضرب": a * b,
                "قسمة": a / b
            }[operation]
            st.success(f"✅ النتيجة = {result}")

# ------------------------------------------------
# Tab 2: حل المعادلات
# ------------------------------------------------
with tab2:
    st.header("📐 حل المعادلات خطوة بخطوة")

    eq_input = st.text_input("أدخل المعادلة (مثال: x^2-4x+3=0)")

    if st.button("حل المعادلة"):
        try:
            if "=" not in eq_input:
                st.error("❌ يجب أن تحتوي المعادلة على =")
            else:
                st.subheader("🔹 الخطوة 1: المعادلة الأصلية")
                st.write(eq_input)

                python_eq = convert_math_to_python(eq_input)
                st.subheader("🔹 الخطوة 2: تحويل الصيغة")
                st.code(python_eq)

                left, right = python_eq.split("=")
                equation = Eq(sympify(left), sympify(right))

                st.subheader("🔹 الخطوة 3: تمثيل المعادلة رياضيًا")
                st.latex(latex(equation))

                simplified = expand(equation.lhs - equation.rhs)
                st.subheader("🔹 الخطوة 4: تبسيط المعادلة")
                st.latex(f"{latex(simplified)} = 0")

                solutions = solve(equation, x)
                st.subheader("🔹 الخطوة 5: الحلول")

                if not solutions:
                    st.warning("⚠ لا يوجد حلول حقيقية")
                else:
                    for i, sol in enumerate(solutions, start=1):
                        st.latex(f"x_{i} = {latex(sol)}")

        except Exception as e:
            st.error(f"❌ خطأ: {e}")

# ------------------------------------------------
# Tab 3: رسم الدوال (✔ تم الإصلاح)
# ------------------------------------------------
with tab3:
    st.header("📊 رسم الدوال")

    func_text = st.text_input("أدخل الدالة (مثال: x^2-4x+3)")

    if st.button("ارسم"):
        try:
            func_python = convert_math_to_python(func_text)
            f_sym = sympify(func_python)

            # ✔ الحل الصحيح هنا
            f = lambdify(x, f_sym, "numpy")

            xs = np.linspace(-10, 10, 400)
            ys = f(xs)

            roots = solve(Eq(f_sym, 0), x)
            roots_real = []
            for r in roots:
                try:
                    roots_real.append(float(r))
                except:
                    pass

            fig, ax = plt.subplots()
            ax.plot(xs, ys, linewidth=2)
            ax.axhline(0)
            ax.axvline(0)
            ax.grid(True, linestyle="--", alpha=0.7)

            for r in roots_real:
                ax.plot(r, 0, "ro")

            ax.set_title(arabic_text(f"رسم الدالة: {func_text}"))
            ax.set_xlabel(arabic_text("س"))
            ax.set_ylabel(arabic_text("ص"))

            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ خطأ في رسم الدالة: {e}")
