import streamlit as st
from sympy import symbols, Eq, solve, sympify, degree, diff
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import make_interp_spline

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
tab1, tab2, tab3, tab4 = st.tabs([
    "🔢 العمليات الحسابية",
    "📐 حل المعادلات",
    "📊 رسم وتحليل الدوال",
    "✍️ رسم الدالة عبر نقاط"
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
# Tab 3: رسم وتحليل الدوال
# ---------------------
with tab3:
    st.header("📊 رسم وتحليل الدوال")

    func_text_input = st.text_input("أدخل الدالة (مثال: x**2 - 4*x + 3)")
    color = st.color_picker("اختر لون المنحنى", "#1f77b4")
    x_min, x_max = st.slider("اختر نطاق x", -100, 100, (-10, 10))
    y_min, y_max = st.slider("اختر نطاق y", -100, 100, (-10, 10))
    example = st.button("✨ جرب مثال جاهز")
    draw_button = st.button("ارسم الدالة")

    func_text = "x**2 - 4*x + 3" if example else func_text_input

    if draw_button:
        try:
            f = sympify(func_text)
            xs = np.linspace(x_min, x_max, 1000)
            ys = np.array([float(f.subs(x, val)) for val in xs])

            deg = degree(f)
            dtype = "ثابتة" if deg==0 else "خطية" if deg==1 else "تربيعية" if deg==2 else "تكعيبية" if deg==3 else f"درجة {deg} أو أعلى"
            st.info(f"🔍 نوع الدالة: {dtype}")

            roots = solve(f, x)
            real_roots = [float(r.evalf()) for r in roots if r.is_real]

            df = diff(f, x)
            crit_points = solve(df, x)
            real_crit = [float(p.evalf()) for p in crit_points if p.is_real]
            crit_vals = [float(f.subs(x, p)) for p in real_crit]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='الدالة', line=dict(color=color)))
            if real_roots:
                fig.add_trace(go.Scatter(x=real_roots, y=[0]*len(real_roots), mode='markers', name='تقاطع x', marker=dict(color='red', size=10)))
            if real_crit:
                fig.add_trace(go.Scatter(x=real_crit, y=crit_vals, mode='markers', name='نقاط حرجة', marker=dict(color='green', size=10)))
            fig.update_layout(title=f"رسم الدالة: {func_text}", xaxis_title="x", yaxis_title="y",
                              xaxis=dict(range=[x_min, x_max]), yaxis=dict(range=[y_min, y_max]),
                              template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

            table_x = np.linspace(x_min, x_max, 11)
            table_y = [float(f.subs(x, val)) for val in table_x]
            st.subheader("📋 جدول قيم x و y")
            st.table({"x": table_x, "y": table_y})

        except Exception as e:
            st.error(f"❌ خطأ في الدالة: {e}")

# ---------------------
# Tab 4: رسم الدالة عبر نقاط (بديل الرسم اليدوي)
# ---------------------
with tab4:
    st.header("✍️ رسم الدالة عبر إدخال نقاط x و y")
    st.markdown("أدخل مجموعة من النقاط (x, y) بصيغة: x1,y1;x2,y2;...")

    points_text = st.text_area(
        "مثال: 0,0;1,1;2,4;3,9",
        "0,0;1,1;2,4;3,9"
    )

    draw_button_manual = st.button("ارسم الدالة")

    if draw_button_manual:
        try:
            points = points_text.split(";")
            xs, ys = [], []
            for p in points:
                x_val, y_val = p.split(",")
                xs.append(float(x_val.strip()))
                ys.append(float(y_val.strip()))

            # تقريب الدالة باستخدام Spline
            xs_sorted, ys_sorted = zip(*sorted(zip(xs, ys)))
            xs_new = np.linspace(min(xs_sorted), max(xs_sorted), 500)
            spline = make_interp_spline(xs_sorted, ys_sorted, k=3)
            ys_new = spline(xs_new)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=xs_new, y=ys_new, mode='lines+markers', name='الدالة المرسومة'))
            fig.update_layout(title="الدالة المرسومة من النقاط", xaxis_title="x", yaxis_title="y",
                              template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("📋 جدول قيم x و y")
            table_x = np.linspace(min(xs_sorted), max(xs_sorted), 11)
            table_y = spline(table_x)
            st.table({"x": table_x, "y": table_y})

            st.success("✅ تم رسم وتحليل الدالة بنجاح!")

        except Exception as e:
            st.error(f"❌ خطأ أثناء معالجة النقاط: {e}")
