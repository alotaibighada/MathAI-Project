import streamlit as st
from sympy import symbols, Eq, solve, sympify, degree
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Math AI Project", layout="wide")
st.title("🧮 Math AI – مشروع علمي ذكي")

x = symbols("x")

mode = st.radio("اختر وضع الاستخدام:", ["👩‍🎓 وضع تعليمي", "👩‍🔬 وضع متقدم"])

# =====================
# العمليات الحسابية
# =====================
st.header("🔢 العمليات الحسابية")
a = st.number_input("الرقم الأول", value=0)
b = st.number_input("الرقم الثاني", value=0)
op = st.selectbox("العملية", ["جمع", "طرح", "ضرب", "قسمة"])

if st.button("احسب"):
    if op == "جمع":
        r = a + b
    elif op == "طرح":
        r = a - b
    elif op == "ضرب":
        r = a * b
    elif op == "قسمة":
        if b == 0:
            st.error("لا يمكن القسمة على صفر")
            r = None
        else:
            r = a / b
    if r is not None:
        st.success(f"النتيجة = {r}")
        if mode == "👩‍🎓 وضع تعليمي":
            st.info("تم تطبيق العملية الحسابية على الرقمين مباشرة")

# =====================
# حل المعادلات خطوة بخطوة
# =====================
st.header("📐 حل المعادلات خطوة بخطوة")
eq_text = st.text_input(" 2*x + 5 = 15")

if st.button("حل المعادلة"):
    try:
        left, right = eq_text.split("=")
        eq = Eq(sympify(left), sympify(right))
        sol = solve(eq, x)

        if mode == "👩‍🎓 وضع تعليمي":
            st.write("🔹 الخطوة 1: المعادلة الأصلية")
            st.write(eq_text)
            st.write("🔹 الخطوة 2: حل المعادلة")
        st.success(f"الحل النهائي: x = {sol}")
    except:
        st.error("صيغة المعادلة غير صحيحة")

# =====================
# رسم الدوال + تحليل
# =====================
st.header("📊 رسم وتحليل الدوال")

example = st.button("✨ جرب مثال جاهز")
func_text = "x**2 - 4*x + 3" if example else st.text_input("x**2 - 4*x + 3")

if st.button("ارسم الدالة"):
    try:
        f = sympify(func_text)
        xs = np.linspace(-10, 10, 400)
        ys = [float(f.subs(x, i)) for i in xs]

        deg = degree(f)
        if deg == 1:
            dtype = "خطية"
        elif deg == 2:
            dtype = "تربيعية"
        elif deg == 3:
            dtype = "تكعيبية"
        else:
            dtype = "غير محددة"

        st.info(f"🔍 نوع الدالة: {dtype}")

        fig, ax = plt.subplots()
        ax.plot(xs, ys, label="الدالة")
        ax.axhline(0)
        ax.axvline(0)

        roots = solve(f, x)
        for r in roots:
            if r.is_real:
                ax.scatter(float(r), 0)

        ax.legend()
        st.pyplot(fig)

        if mode == "👩‍🎓 وضع تعليمي":
            st.write("📍 تم تحديد نقاط التقاطع مع المحاور")

understand = st.radio(
    "🤔 هل فهمت شكل الدالة؟",
    ["— اختر —", "👍 نعم، فهمت", "❓ لا، أحتاج شرح"]
)
if understand == "👍 نعم، فهمت":
    st.success("🎉 ممتاز! هذا يدل على فهمك لشكل الدالة والعلاقة بين x و y")

elif understand == "❓ لا، أحتاج شرح":
    st.info("""
    🔍 شرح مبسّط:
    • المنحنى يوضّح كيف تتغير قيمة y عند تغيير x  
    • نقاط التقاطع تمثل حلول الدالة  
    • شكل المنحنى يساعد على التنبؤ بالسلوك
    """)

    except:
        st.error("خطأ في الدالة")
