import streamlit as st
from sympy import symbols, Eq, solve, sympify, latex, lambdify
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import re

# =====================
# إعداد الخط في Matplotlib
# =====================
rcParams['font.family'] = 'Arial'
rcParams['axes.unicode_minus'] = False

# =====================
# إعداد الصفحة
# =====================
st.set_page_config(page_title="Math AI Project", layout="wide")

# =====================
# شعار المشروع
# =====================
st.image("logo.png", width=180)
st.markdown("<h2 style='text-align:center;'>Math AI</h2>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:gray;'>مساعد ذكي لتعلم الرياضيات</p>",
    unsafe_allow_html=True
)
st.divider()

x = symbols("x")
mode = st.radio("اختر وضع الاستخدام:", ["👩‍🎓 وضع تعليمي", "👩‍🔬 وضع متقدم"])

# =====================
# تحويل الصيغة الرياضية
# =====================
def convert_math_to_python(text):
    text = text.replace(" ", "")
    text = text.replace("^", "**")
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)
    text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', text)
    text = re.sub(r'([a-zA-Z])\(', r'\1*(', text)
    text = re.sub(r'\)\(', r')*(', text)
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

# ------------------------------------------------
# Tab 2: حل المعادلات مع الشرح
# ------------------------------------------------
with tab2:
    st.header("📐 حل المعادلات خطوة بخطوة")
    eq_input = st.text_input("أدخل المعادلة (مثال: x^2-4x+3=0)")

    if st.button("حل المعادلة"):
        try:
            if "=" not in eq_input:
                st.error("❌ يجب أن تحتوي المعادلة على =")
            else:
                eq_text = convert_math_to_python(eq_input)
                left, right = eq_text.split("=")
                equation = Eq(sympify(left), sympify(right))
                solutions = solve(equation, x)

                if mode == "👩‍🎓 وضع تعليمي":
                    st.subheader("🔍 خطوات الحل")
                    st.markdown(f"**1️⃣ المعادلة المدخلة:** `{eq_input}`")
                    st.markdown(f"**2️⃣ بعد التحويل البرمجي:** `{eq_text}`")
                    st.markdown("**3️⃣ نقل جميع الحدود لطرف واحد:**")
                    st.latex(latex(equation))
                    st.markdown("**4️⃣ حل المعادلة:**")

                st.subheader("✅ الحل النهائي")
                for s in solutions:
                    st.latex(f"x = {latex(s)}")

        except Exception as e:
            st.error(f"❌ خطأ في المعادلة: {e}")

# ------------------------------------------------
# Tab 3: رسم الدوال
# ------------------------------------------------
with tab3:
    st.header("📊 رسم الدوال")
    func_text = st.text_input("أدخل الدالة (مثال: x^2-4x+3)")

    if st.button("ارسم الدالة"):
        try:
            f_sym = sympify(convert_math_to_python(func_text))
            f = lambdify(x, f_sym, "numpy")

            roots = solve(Eq(f_sym, 0), x)
            real_roots = []
            for r in roots:
                try:
                    real_roots.append(float(r))
                except:
                    pass

            x_min = min(real_roots) - 5 if real_roots else -10
            x_max = max(real_roots) + 5 if real_roots else 10

            xs = np.linspace(x_min, x_max, 400)
            ys = f(xs)

            fig, ax = plt.subplots()
            ax.plot(xs, ys, linewidth=2)
            ax.axhline(0, color="black")
            ax.axvline(0, color="black")
            ax.grid(True, linestyle="--", alpha=0.7)

            for r in real_roots:
                ax.plot(r, 0, "ro")

            ax.set_title(f"رسم الدالة: {func_text}")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            fig.tight_layout()

            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ خطأ في الدالة: {e}")
