import streamlit as st
from sympy import symbols, Eq, solve, sympify, expand
import numpy as np
import matplotlib.pyplot as plt
import re
import random

# =====================
# إعداد الصفحة
# =====================
st.set_page_config(
    page_title="Math AI",
    layout="wide"
)

# =====================
# Header مع خلفية تقنية
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
# عبارات تشجيعية
# =====================
encouragement_messages = [
    "🎉 رائع! لقد تمكنت من حل المعادلة بنجاح. كل خطوة تقربك أكثر لفهم الرياضيات!",
    "💡 تذكّر: دلتا (Δ) تحدد عدد الحلول الحقيقية أو المركبة للمعادلة التربيعية.",
    "✨ ممتاز! كل عملية حسابية تتقنها تزيد من مهارتك الرياضية!",
    "🧠 فهم المعادلات خطوة مهمة للوصول إلى حلول دقيقة ومبتكرة!",
]

# =====================
# Tab: حل المعادلات
# =====================
st.markdown("<h2 style='color:#32CD32;'>📐 حل المعادلات التربيعية</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#555;'>أدخل المعادلة على شكل <b>x^2-4x+3=0</b>:</p>", unsafe_allow_html=True)

eq_input = st.text_input("أدخل المعادلة")
method = st.radio(
    "اختر طريقة الحل:",
    ["القانون العام", "حل تلقائي"]
)

if st.button("حل المعادلة"):
    try:
        if "=" not in eq_input:
            st.error("❌ يجب أن تحتوي المعادلة على =")
        else:
            st.markdown("<h4 style='color:#4B0082;'>1️⃣ المعادلة المعطاة</h4>", unsafe_allow_html=True)
            st.write(eq_input)

            python_eq = convert_math_to_python(eq_input)
            left, right = python_eq.split("=")
            equation = Eq(sympify(left), sympify(right))
            simplified = expand(equation.lhs - equation.rhs)

            st.markdown("<h4 style='color:#4B0082;'>2️⃣ الصورة العامة</h4>", unsafe_allow_html=True)
            st.latex(f"{simplified} = 0")

            # حل المعادلة (يدعم المركبات)
            solutions = solve(simplified, x)

            st.markdown("<h4 style='color:#32CD32;'>3️⃣ الحلول</h4>", unsafe_allow_html=True)
            for i, sol in enumerate(solutions, 1):
                # تحويل الجزء الحقيقي والتخيلي إلى أرقام عشرية
                real_part = float(sol.as_real_imag()[0])
                imag_part = float(sol.as_real_imag()[1])
                if imag_part == 0:
                    sol_str = f"{real_part:.3f}"
                else:
                    sol_str = f"{real_part:.3f} {'+' if imag_part>0 else '-'} {abs(imag_part):.3f}i"
                st.markdown(f"<span style='color:#FF6347; font-weight:bold;'>x_{i} = {sol_str}</span>", unsafe_allow_html=True)

            st.success("✔ تم حل المعادلة بنجاح")

            # عرض عبارة تشجيعية عشوائية
            st.info(random.choice(encouragement_messages))

    except Exception as e:
        st.error(f"❌ خطأ: {e}")
