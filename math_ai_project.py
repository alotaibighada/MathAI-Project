import streamlit as st
from sympy import symbols, Eq, solve, sympify, degree, diff
import numpy as np
import matplotlib.pyplot as plt
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
# Tabs للفصل بين الوظائف
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
# Tab 2: حل المعادلات
# ---------------------
with tab2:
    st.header("📐 حل المعادلات خطوة بخطوة")
    eq_text = st.text_input("أدخل المعادلة (مثال: 2*x + 5 = 15)")

    if st.button("حل المعادلة"):
        try:
            if "=" in eq_text:
                left, _, right = eq_text.partition("=")
                eq = Eq(sympify(left), sympify(right))
            else:
                st.error("❌ يجب أن تحتوي المعادلة على '='")
                st.stop()
            
            sol = solve(eq, x)

            if mode == "👩‍🎓 وضع تعليمي":
                st.write("🔹 المعادلة الأصلية:", eq_text)
                lhs_simplified = sympify(left) - sympify(right)
                st.write("🔹 بعد النقل للحصول على 0 =", lhs_simplified)

            st.success(f"✅ الحل النهائي: x = {sol}")

        except Exception as e:
            st.error(f"❌ صيغة المعادلة غير صحيحة: {e}")

# ---------------------
# Tab 3: رسم وتحليل الدوال (بالتمثيل البياني التقليدي ودعم العربية)
# ---------------------
with tab3:
    st.header("📊 رسم وتحليل الدوال")
    func_text_input = st.text_input("أدخل الدالة (مثال: x**2 - 4*x + 3)")
    x_min, x_max = st.slider("اختر نطاق x", -100, 100, (-10, 10))
    y_min, y_max = st.slider("اختر نطاق y", -100, 100, (-10, 10))
    color = st.color_picker("اختر لون المنحنى", "#1f77b4")
    example = st.button("✨ جرب مثال جاهز")
    draw_button = st.button("ارسم الدالة")

    func_text = "x**2 - 4*x + 3" if example else func_text_input

    if draw_button:
        try:
            f = sympify(func_text)
            xs = np.linspace(x_min, x_max, 500)
            ys = np.array([float(f.subs(x, val)) for val in xs])

            # نقاط التقاطع الحقيقية
            roots = solve(f, x)
            real_roots = [float(r.evalf()) for r in roots if r.is_real]

            # النقاط الحرجة
            df = diff(f, x)
            crit_points = solve(df, x)
            real_crit = [float(p.evalf()) for p in crit_points if p.is_real]
            crit_vals = [float(f.subs(x, p)) for p in real_crit]

            # إعادة تشكيل النص العربي
            title_text = get_display(arabic_reshaper.reshape(f"رسم الدالة: {func_text}"))
            label_roots = get_display(arabic_reshaper.reshape("نقاط التقاطع"))
            label_crit = get_display(arabic_reshaper.reshape("النقاط الحرجة"))

            # رسم التمثيل البياني التقليدي
            fig, ax = plt.subplots(figsize=(8,5))
            ax.plot(xs, ys, label=get_display(arabic_reshaper.reshape("الدالة")), color=color)
            ax.axhline(0, color='black', linewidth=1)  # محور x
            ax.axvline(0, color='black', linewidth=1)  # محور y
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_xlabel(get_display(arabic_reshaper.reshape('x')))
            ax.set_ylabel(get_display(arabic_reshaper.reshape('y')))
            ax.set_title(title_text)

            # نقاط التقاطع الحمراء
            ax.scatter(real_roots, [0]*len(real_roots), color='red', label=label_roots)
            # النقاط الحرجة الخضراء
            ax.scatter(real_crit, crit_vals, color='green', label=label_crit)

            ax.legend()
            st.pyplot(fig)

            # جدول قيم x و y
            table_x = np.linspace(-5, 5, 11)
            table_y = [float(f.subs(x, val)) for val in table_x]
            st.subheader(get_display(arabic_reshaper.reshape("📋 جدول قيم x و y")))
            st.table({"x": table_x, "y": table_y})

        except Exception as e:
            st.error(f"❌ خطأ في الدالة: {e}")
