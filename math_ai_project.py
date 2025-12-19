# =====================
# رسم وتحليل الدوال مع شرح عربي مرتب
# =====================
st.header("📊 رسم وتحليل الدوال")

col1, col2 = st.columns(2)

with col1:
    example = st.button("✨ جرب مثال جاهز")
    func_text_input = st.text_input("أدخل الدالة (مثال: x**2 - 4*x + 3)")
    func_text = "x**2 - 4*x + 3" if example else func_text_input

with col2:
    color = st.color_picker("اختر لون المنحنى", "#1f77b4")

draw_button = st.button("ارسم الدالة")

if draw_button:
    try:
        f = sympify(func_text)
        xs = np.linspace(-10, 10, 400)
        ys = [float(f.subs(x, val)) for val in xs]

        # تحديد نوع الدالة
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
        ax.set_title(f"رسم الدالة: {func_text}")

        # نقاط التقاطع الحقيقية
        roots = solve(f, x)
        real_roots = [float(r) for r in roots if r.is_real]
        ax.scatter(real_roots, [0]*len(real_roots), color="red", label="نقاط التقاطع")

        # النقاط الحرجة (المشتقة = 0)
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

        # شرح عربي مرتب
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
