import streamlit as st
from sympy import symbols, Eq, solve, sympify, latex, expand, sqrt, lambdify
import numpy as np
import matplotlib.pyplot as plt
import re
import arabic_reshaper
from bidi.algorithm import get_display
from matplotlib import font_manager

st.set_page_config(page_title="Math AI", layout="wide")

st.markdown("<h1 style='text-align:center; color:#4B0082;'>🧮 Math AI – أداة رياضية ذكية</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#6A5ACD;'>حل المعادلات، العمليات الحسابية، ورسم الدوال بسهولة</p>", unsafe_allow_html=True)

x = symbols("x")

def convert_math_to_python(text):
    text = text.replace(" ", "")
    text = text.replace("^", "**")
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)
    text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', text)
    return text

arabic_font_path = "./Amiri-Regular.ttf"
try:
    font_prop = font_manager.FontProperties(fname=arabic_font_path)
except:
    font_prop = None

def arabic_text(text):
    if not text:
        return ""
    reshaped_text = arabic_reshaper.reshape(str(text))
    bidi_text = get_display(reshaped_text)
    return bidi_text

tab1, tab2, tab3 = st.tabs([
    "🔢 العمليات الحسابية",
    "📐 حل المعادلات",
    "📊 رسم الدوال"
])

with tab1:
    a_num = st.number_input("العدد الأول", value=0.0)
    b_num = st.number_input("العدد الثاني", value=0.0)
    operation = st.selectbox("اختر العملية", ["جمع 🟢", "طرح 🔴", "ضرب ✖️", "قسمة ➗"])
    if st.button("احسب", key="calc_btn"):
        if operation.startswith("قسمة") and b_num == 0:
            st.error("❌ لا يمكن القسمة على صفر")
        else:
            result = {
                "جمع 🟢": a_num + b_num,
                "طرح 🔴": a_num - b_num,
                "ضرب ✖️": a_num * b_num,
                "قسمة ➗": a_num / b_num
            }[operation]
            st.markdown(f"<span style='color:#FF4500; font-weight:bold;'>✅ النتيجة = {result}</span>", unsafe_allow_html=True)

with tab2:
    eq_input = st.text_input("أدخل المعادلة")
    method = st.radio("اختر طريقة الحل:", ["التحليل", "القانون العام", "حل تلقائي"])
    if st.button("حل المعادلة", key="solve_btn"):
        try:
            if "=" not in eq_input:
                st.error("❌ يجب أن تحتوي المعادلة على =")
            else:
                python_eq = convert_math_to_python(eq_input)
                left, right = python_eq.split("=")
                equation = Eq(sympify(left), sympify(right))
                simplified = expand(equation.lhs - equation.rhs)
                poly = simplified.as_poly(x)
                if poly is None or poly.degree() != 2:
                    st.warning("⚠ هذه المعادلة ليست تربيعية")
                else:
                    a = poly.coeff_monomial(x**2)
                    b = poly.coeff_monomial(x)
                    c = poly.coeff_monomial(1)
                    if method == "القانون العام":
                        D = b**2 - 4*a*c
                        solutions = [(-b + sqrt(D)) / (2*a), (-b - sqrt(D)) / (2*a)]
                    else:
                        solutions = solve(simplified, x)
                    for i, sol in enumerate(solutions, 1):
                        st.markdown(f"<span style='color:#FF6347; font-weight:bold;'>{arabic_text(f'x_{i} = {sol}')}</span>", unsafe_allow_html=True)
                    st.success("✔ تم حل المعادلة بنجاح")

 with tab3:
    func_text = st.text_input("أدخل الدالة")
    if st.button("ارسم", key="plot_btn"):
        try:
            if func_text:
                func_python = convert_math_to_python(func_text)
                f_sym = sympify(func_python)
                f = lambdify(x, f_sym, "numpy")
                xs = np.linspace(-10, 10, 400)
                ys = f(xs)
                fig, ax = plt.subplots(figsize=(7,5))
                ax.plot(xs, ys, color="#FF6347", linewidth=2, label="الدالة")
                ax.axhline(0, color='black', linewidth=1)
                ax.axvline(0, color='black', linewidth=1)
                ax.set_facecolor("#F5F5F5")
                ax.grid(True, linestyle='--', alpha=0.7)
                if font_prop:
                    try:
                        plt.rcParams['font.family'] = font_prop.get_name()
                        ax.set_title(arabic_text(f"رسم الدالة: {func_text}"), fontsize=14, color="#4B0082")
                        ax.set_xlabel(arabic_text("س"), fontsize=12)
                        ax.set_ylabel(arabic_text("ص"), fontsize=12)
                        ax.legend([arabic_text("الدالة")])
                    except:
                        ax.set_title(f"رسم الدالة: {func_text}", fontsize=14, color="#4B0082")
                        ax.set_xlabel("س", fontsize=12)
                        ax.set_ylabel("ص", fontsize=12)
                        ax.legend(["الدالة"])
                else:
                    ax.set_title(f"رسم الدالة: {func_text}", fontsize=14, color="#4B0082")
                    ax.set_xlabel("س", fontsize=12)
                    ax.set_ylabel("ص", fontsize=12)
                    ax.legend(["الدالة"])
                fig.tight_layout()
                st.pyplot(fig)
        except Exception as e:
            st.error(f"❌ خطأ في الرسم: {e}")
