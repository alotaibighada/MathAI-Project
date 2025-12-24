import streamlit as st
from sympy import symbols, Eq, solve, sympify, latex, expand, lambdify
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
# Tab 1: العمليات الحسابية
# ------------------------------------------------
with tab1:
    st.markdown("<h2 style='color:#1E90FF;'>🔢 العمليات الحسابية</h2>", unsafe_allow_html=True)

    a_num = st.number_input("العدد الأول", value=0.0)
    b_num = st.number_input("العدد الثاني", value=0.0)
    operation = st.selectbox("اختر العملية", ["جمع", "طرح", "ضرب", "قسمة"])

    if st.button("احسب", key="calc_btn"):
        if operation == "قسمة" and b_num == 0:
            st.error("❌ لا يمكن القسمة على صفر")
        else:
            result = {
                "جمع": a_num + b_num,
                "طرح": a_num - b_num,
                "ضرب": a_num * b_num,
                "قسمة": a_num / b_num
            }[operation]
            st.write(f"✅ النتيجة = {result}")

# ------------------------------------------------
# Tab 2: حل المعادلات
# ------------------------------------------------
with tab2:
    st.markdown("<h2 style='color:#32CD32;'>📐 حل المعادلات التربيعية</h2>", unsafe_allow_html=True)

    eq_input = st.text_input("أدخل المعادلة على شكل x^2-4x+3=0")

    if st.button("حل المعادلة", key="solve_btn"):
        try:
            if "=" not in eq_input:
                st.error("❌ يجب أن تحتوي المعادلة على =")
            else:
                python_eq = convert_math_to_python(eq_input)
                left, right = python_eq.split("=")
                equation = Eq(sympify(left), sympify(right))
                simplified = expand(equation.lhs - equation.rhs)

                st.write("المعادلة المبسطة:")
                st.latex(f"{latex(simplified)} = 0")

                solutions = solve(simplified, x)
                st.write("الحلول:")
                for i, sol in enumerate(solutions, 1):
                    st.latex(f"x_{i} = {latex(sol)}")

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
            if not func_text:
                st.warning("⚠ أدخل دالة أولاً")
            else:
                func_python = convert_math_to_python(func_text)
                f_sym = sympify(func_python)
                f = lambdify(x, f_sym, "numpy")

                xs = np.linspace(-10, 10, 400)
                ys = np.array([f(val) for val in xs])

                fig, ax = plt.subplots(figsize=(7,5))
                ax.plot(xs, ys, color="#FF6347", linewidth=2)
                ax.axhline(0, color='black', linewidth=1)
                ax.axvline(0, color='black', linewidth=1)
                ax.grid(True, linestyle='--', alpha=0.7)
                ax.set_title(func_text)
                ax.set_xlabel("x")
                ax.set_ylabel("y")

                st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ خطأ في الرسم: {e}")

# =====================
# Footer ثابت أسفل الصفحة
# =====================
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 14px;
        color: #888888;
        background-color: #F5F5F5;
        padding: 8px 0;
        box-shadow: 0 -1px 5px rgba(0,0,0,0.1);
        z-index: 100;
    }
    </style>
    <div class="footer">
        © 2025 Ghada Inc. | جميع الحقوق محفوظة
    </div>
    """,
    unsafe_allow_html=True
)
