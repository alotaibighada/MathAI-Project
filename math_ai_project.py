import streamlit as st
from sympy import symbols, solve, sympify, latex, expand, factor
import numpy as np
import matplotlib.pyplot as plt
import re

# =====================
# إعداد الصفحة
# =====================
st.set_page_config(
    page_title="Math AI",
    layout="wide"
)

# =====================
# Header
# =====================
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #1E3C72, #2A5298);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    ">
        <h1 style='color:#ffffff;'>🧮 Math AI – أداة رياضية ذكية</h1>
        <p style='color:#C0C0C0;'>حل المعادلات، العمليات الحسابية، ورسم الدوال بسهولة</p>
    </div>
    """,
    unsafe_allow_html=True
)

x = symbols("x")

# =====================
# تحويل الصيغة الرياضية
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
# Tab 1: العمليات الحسابية (إيموجي ملونة)
# ------------------------------------------------
with tab1:
    st.markdown("<h2 style='color:#1E90FF;'>🔢 العمليات الحسابية</h2>", unsafe_allow_html=True)

    a_num = st.number_input("العدد الأول", value=0.0)
    b_num = st.number_input("العدد الثاني", value=0.0)

    operation = st.selectbox(
        "اختر العملية",
        ["🟢 جمع ➕", "🔴 طرح ➖", "🔵 ضرب ✖️", "🟣 قسمة ➗"]
    )

    if st.button("احسب", key="calc_btn"):
        if "قسمة" in operation and b_num == 0:
            st.error("❌ لا يمكن القسمة على صفر")
        else:
            result = {
                "🟢 جمع ➕": a_num + b_num,
                "🔴 طرح ➖": a_num - b_num,
                "🔵 ضرب ✖️": a_num * b_num,
                "🟣 قسمة ➗": a_num / b_num
            }[operation]

            st.write(f"✅ النتيجة = {result}")

# ------------------------------------------------
# Tab 2: حل المعادلات (اختيار بالأيقونات)
# ------------------------------------------------
with tab2:
    st.markdown("<h2 style='color:#32CD32;'>📐 حل المعادلات التربيعية</h2>", unsafe_allow_html=True)

    eq_input = st.text_input("أدخل المعادلة على شكل x^2-4x+3=0")

    method = st.radio(
        "اختر طريقة الحل:",
        ["🧩 التحليل", "📐 القانون العام", "🤖 الحل المباشر"],
        horizontal=True
    )

    if st.button("حل المعادلة", key="solve_btn"):
        try:
            if "=" not in eq_input:
                st.error("❌ يجب أن تحتوي المعادلة على =")
            else:
                python_eq = convert_math_to_python(eq_input)
                left, right = python_eq.split("=")
                expr = expand(sympify(left) - sympify(right))

                st.markdown("### ✏️ المعادلة بعد التبسيط")
                st.latex(f"{latex(expr)} = 0")

                a = expr.coeff(x, 2)
                b = expr.coeff(x, 1)
                c = expr.coeff(x, 0)

                # 🧩 التحليل
                if method == "🧩 التحليل":
                    st.markdown("## 🧩 الحل بالتحليل")
                    factored = factor(expr)
                    if factored != expr:
                        st.latex(f"{latex(factored)} = 0")
                        for sol in solve(factored, x):
                            st.latex(f"x = {latex(sol)}")
                    else:
                        st.warning("لا يمكن تحليل المعادلة")

                # 📐 القانون العام
                elif method == "📐 القانون العام":
                    st.markdown("## 📐 الحل بالقانون العام")
                    st.latex("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}")

                    delta = b**2 - 4*a*c
                    st.latex(f"\\Delta = {latex(delta)}")

                    if delta < 0:
                        st.warning("لا يوجد حلول حقيقية")
                    else:
                        x1 = (-b + delta**0.5) / (2*a)
                        x2 = (-b - delta**0.5) / (2*a)
                        st.latex(f"x_1 = {latex(x1)}")
                        st.latex(f"x_2 = {latex(x2)}")

                # 🤖 الحل المباشر
                elif method == "🤖 الحل المباشر":
                    st.markdown("## 🤖 الحل المباشر")
                    for sol in solve(expr, x):
                        st.latex(f"x = {latex(sol)}")

        except Exception as e:
            st.error(f"❌ خطأ: {e}")

# ------------------------------------------------
# Tab 3: رسم الدوال
# ------------------------------------------------
with tab3:
    st.markdown("<h2 style='color:#FF8C00;'>📊 رسم الدوال</h2>", unsafe_allow_html=True)

    func_text = st.text_input("أدخل الدالة على شكل x^2-4x+3")

    if st.button("ارسم", key="plot_btn"):
        try:
            func_python = convert_math_to_python(func_text)
            f_sym = sympify(func_python)

            xs = np.linspace(-10, 10, 400)
            ys = [f_sym.subs(x, val) for val in xs]

            fig, ax = plt.subplots(figsize=(7,5))
            ax.plot(xs, ys)
            ax.axhline(0)
            ax.axvline(0)
            ax.grid(True)

            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ خطأ في الرسم: {e}")

# =====================
# Footer
# =====================
st.markdown(
    """
    <div style="text-align:center;color:#888;font-size:14px;margin-top:30px;">
        © 2025 Ghada Inc. | جميع الحقوق محفوظة
    </div>
    """,
    unsafe_allow_html=True
)
