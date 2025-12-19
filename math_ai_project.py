import streamlit as st
from sympy import symbols, Eq, solve, sympify, diff, sin, cos, exp, log, integrate, latex
import numpy as np
import plotly.graph_objs as go
import arabic_reshaper
from bidi.algorithm import get_display
import re

# =====================
# إعداد الصفحة
# =====================
st.set_page_config(page_title="Math AI Project", layout="wide")
st.title("🧮 Math AI – مساعد رياضي ذكي")

x = symbols("x")
mode = st.radio("اختر وضع الاستخدام:", ["👩‍🎓 وضع تعليمي", "👩‍🔬 وضع متقدم"])

# =====================
# تحويل صياغة المستخدم إلى SymPy
# =====================
def convert_math_to_python(text):
    text = text.replace(' ', '')
    text = re.sub(r'\^(\d+)', r'**\1', text)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)
    text = re.sub(r'([a-zA-Z])(\d+)', r'\1*\2', text)
    return text

# =====================
# توليد شرح ذكي بالعربي (AI مبسط)
# =====================
def generate_explanation(eq, solutions):
    explanations = []
    lhs = eq.lhs
    rhs = eq.rhs
    explanations.append(f"نقلنا جميع الحدود للحصول على صفر: {latex(lhs - rhs)} = 0")
    for i, sol in enumerate(solutions, start=1):
        explanations.append(f"الحل رقم {i}: x = {latex(sol)}")
    return explanations

# =====================
# Tabs
# =====================
tab1, tab2, tab3 = st.tabs([
    "🔢 العمليات الحسابية",
    "📐 حل المعادلات",
    "📊 رسم وتحليل الدوال"
])

# ---------------------
# Tab 1: العمليات الحسابية
# ---------------------
with tab1:
    st.header("🔢 العمليات الحسابية")
    a = st.number_input("الرقم الأول", value=0)
    b = st.number_input("الرقم الثاني", value=0)
    op = st.selectbox("العملية", ["جمع", "طرح", "ضرب", "قسمة"])

    if st.button("احسب"):
        try:
            if op == "جمع":
                r = a + b
            elif op == "طرح":
                r = a - b
            elif op == "ضرب":
                r = a * b
            elif op == "قسمة":
                if b == 0:
                    st.error("❌ لا يمكن القسمة على صفر")
                    r = None
                else:
                    r = a / b
            if r is not None:
                st.success(f"✅ النتيجة = {r}")
                if mode == "👩‍🎓 وضع تعليمي":
                    st.info("💡 تم تطبيق العملية الحسابية على الرقمين مباشرة")
        except Exception as e:
            st.error(f"❌ خطأ أثناء الحساب: {e}")

# ---------------------
# Tab 2: حل المعادلات مع شرح AI
# ---------------------
with tab2:
    st.header("📐 حل المعادلات خطوة بخطوة")
    eq_text_input = st.text_input("أدخل المعادلة (مثال: x^2 - 4x + 3 = 0)")
    example_eq = st.button("✨ جرب مثال جاهز")

    if example_eq:
        eq_text_input = "x^2 - 4*x + 3 = 0"

    if st.button("حل المعادلة"):
        try:
            eq_text = convert_math_to_python(eq_text_input)
            if "=" not in eq_text:
                st.error("❌ يجب أن تحتوي المعادلة على '='")
                st.stop()
            left, _, right = eq_text.partition("=")
            eq = Eq(sympify(left), sympify(right))
            sol = solve(eq, x)

            if mode == "👩‍🎓 وضع تعليمي":
                st.write("🔹 المعادلة الأصلية:", eq_text_input)
                lhs_simplified = sympify(left) - sympify(right)
                st.write("🔹 بعد النقل للحصول على 0:")
                st.latex(Eq(lhs_simplified, 0))
                st.write("🔹 شرح AI خطوة بخطوة:")
                for line in generate_explanation(eq, sol):
                    st.markdown(f"- {line}")

            st.success(f"✅ الحل النهائي: x = {[latex(s) for s in sol]}")

        except Exception as e:
            st.error(f"❌ صيغة المعادلة غير صحيحة: {e}")

