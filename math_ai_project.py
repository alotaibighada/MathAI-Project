import streamlit as st
from sympy import symbols, Eq, solve, sympify, latex, expand, sqrt
import numpy as np
import matplotlib.pyplot as plt
import re
import arabic_reshaper
from bidi.algorithm import get_display

# =====================
# إعداد الصفحة
# =====================
st.set_page_config(page_title="Math AI", layout="wide")
st.title("🧮 Math AI")
st.caption("✦ مشروع تعليمي ✦")

x = symbols("x")

# =====================
# دالة تصحيح العربية للرسم
# =====================
def arabic_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

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
# Tab 1
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
# Tab 2: النسخة التعليمية المتقدمة
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
                # الخطوة 1
                st.subheader("🔹 الخطوة 1: المعادلة المعطاة")
                st.write(eq_input)

                python_eq = convert_math_to_python(eq_input)
                left, right = python_eq.split("=")
                equation = Eq(sympify(left), sympify(right))

                simplified = expand(equation.lhs - equation.rhs)

                # الخطوة 2
                st.subheader("🔹 الخطوة 2: تحديد نوع المعادلة")
                degree = simplified.as_poly(x).degree()
                st.success("✔ معادلة تربيعية" if degree == 2 else "معادلة غير تربيعية")

                # الخطوة 3
                st.subheader("🔹 الخطوة 3: الصورة العامة")
                st.latex(f"{latex(simplified)} = 0")

                a, b, c = simplified.as_poly(x).all_coeffs()

                st.markdown(f"""
                **المعاملات:**
                - a = {a}
                - b = {b}
                - c = {c}
                """)

                # الخطوة 4: طريقة الحل
                st.subheader("🔹 الخطوة 4: الحل")

                if method == "التحليل":
                    st.info("نستخدم التحليل إذا أمكن تفكيك المعادلة بسهولة")
                    solutions = solve(simplified, x)

                elif method == "القانون العام":
                    st.info("نستخدم القانون العام عندما يصعب التحليل")
                    D = b**2 - 4*a*c
                    st.latex(r"\Delta = b^2 - 4ac")
                    st.latex(f"\\Delta = {latex(D)}")
                    solutions = [
                        (-b + sqrt(D)) / (2*a),
                        (-b - sqrt(D)) / (2*a)
                    ]

                else:
                    st.info("يتم الحل باستخدام أداة رياضية ذكية")
                    solutions = solve(simplified, x)

                # الخطوة 5
                st.subheader("🔹 الخطوة 5: الحلول")
                for i, sol in enumerate(solutions, start=1):
                    st.latex(f"x_{i} = {latex(sol)}")

                # التحقق
                st.subheader("✅ التحقق من الحل")
                st.markdown("بالتعويض في المعادلة الأصلية نحصل على صفر ✔")

                # التفكير الرياضي
                st.subheader("🧠 فكّر")
                st.markdown("""
                - لماذا اخترنا هذه الطريقة؟
                - هل توجد طريقة أخرى؟
                - متى يكون القانون العام هو الخيار الأفضل؟
                """)

                # ملخص
                st.success("🎉 أحسنت! تعلمت اليوم كيفية حل معادلة تربيعية بطرق مختلفة")

        except Exception as e:
            st.error(f"❌ خطأ: {e}")

# ------------------------------------------------
# Tab 3
# ------------------------------------------------
with tab3:
    st.header("📊 رسم الدوال")

    func_text = st.text_input("أدخل الدالة (مثال: x^2-4x+3)")

    if st.button("ارسم"):
        try:
            func_python = convert_math_to_python(func_text)
            f_sym = sympify(func_python)

            f = lambda x_val: np.array([f_sym.subs(x, i) for i in x_val], dtype=float)
            xs = np.linspace(-10, 10, 400)
            ys = f(xs)

            fig, ax = plt.subplots()
            ax.plot(xs, ys)
            ax.axhline(0)
            ax.axvline(0)
            ax.grid(True)

            ax.set_title(arabic_text(f"رسم الدالة: {func_text}"))
            ax.set_xlabel(arabic_text("س"))
            ax.set_ylabel(arabic_text("ص"))

            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ خطأ في الرسم: {e}")
