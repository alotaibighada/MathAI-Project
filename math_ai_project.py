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
# رسم وتحليل الدوال
# =====================
st.header("📊 رسم وتحليل الدوال")

# إنشاء فورم لتجميع إدخال الدوال وزر الرسم
with st.form("func_form"):
    funcs_input = st.text_area(
        "أدخل الدوال مفصولة بفاصلة (مثال: x**2 -4*x +3, 2*x + 3, x**3 - 6*x**2 + 11*x -6)"
    )
    plot_button = st.form_submit_button("ارسم الدوال")

if plot_button:
    try:
        # تحويل النص إلى دوال sympy
        func_list = [sympify(f.strip()) for f in funcs_input.split(",") if f.strip()]
        xs = np.linspace(-10, 10, 500)
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['blue', 'green', 'orange', 'purple', 'red']

        for i, f in enumerate(func_list):
            # حساب قيم y
            ys = [float(f.subs(x, val)) for val in xs]
            ax.plot(xs, ys, label=f"f{i+1}(x) = {f}", color=colors[i % len(colors)])

            # حساب نقاط التقاطع مع محور x
            roots = solve(f, x)
            real_roots = [float(r) for r in roots if r.is_real]
            ax.scatter(real_roots, [0]*len(real_roots), color=colors[i % len(colors)], marker='o', s=50, label=f"Roots f{i+1}")

            # النقاط المهمة للدوال التربيعية (Vertex)
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

        # تنسيق الرسم
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("رسم وتحليل الدوال")
        ax.legend()
        st.pyplot(fig)

        # سؤال التعليم والفهم
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