# ---------------------
# Tab 3: رسم وتحليل الدوال مع AI
# ---------------------
with tab3:
    st.header("📊 رسم وتحليل الدوال تفاعلي")
    func_text_input = st.text_input("أدخل الدالة (مثال: x^2 - 4x + 3)")
    x_min, x_max = st.slider("اختر نطاق x", -100, 100, (-10, 10))
    y_min, y_max = st.slider("اختر نطاق y", -100, 100, (-10, 10))
    color = st.color_picker("اختر لون المنحنى", "#1f77b4")
    example_func = st.button("✨ جرب مثال جاهز")
    draw_button = st.button("ارسم الدالة")

    if example_func:
        func_text_input = "x^2 - 4*x + 3"

    func_text = func_text_input

    if draw_button:
        try:
            func_text_sympy = convert_math_to_python(func_text)
            allowed_functions = {"sin": sin, "cos": cos, "exp": exp, "log": log, "sqrt": lambda x: x**0.5}
            f = sympify(func_text_sympy, locals=allowed_functions)

            xs = np.linspace(x_min, x_max, 500)
            ys = []
            for val in xs:
                try:
                    ys.append(float(f.subs(x, val)))
                except:
                    ys.append(np.nan)

            # نقاط التقاطع
            roots = solve(f, x)
            real_roots = [float(r.evalf()) for r in roots if r.is_real]

            # النقاط الحرجة
            df = diff(f, x)
            crit_points = solve(df, x)
            real_crit = [float(p.evalf()) for p in crit_points if p.is_real]
            crit_vals = [float(f.subs(x, p)) for p in real_crit]

            # المشتقة الثانية ونقاط الانعطاف
            d2f = diff(f, x, 2)
            inflect_points = solve(d2f, x)
            real_infl = [float(p.evalf()) for p in inflect_points if p.is_real]
            infl_vals = [float(f.subs(x, p)) for p in real_infl]

            # إعادة تشكيل النص العربي
            title_text = get_display(arabic_reshaper.reshape(f"رسم الدالة: {func_text}"))
            label_func = get_display(arabic_reshaper.reshape("الدالة"))
            label_roots = get_display(arabic_reshaper.reshape("نقاط التقاطع"))
            label_crit = get_display(arabic_reshaper.reshape("النقاط الحرجة"))
            label_infl = get_display(arabic_reshaper.reshape("نقاط الانعطاف"))

            # Plotly تفاعلي
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name=label_func, line=dict(color=color)))
            if real_roots:
                fig.add_trace(go.Scatter(x=real_roots, y=[0]*len(real_roots), mode='markers', name=label_roots, marker=dict(color='red', size=10)))
            if real_crit:
                fig.add_trace(go.Scatter(x=real_crit, y=crit_vals, mode='markers', name=label_crit, marker=dict(color='green', size=10)))
            if real_infl:
                fig.add_trace(go.Scatter(x=real_infl, y=infl_vals, mode='markers', name=label_infl, marker=dict(color='orange', size=10)))
            fig.update_layout(title=title_text, xaxis_title=get_display(arabic_reshaper.reshape('x')),
                              yaxis_title=get_display(arabic_reshaper.reshape('y')), width=800, height=500)
            st.plotly_chart(fig, use_container_width=True)

            # جدول قيم x و y
            table_x = np.linspace(x_min, x_max, 11)
            table_y = []
            for val in table_x:
                try:
                    table_y.append(float(f.subs(x, val)))
                except:
                    table_y.append(np.nan)
            st.subheader(get_display(arabic_reshaper.reshape("📋 جدول قيم x و y")))
            st.table({"x": table_x, "y": table_y})

            # عرض نقاط التقاطع والنقاط الحرجة والانفلاق
            st.subheader(label_roots)
            st.write(real_roots)
            st.subheader(label_crit)
            st.write(list(zip(real_crit, crit_vals)))
            st.subheader(label_infl)
            st.write(list(zip(real_infl, infl_vals)))

        except Exception as e:
            st.error(f"❌ خطأ في الدالة: {e}")
