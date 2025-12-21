import streamlit as st
from sympy import symbols, Eq, solve, sympify, latex, lambdify
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import re
import arabic_reshaper
from bidi.algorithm import get_display

# =====================
# إعداد الخط العربي
# =====================
rcParams['font.family'] = 'DejaVu Sans'
rcParams['axes.unicode_minus'] = False

# =====================
# إعداد الصفحة
# =====================
st.set_page_config(page_title="Math AI Project", layout="wide")
st.title("🧮 مشروع Math AI – شرح تفصيلي لحل المعادلات")

x = symbols("x")
mode = st.radio("اختر وضع الاستخدام:", ["👩‍🎓 وضع تعليمي", "👩‍🔬 وضع متقدم"])

# =====================
# دوال مساعدة
# =====================
def convert_math_to_python(text):
    text = text.replace(" ", "")
    text = text.replace("^", "**")
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)
    text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', text)
    text = re.sub(r'([a-zA-Z])\(', r'\1*(', text)
    text = re.sub(r'\)\(', r')*(', text)
    return text

def arabic_text(text):
    return get_display(arabic_reshaper.reshape(text))

# =====================
# Tabs
# =====================
tab1, tab2, tab3 = st.tabs([
    "🔢 العمليات الحسابية",
    "📐 حل المعادلات (شرح تفصيلي)",
    "📊 رسم الدوال"
])

# ------------------------------------------------
# Tab 1: العمليات الحسابية
# ------------------------------------------------
with tab1:
    st.header("🔢 العمليات الحسابية")

    a = st.number_input("الرقم الأول", value=0.0)
    b = st.number_input("الرقم الثاني", value=0.0)
    op = st.selectbox("العملية", ["جمع", "طرح", "ضرب", "قسمة"])

    if st.button("احسب"):
        if op == "قسمة" and b == 0:
            st.error("❌ لا يمكن القسمة على صفر")
        else:
            result = {
                "جمع": a + b,
                "طرح": a - b,
                "ضرب": a * b,
                "قسمة": a / b
            }[op]
            st.success(f"✅ النتيجة = {result}")

# ------------------------------------------------
# Tab 2: حل المعادلات (شرح تفصيلي)
# ------------------------------------------------
with tab2:
    st.header("📐 حل المعادلات خطوة بخطوة (شرح تفصيلي)")

    eq_input = st.text_input("أدخل المعادلة (مثال: x^2-4x+3 = 0)")

    if st.button("حل المعادلة"):
        if "=" not in eq_input:
            st.error("❌ يجب أن تحتوي المعادلة على علامة =")
        else:
            try:
                # 1️⃣ تحويل الصيغة
                eq_text = convert_math_to_python(eq_input)
                left, right = eq_text.split("=")

                # 2️⃣ تكوين المعادلة
                equation = Eq(sympify(left), sympify(right))
                moved_eq = sympify(left) - sympify(right)

                # 3️⃣ تحديد نوع المعادلة
                degree = moved_eq.as_poly(x).degree()

                solutions = solve(equation, x)

                # =====================
                # الشرح التفصيلي
                # =====================
                st.subheader("🧠 شرح خطوات الحل")

                st.markdown("### ① كتابة المعادلة")
                st.write(f"المعادلة المدخلة هي:")
                st.latex(eq_input)

                st.markdown("### ② تحويل المعادلة إلى صيغة مناسبة")
                st.write("نحوّل المعادلة إلى صيغة يستطيع البرنامج التعامل معها:")
                st.code(eq_text)

                st.markdown("### ③ نقل جميع الحدود إلى طرف واحد")
                st.write("نطرح الطرف الأيمن من الطرف الأيسر للحصول على صفر:")
                st.latex(Eq(moved_eq, 0))

                st.markdown("### ④ تحديد نوع المعادلة")
                if degree == 1:
                    st.write("هذه **معادلة خطية من الدرجة الأولى**.")
                elif degree == 2:
                    st.write("هذه **معادلة تربيعية من الدرجة الثانية**.")
                else:
                    st.write("هذه معادلة من درجة أعلى.")

                st.markdown("### ⑤ حل المعادلة")
                st.write("نقوم بحل المعادلة لإيجاد قيمة المتغير x.")

                for s in solutions:
                    st.latex(f"x = {latex(s)}")

                st.markdown("### ✅ الحل النهائي")
                st.success(f"قيم x التي تحقق المعادلة هي: {solutions}")

            except Exception as e:
                st.error(f"❌ حدث خطأ أثناء الحل: {e}")

# ------------------------------------------------
# Tab 3: رسم الدوال
# ------------------------------------------------
with tab3:
    st.header("📊 رسم الدوال")

    func_text = st.text_input("أدخل الدالة (مثال: x^2-4x+3)")

    if st.button("ارسم الدالة"):
        try:
            f_sym = sympify(convert_math_to_python(func_text))
            f = lambdify(x, f_sym, "numpy")

            roots = solve(Eq(f_sym, 0), x)
            real_roots = [float(r) for r in roots if r.is_real]

            x_min = min(real_roots) - 5 if real_roots else -10
            x_max = max(real_roots) + 5 if real_roots else 10

            xs = np.linspace(x_min, x_max, 400)
            ys = f(xs)

            fig, ax = plt.subplots()
            ax.plot(xs, ys, linewidth=2, label=arabic_text("الدالة"))
            ax.axhline(0, color="black")
            ax.axvline(0, color="black")
            ax.grid(True, linestyle="--", alpha=0.7)

            for r in real_roots:
                ax.plot(r, 0, 'ro')
                ax.text(r, 0, f"{r}", fontsize=9)

            ax.set_title(arabic_text(f"رسم الدالة: {func_text}"))
            ax.set_xlabel(arabic_text("س"))
            ax.set_ylabel(arabic_text("ص"))
            ax.legend()
            st.pyplot(fig)

        except Exception as e:
            st.error(f"❌ خطأ في الرسم: {e}")
