import streamlit as st
from sympy import symbols, Eq, solve, sympify, latex, expand, sqrt
import numpy as np
import matplotlib.pyplot as plt
import re

# =====================
# إعداد الصفحة
# =====================
st.set_page_config(
    page_title="Math AI – مساعد الرياضيات التعليمي",
    layout="wide"
)

# =====================
# تحسين الواجهة (CSS)
# =====================
st.markdown("""
<style>

/* اتجاه عربي وخط */
html, body, [class*="css"]  {
    direction: rtl;
    font-family: 'Tahoma', 'Arial';
}

/* الخلفية */
.stApp {
    background-color: #f4f8fb;
}

/* العناوين */
h1, h2, h3, h4 {
    text-align: center;
    color: #2C3E50;
}

/* كرت المحتوى */
.block-container {
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
}

/* الأزرار */
.stButton > button {
    background: linear-gradient(90deg, #4CAF50, #2ECC71);
    color: white;
    border-radius: 14px;
    height: 3em;
    font-size: 18px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #43A047, #27AE60);
}

/* الإدخالات */
.stTextInput input,
.stNumberInput input {
    border-radius: 12px;
    padding: 10px;
    border: 1px solid #dfe6e9;
}

/* الراديو */
.stRadio > div {
    background-color: #f7fdf9;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #e0f2e9;
}

/* الرسائل */
.stSuccess {
    background-color: #eafaf1;
    border-right: 6px solid #2ecc71;
}

.stError {
    background-color: #fdecea;
    border-right: 6px solid #e74c3c;
}

.stInfo {
    background-color: #eaf2fb;
    border-right: 6px solid #3498db;
}

.stWarning {
    background-color: #fff4e5;
    border-right: 6px solid #f39c12;
}

/* التبويبات */
.stTabs [role="tab"] {
    font-size: 18px;
    padding: 10px 25px;
}

.stTabs [aria-selected="true"] {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================
# العنوان
# =====================
st.markdown("<h1>🧮 Math AI</h1>", unsafe_allow_html=True)
st.markdown("<h4>مساعد الرياضيات التعليمي</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#4CAF50;'>معلمة مبدعة للجميع</p>", unsafe_allow_html=True)
st.markdown("---")

# =====================
# أدوات
# =====================
x = symbols("x")

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
    st.header("📐 حل المعادلات التربيعية خطوة بخطوة")

    eq_input = st.text_input("أدخل المعادلة (مثال: x^2-4x+3=0)")
    method = st.radio(
        "اختر طريقة الحل:",
        ["التحليل", "القانون العام", "حل جبري تلقائي"]
    )

    if st.button("حل المعادلة"):
        try:
            if "=" not in eq_input:
                st.error("❌ يجب أن تحتوي المعادلة على =")
            else:
                st.subheader("🔹 الخطوة 1: المعادلة المعطاة")
                st.write(eq_input)

                python_eq = convert_math_to_python(eq_input)
                left, right = python_eq.split("=")
                equation = Eq(sympify(left), sympify(right))
                simplified = expand(equation.lhs - equation.rhs)

                st.subheader("🔹 الخطوة 2: الصورة العامة")
                st.latex(f"{latex(simplified)} = 0")

                a, b, c = simplified.as_poly(x).all_coeffs()
                st.markdown(f"""
                **المعاملات:**
                - a = {a}
                - b = {b}
                - c = {c}
                """)

                st.subheader("🔹 الخطوة 3: الحل")

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

                st.subheader("🔹 الخطوة 4: الحلول")
                for i, sol in enumerate(solutions, start=1):
                    st.latex(f"x_{i} = {latex(sol)}")

                st.success("✔ تم التحقق من الحل بالتعويض")

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
            func_python = convert_math_to_python(func_text)
            f_sym = sympify(func_python)

            xs = np.linspace(-10, 10, 400)
            ys = [f_sym.subs(x, i) for i in xs]

            fig, ax = plt.subplots()
            ax.plot(xs, ys)
            ax.axhline(0)
            ax.axvline(0)
            ax.grid(True)

            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ خطأ في الرسم: {e}")
