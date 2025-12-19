import streamlit as st
from sympy import symbols, Eq, solve, sympify, degree, diff
import matplotlib.pyplot as plt
import numpy as np

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
tab1, tab2, tab3 = st.tabs(["🔢 العمليات الحسابية", "📐 حل المعادلات", "📊 رسم وتحليل الدوال"])

# ---------------------
# Tab 1: العمليات الحسابية
# ---------------------
with tab1:
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

# ---------------------
# Tab 2: حل المعادلات
# ---------------------
with tab2:
    st.header("📐 حل المعادلات خطوة بخطوة")
    eq_text = st.text_input("أدخل المعادلة (مثال: 2*x + 5 = 15)")

    if st.button("حل المعادلة"):
        try:
            left, right = eq_text.split("=")
            eq = Eq(sympify(left), sympify(right))
            sol = solve(eq, x)

            if mode == "👩‍🎓 وضع تعليمي":
                st.write("🔹 الخطوة 1: المعادلة الأصلية")
                st.write(eq_text)
                
                lhs_simplified = sympify(left) - sympify(right)
                st.write("🔹 الخطوة 2: نقل الحدود للحصول على 0 = ...")
                st.write(f"0 = {lhs_simplified}")
                
            st.success(f"✅ الحل النهائي: x = {sol}")
        except:
            st.error("❌ صيغة المعادلة غير صحيحة")

# ---------------------
# Tab 3: رسم وتحليل الدوال
# ---------------------
with tab3:
    st.header("📊 رسم وتحليل الدوال")

    func_text_input = st.text_input("أدخل الدالة (مثال: x**2 - 4*x + 3)")
    color = st.color_picker("اختر لون المنحنى", "#1f77b4")
    example = st.button("✨ جرب مثال جاهز")
    draw_button = st.button("ارسم الدالة")

    func_text = "x**2 - 4*x + 3" if example else func_text_input

    if draw_button:
        try:
            f = sympify(func_text)
            xs = np.linspace(-10, 10, 1000)
            ys = [float(f.subs(x, val)) for val in xs]

            deg = degree(f)
            if deg == 0:
                dtype = "ثابتة"
            elif deg == 1:
                dtype = "خطية"
            elif deg == 2:
                dtype = "تربيعية"
            elif deg == 3:
                dtype = "تكعيبية"
            else:
                dtype = f"درجة {deg} أو أعلى"

            st.info(f"🔍 نوع الدالة: {dtype}")

            # رسم المنحنى
            fig, ax = plt.subplots()
            ax.plot(xs, ys, label="الدالة", color=color)
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(0, color='black', linewidth=1)
            ax.grid(True)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_xlim(-10, 10)
            ax.set_ylim(min(ys)-1, max(ys)+1)
            ax.set_title(f"رسم الدالة: {func_text}")

            # نقاط التقاطع الحقيقية
            roots = solve(f, x)
            real_roots = [float(r) for r in roots if r.is_real]
            ax.scatter(real_roots, [0]*len(real_roots), color="red", label="نقاط التقاطع")

            # النقاط الحرجة
            df = diff(f, x)
            crit_points = solve(df, x)
            real_crit = [float(p) for p in crit_points if p.is_real]
            ax.scatter(real_crit, [float(f.subs(x, p)) for p in real_crit], color="green", label="نقاط حرجة")

            ax.legend()
            st.pyplot(fig)

            # جدول قيم x و y
            st.subheader("📋 جدول قيم x و y")
            table_x = np.linspace(-5, 5, 11)
            table_y = [float(f.subs(x, val)) for val in table_x]
            st.table({"x": table_x, "y": table_y})

            # شرح مبسط
            st.markdown("""
            <div style='text-align: right; direction: rtl; line-height: 1.6; font-size: 14px;'>
            🔍 <b>شرح مبسّط:</b><br>
            • المنحنى يوضّح كيف تتغير قيمة y عند تغيير x<br>
            • نقاط التقاطع تمثل حلول الدالة<br>
            • النقاط الحرجة تمثل أعلى وأدنى القيم للمنحنى<br>
            • جدول القيم يساعد على تصور العلاقة بين x و y
            </div>
            """, unsafe_allow_html=True)

            # سؤال الفهم
            understand = st.radio(
                "🤔 هل فهمت شكل الدالة؟",
                ["— اختر —", "👍 نعم، فهمت", "❓ لا، أحتاج شرح"]
            )
            if understand == "👍 نعم، فهمت":
                st.success("🎉 ممتاز! هذا يدل على فهمك لشكل الدالة والعلاقة بين x و y")
            elif understand == "❓ لا، أحتاج شرح":
                st.info("💡 حاول مراجعة المنحنى ونقاط التقاطع والنقاط الحرجة مرة أخرى")

        except Exception as e:
            st.error(f"❌ خطأ في الدالة: {e}")
