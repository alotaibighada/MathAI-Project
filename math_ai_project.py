import streamlit as st
from sympy import symbols, sympify, lambdify
import numpy as np
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display
from matplotlib import font_manager

# =====================
# إعداد الصفحة
# =====================
st.set_page_config(page_title="Math AI", layout="wide")
st.title("🧮 Math AI – رسم الدوال")
st.markdown("أدخل الدالة على شكل x^2-4*x+3 ثم اضغط ارسم")

# =====================
# المتغيرات
# =====================
x = symbols("x")

# =====================
# دعم النص العربي
# =====================
arabic_font_path = "./Amiri-Regular.ttf"  # تأكد أن الخط موجود في نفس المجلد
font_prop = font_manager.FontProperties(fname=arabic_font_path)

def arabic_text(text):
    if not text:
        return ""
    reshaped_text = arabic_reshaper.reshape(str(text))
    bidi_text = get_display(reshaped_text)
    return bidi_text

# =====================
# تبسيط كتابة المعادلة
# =====================
def convert_math_to_python(text):
    text = text.replace(" ", "")
    text = text.replace("^", "**")
    return text

# =====================
# إدخال الدالة
# =====================
func_text = st.text_input("أدخل الدالة", "x^2-4*x+3")

if st.button("ارسم"):
    try:
        if not func_text:
            st.warning("⚠ أدخل دالة أولاً")
        else:
            # تحويل النص البرمجي
            func_python = convert_math_to_python(func_text)
            f_sym = sympify(func_python)
            f = lambdify(x, f_sym, "numpy")

            # إعداد النقاط
            xs = np.linspace(-10, 10, 400)
            ys = f(xs)

            # إعداد الرسم
            fig, ax = plt.subplots(figsize=(8,5))
            ax.plot(xs, ys, color="#FF6347", linewidth=2, label=arabic_text("الدالة"))
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(0, color='black', linewidth=1)
            ax.set_facecolor("#F5F5F5")
            ax.grid(True, linestyle='--', alpha=0.7)

            # استخدام الخط العربي
            plt.rcParams['font.family'] = font_prop.get_name()

            ax.set_title(arabic_text(f"رسم الدالة: {func_text}"), fontsize=14, color="#4B0082")
            ax.set_xlabel(arabic_text("س"), fontsize=12)
            ax.set_ylabel(arabic_text("ص"), fontsize=12)
            ax.legend()
            fig.tight_layout()

            # عرض الرسم
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ خطأ في الرسم: {e}")
