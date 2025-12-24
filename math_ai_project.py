import streamlit as st
from sympy import symbols, Eq, solve, sympify, latex, expand, sqrt, lambdify
import numpy as np
import matplotlib.pyplot as plt
import re

# =====================
# إعداد الصفحة
# =====================
st.set_page_config(page_title="Math AI", layout="wide")
st.title("🧮 Math AI")
st.caption("✦ مشروع تعليمي ذكي ✦")

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
    st.header("🔢 العمليات الحسابية")

    a_num = st.number_input("العدد الأول", value=0.0)
    b_num = st.number_input("العدد الثاني", value=0.0)
    operation = st.selectbox("اختر العملية", ["جمع", "طرح", "ضرب", "قسمة"])

    if st.button("احسب"):
        if operation == "قسمة" and b_num == 0:
            st.error("❌ لا يمكن القسمة على صفر")
        else:
            result = {
                "جمع": a_num + b_num,
                "طرح": a_num - b_num,
                "ضرب": a_num * b_num,
                "قسمة": a_num / b_num
            }[operation]
            st.success(f"✅ النتيجة = {result}")

# ------------------------------------------------
# Tab 2: حل المعادلات
# ------------------------------------------------
with tab2:
    st.header("📐 حل المعادلات التربيعية خطوة بخطوة")

    eq_input = st.text_input("أدخل المعادلة (مثال: x^2-4x+3=0)")
    method = st.radio(
        "اختر طريقة الحل:",
        ["التحليل", "القانون العام", "حل تلقائي"]
    )

    if st.button("حل المعادلة"):
        try:
            if "=" not in eq_input:
                st.error("❌ يجب أن تحتوي المعادلة على =")
            else:
                st.subheader("1️⃣ المعادلة المعطاة")
                st.write(eq_input)

                python_eq = convert_math_to_python(eq_input)
                left, right = python_eq.split("=")
                equation = Eq(sympify(left), sympify(right))
                simplified = expand(equation.lhs - equation.rhs)

                st.subheader("2️⃣ الصورة العامة")
                st.latex(f"{latex(simplified)} = 0")

                poly = simplified.as_poly(x)

                if poly is None or poly.degree() != 2:
                    st.warning("⚠ هذه المعادلة ليست تربيعية")
                else:
                    # استخراج المعاملات بأمان
                    a = poly.coeff_monomial(x**2)
                    b = poly.coeff_monomial(x)
                    c = poly.coeff_monomial(1)

                    st.markdown(f"""
                    **المعاملات**
                    - a = {a}
                    - b = {b}
                    - c = {c}
                    """)

                    st.subheader("3️⃣ الحل")

                    if method == "القانون العام":
                        D = b**2 - 4*a*c
                        st.latex(r"\Delta = b^2 - 4ac")
                        st.latex(f"\\Delta = {latex(D)}")
                        solutions = [
                            (-b + sqrt(D)) / (2*a),
                            (-b - sqrt(D)) / (2*a)
                        ]
                    else:
                        solutions = solve(simplified, x)

                    st.subheader("4️⃣ الحلول")
                    for i, sol in enumerate(solutions, 1):
                        st.latex(f"x_{i} = {latex(sol)}")

                    st.success("✔ تم حل المعادلة بنجاح")

        except Exception as e:
            st.error(f"❌ خطأ: {e}")

# ------------------------------------------------
# Tab 3: رسم الدوال
# ------------------------------------------------
with tab3:
    st.header("📊 رسم الدوال")

    func_text = st.text_input("أدخل الدالة (مثال: x^2-4x+3)")

    if st.button("ارسم"):
        try:
            if not func_text:
                st.warning("⚠ أدخل دالة أولاً")
            else:
                func_python = convert_math_to_python(func_text)
                f_sym = sympify(func_python)

                f = lambdify(x, f_sym, "numpy")
                xs = np.linspace(-10, 10, 400)
                ys = f(xs)

                fig, ax = plt.subplots()
                ax.plot(xs, ys, linewidth=2)
                ax.axhline(0)
                ax.axvline(0)
                ax.grid(True)

                ax.set_title(f"= {func_text}")
                ax.set_xlabel("x")
                ax.set_ylabel("y")

                st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ خطأ في الرسم: {e}")
