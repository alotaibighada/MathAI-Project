import streamlit as st
from sympy import symbols, Eq, solve, sympify, degree, diff
import matplotlib.pyplot as plt
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display

# =====================
# إعداد الصفحة
# =====================
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
    r = None
    if op == "جمع":
        r = a + b
    elif op == "طرح":
        r = a - b
    elif op == "ضرب":
        r = a * b
    elif op == "قسمة":
        if b == 0:
            st.error("❌ لا يمكن القسمة على صفر")
        else:
            r = a / b
    if r is not None:
        st.success(f"✅ النتيجة = {r}")
        if mode == "👩‍🎓 وضع تعليمي":
            st.info("💡 تم تطبيق العملية الحسابية على الرقمين مباشرة")

# =====================
# حل المعادلات خطوة بخطوة
# =====================
st.header("📐 حل المعادلات خطوة بخطوة")
eq_text = st.text_input("أدخل المعادلة (
