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
mode = st.radio("اختر وضع الاستخدام:", ["👩‍🎓 وضع تعليمي", "👩‍🔬 وضع متقدم"], key="usage_mode")

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
# دالة لإعادة تشكيل النصوص العربية
# =====================
def arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

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
    st.header(arabic_text("🔢 العمليات الحسابية"))
    a = st.number_input(arabic_text("الرقم الأول"), value=0, key="calc_a")
    b = st.number_input(arabic_text("الرقم الثاني"), value=0, key="calc_b")
    op = st.selectbox(arabic_text("العملية"), ["جمع", "طرح", "ضرب", "قسمة"], key="calc_op")

    if st.button(arabic_text("احسب"), key="calc_button"):
        try:
            if op == "جمع":
                r = a + b
            elif op == "طرح":
                r = a - b
            elif op == "ضرب":
                r = a * b
            elif op == "قسمة":
                if b == 0:
                    st.error(arabic_text("❌ لا يمكن القسمة على صفر"))
                    r = None
                else:
                    r = a / b
            if r is not None:
                st.success(arabic_text(f"✅ النتيجة = {r}"))
                if mode == "👩‍🎓 وضع تعليمي":
                    st.info(arabic_text("💡 تم تطبيق العملية الحسابية على الرقمين مباشرة"))
        except Exception as e:
            st.error(arabic_text(f"❌ خطأ أثناء الحساب: {e}"))

# ---------------------
# Tab 2: حل المعادلات مع شرح AI
# ---------------------
with tab2:
    st.header(arabic_text("📐 حل المعادلات خطوة بخطوة"))
    eq_text_input = st.text_input(arabic_text("أدخل المعادلة (مثال: x^2 - 4x + 3 = 0)"), key="eq_input")
    example_eq = st.button(arabic_text("✨ جرب مثال جاهز"), key="example_eq")

    if example_eq:
        eq_text_input = "x^2 - 4*x + 3 = 0"

    if st.button(arabic_text("حل المعادلة"), key="solve_eq"):
        try:
            eq_text = convert_math_to_python(eq_text_input)
            if "=" not in eq_text:
                st.error(arabic_text("❌ يجب أن تحتوي المعادلة على '='"))
                st.stop()
            left, _, right = eq_text.partition("=")
            eq = Eq(sympify(left), sympify(right))
            sol = solve(eq, x)

            if mode == "👩‍🎓 وضع تعليمي":
                st.write(arabic_text("🔹 المعادلة الأصلية:"), eq_text_input)
                lhs_simplified = sympify(left) - sympify(right)
                st.write(arabic_text("🔹 بعد النقل للحصول على 0:"))
                st.latex(Eq(lhs_simplified, 0))
                st.write(arabic_text("🔹 شرح AI خطوة بخطوة:"))
                for line in generate_explanation(eq, sol):
                    st.markdown(arabic_text(f"- {line}"))

            st.success(arabic_text(f"✅ الحل النهائي: x = {[latex(s) for s in sol]}"))

        except Exception as e:
            st.error(arabic_text(f"❌ صيغة المعادلة غير صحيحة: {e}"))

# ---------------------
# Tab 3: رسم وتحليل الدوال مع AI
# ---------------------
with tab3:
    st.header(arabic_text("📊 رسم وتحليل الدوال تفاعلي"))
    func_text_input = st.text_input(arabic_text("أدخل الدالة (مثال: x^2 - 4x + 3)"), key="func_input")
    x_min, x_max = st.slider(arabic_text("اختر نطاق x"), -100, 100, (-10, 10), key="slider_x")
    y_min, y_max = st.slider(arabic_text("اختر نطاق y"), -100, 100, (-10, 10), key="slider_y")
    color = st.color_picker(arabic_text("اختر لون المنحنى"), "#1f77b4", key="color_picker")

    example_func = st.button(arabic_text("✨ جرب مثال جاهز"), key="example_func")
    draw_button = st.button(arabic_text("ارسم الدالة"), key="draw_button")

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

            # Plotly تفاعلي مع النصوص العربية صحيحة
            title_text = arabic_text(f"رسم الدالة: {func_text}")
            label_func = arabic_text("الدالة")
            label_roots = arabic_text("نقاط التقاطع")
            label_crit = arabic_text("النقاط الحرجة")
            label_infl = arabic_text("نقاط الانعطاف")

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name=label_func, line=dict(color=color)))
            if real_roots:
                fig.add_trace(go.Scatter(x=real_roots, y=[0]*len(real_roots), mode='markers', name=label_roots, marker=dict(color='red', size=10)))
            if real_crit:
                fig.add_trace(go.Scatter(x=real_crit, y=crit_vals, mode='markers', name=label_crit, marker=dict(color='green', size=10)))
            if real_infl:
                fig.add_trace(go.Scatter(x=real_infl, y=infl_vals, mode='markers', name=label_infl, marker=dict(color='orange', size=10)))

            fig.update_layout(
                title=title_text,
                xaxis_title=arabic_text('x'),
                yaxis_title=arabic_text('y'),
                font=dict(family="Arial", size=12),
                width=800,
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

            # جدول قيم x و y
            table_x = np.linspace(x_min, x_max, 11)
            table_y = []
            for val in table_x:
                try:
                    table_y.append(float(f.subs(x, val)))
                except:
                    table_y.append(np.nan)
            st.subheader(arabic_text("📋 جدول قيم x و y"))
            st.table({"x": table_x, "y": table_y})

            # عرض نقاط التقاطع والنقاط الحرجة والانعطاف
            st.subheader(label_roots)
            st.write(real_roots)
            st.subheader(label_crit)
            st.write(list(zip(real_crit, crit_vals)))
            st.subheader(label_infl)
            st.write(list(zip(real_infl, infl_vals)))

        except Exception as e:
            st.error(arabic_text(f"❌ خطأ في الدالة: {e}"))
