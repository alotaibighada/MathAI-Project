import streamlit as st
from sympy import symbols, Eq, solve, sympify, degree, diff
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Math AI Advanced", layout="wide")
st.title("🧮 Math AI – النسخة المتقدمة")

x = symbols("x")

# =====================
# وضع الاستخدام
# =====================
mode = st.radio("اختر وضع الاستخدام:", ["👩‍🎓 وضع تعليمي", "👩‍🔬 وضع متقدم"])

# =====================
# العمليات الحسابية
# =====================
st.header("🔢 العمليات الحسابية")
with st.form("calc_form"):
    a = st.number_input("الرقم الأول", value=0)
    b = st.number_input("الرقم الثاني", value=0)
    op = st.selectbox("العملية", ["جمع", "طرح", "ضرب", "قسمة"])
    submitted = st.form_submit_button("احسب")

    if submitted:
        try:
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
        except Exception as e:
            st.error(f"خطأ في العملية: {e}")

# =====================
# حل المعادلات خطوة بخطوة
# =====================
st.header("📐 حل المعادلات خطوة بخطوة")
with st.form("eq_form"):
    eq_text = st.text_input("أدخل المعادلة (مثال: 2*x + 5 = 15)")
    solve_button = st.form_submit_button("حل المعادلة")

    if solve_button:
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
# رسم وتحليل الدوال
# =====================
st.header("📊 رسم وتحليل الدوال")

# إدخال دوال متعددة
with st.form("func_form"):
    funcs_input = st.text_area(
        "أدخل الدوال مفصولة بفاصلة (مثال: x**2 -4*x +3, 2*x + 3, x**3 - 6*x**2 + 11*x -6)"
    )
    plot_button = st.form_submit_button("ارسم الدوال")

if plot_button:
    try:
        func_list = [sympify(f.strip()) for f in funcs_input.split(",") if f.strip()]
        xs = np.linspace(-10, 10, 500)
        fig, ax = plt.subplots()
        colors = ['blue', 'green', 'orange', 'purple', 'red']

        for i, f in enumerate(func_list):
            ys = [float(f.subs(x, val)) for val in xs]
            ax.plot(xs, ys, label=f"f{i+1}(x) = {f}", color=colors[i % len(colors)])

            # نقاط التقاطع
            roots = solve(f, x)
            real_roots = [float(r) for r in roots if r.is_real]
            ax.scatter(real_roots, [0]*len(real_roots), color=colors[i % len(colors)], marker='o', s=50, label=f"Roots f{i+1}")

            # النقاط المهمة للدوال التربيعية
            if degree(f) == 2:
                f_prime = diff(f, x)
                vertex_x = solve(f_prime, x)[0]
                vertex_y = float(f.subs(x, vertex_x))
                ax.scatter(vertex_x, vertex_y, color=colors[i % len(colors)], marker='x', s=100, label=f"Vertex f{i+1}")
                if mode == "👩‍🎓 وضع تعليمي":
                    st.write(f"🔹 الدالة f{i+1}: Vertex عند ({vertex_x}, {vertex_y})")

            # نوع الدالة
            deg = degree(f)
            if deg == 1:
                dtype = "خطية"
            elif deg == 2:
                dtype = "تربيعية"
            elif deg == 3:
                dtype = "تكعيبية"
            else:
                dtype = "غير محددة"
            if mode == "👩‍🎓 وضع تعليمي":
                st.write(f"🔹 الدالة f{i+1}: نوع الدالة = {dtype}")

        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("رسم وتحليل الدوال")
        ax.legend()
        st.pyplot(fig)

        understand = st.radio(
            "🤔 هل فهمت شكل الدوال؟",
            ["— اختر —", "👍 نعم، فهمت", "❓ لا، أحتاج شرح"]
        )
        if understand == "👍 نعم، فهمت":
            st.success("🎉 ممتاز! هذا يدل على فهمك لشكل الدوال والعلاقة بين x و y")
        elif understand == "❓ لا، أحتاج شرح":
            st.info("""
            🔍 شرح مبسّط:
            • المنحنى يوضّح كيف تتغير قيمة y عند تغيير x  
            • نقاط التقاطع تمثل حلول الدوال  
            • الدالة التربيعية تظهر قمة/قاع المنحنى  
            • شكل المنحنى يساعد على التنبؤ بالسلوك
            """)

    except Exception as e:
        st.error(f"خطأ في الدوال: {e}")
