
import streamlit as st
from sympy import symbols, Eq, solve, sympify
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Math AI Project", layout="wide")
st.title("🧮 Math AI – مشروع علمي ذكي")

st.markdown("""
<style>
.stApp {background-color: #f5faff;}
.stButton>button {height:3em; font-size:1.1em; font-weight:bold; border-radius:10px;}
.success-box {background-color: rgba(0,200,0,0.3); padding:10px; border-radius:10px;}
.error-box {background-color: rgba(200,0,0,0.3); padding:10px; border-radius:10px;}
.step-box {background-color: rgba(0,0,200,0.2); padding:10px; border-radius:10px;}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

st.header("🔢 العمليات الحسابية")
num1 = st.number_input("الرقم الأول", value=0)
num2 = st.number_input("الرقم الثاني", value=0)
op = st.selectbox("اختر العملية", ["جمع","طرح","ضرب","قسمة"])

if st.button("احسب"):
    try:
        if op=="جمع": r=num1+num2
        elif op=="طرح": r=num1-num2
        elif op=="ضرب": r=num1*num2
        elif op=="قسمة":
            if num2==0: st.error("لا يمكن القسمة على صفر"); r=None
            else: r=num1/num2
        if r is not None:
            st.success(f"النتيجة = {r}")
            st.session_state.history.append(f"{num1} {op} {num2} = {r}")
    except:
        st.error("خطأ في العملية")

st.header("📐 حل المعادلات")
x = symbols("x")
eq = st.text_input("اكتب معادلة مثل: 2*x+5=15")
if st.button("حل المعادلة"):
    try:
        l,r = eq.split("=")
        sol = solve(Eq(sympify(l), sympify(r)), x)
        st.success(f"الحل: {sol}")
        st.session_state.history.append(f"{eq} -> {sol}")
    except:
        st.error("صيغة المعادلة غير صحيحة")

st.header("📊 رسم الدوال")
func = st.text_input("دالة مثل: x**2 - 4*x")
if st.button("ارسم"):
    try:
        f = sympify(func)
        xs = np.linspace(-10,10,400)
        ys = [float(f.subs(x,i)) for i in xs]
        fig, ax = plt.subplots()
        ax.plot(xs,ys)
        ax.axhline(0); ax.axvline(0)
        st.pyplot(fig)
    except:
        st.error("خطأ في الدالة")

if st.session_state.history:
    st.header("📜 السجل")
    for h in reversed(st.session_state.history):
        st.write(h)
