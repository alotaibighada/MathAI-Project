import streamlit as st
from sympy import symbols, Eq, solve, sympify, latex, lambdify
import numpy as np
import matplotlib.pyplot as plt
import re

# =====================
# إعداد الصفحة
# =====================
st.set_page_config(page_title="Math AI Project", layout="wide")
st.title("🧮 Math AI")

x = symbols("x")
mode = st.radio("اختر وضع الاستخدام:", ["👩‍🎓 وضع تعليمي", "👩‍🔬 وضع متقدم"])

# =====================
# تحويل الصياغة الرياضية
# =====================
def convert_math_to_python(text):
    text = text.replace("^", "**")
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)  # 2x → 2*x
    text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', text)  # x2 → x*2
    text = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', text)  # xy → x*y
    text = text.replace(" ", "")
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
# Tab 2: حل المعادلات بالتفصيل
# ------------------------------------------------
with tab2:
    st.header("📐 حل المعادلات خطوة خطوة")

    eq_input = st.text_input("أدخل المعادلة (مثال: x^2 - 4x + 3 = 0)")

    if st.button("حل المعادلة", key="solve"):
        try:
            if "=" not in eq_input:
                st.error("❌ يجب كتابة المعادلة وبها =")
            else:
                # تحويل المعادلة
                eq_text = convert_math_to_python(eq_input)
                left, right = eq_text.split("=")
                equation = Eq(sympify(left), sympify(right))
                
                # حل المعادلة
                solutions = solve(equation, x)

                # عرض خطوات الحل
                st.subheader("خطوات الحل:")
                st.markdown(f"1️⃣ تم إدخال المعادلة: `{eq_input}`")
                st.markdown(f"2️⃣ تحويل المعادلة لصيغة Python: `{eq_text}`")
                st.markdown(f"3️⃣ إنشاء كائن Sympy للمساواة:")
                st.latex(latex(equation))
                st.markdown("4️⃣ حل المعادلة باستخدام solve()")

                for i, s in enumerate(solutions, start=1):
                    st.markdown(f"5.{i}️⃣ وجدنا الحل: x = {s}")

                st.subheader("الحلول النهائية")
                for s in solutions:
                    st.latex(f"x = {latex(s)}")
        except Exception as e:
            st.error(f"❌ خطأ في حل المعادلة: {e}")

# ------------------------------------------------
# Tab 3: رسم الدوال مع تمييز الجذور
# ------------------------------------------------
with tab3:
    st.header("📊 رسم الدوال")

    func_text = st.text_input("أدخل الدالة (مثال: x^2 - 4x + 3)")

    if st.button("ارسم", key="plot"):
        try:
            # تحويل الدالة
            f_sym = sympify(convert_math_to_python(func_text))
            f = lambdify(x, f_sym, "numpy")

            # تحديد نطاق الرسم تلقائيًا بناءً على جذور الدالة
            roots = solve(Eq(f_sym, 0), x)
            roots_real = [float(r.evalf()) for r in roots if r.is_real]

            if roots_real:
                x_min = min(roots_real) - 5
                x_max = max(roots_real) + 5
            else:
                x_min, x_max = -10, 10

            xs = np.linspace(x_min, x_max, 400)
            ys = f(xs)

            # الرسم
            fig, ax = plt.subplots()
            ax.plot(xs, ys, linewidth=2, label=str(func_text))
            ax.axhline(0, color="black")
            ax.axvline(0, color="black")
            ax.grid(True, linestyle="--", alpha=0.7)

            # تمييز الجذور
            for r in roots_real:
                ax.plot(r, 0, 'ro', label=f'الجذر x={r}')

            # إعدادات الرسم بالعربية
            ax.set_title(f"رسم الدالة: {func_text}", fontsize=14)
            ax.set_xlabel("س", fontsize=12)
            ax.set_ylabel("ص", fontsize=12)
            ax.legend(fontsize=10)

            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ خطأ في الدالة: {e}")
