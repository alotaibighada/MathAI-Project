# ---------------------
# Tab 3: رسم وتحليل الدوال – نسخة محسنة
# ---------------------
with tab3:
    st.header("📊 رسم وتحليل الدوال")
    func_text_input = st.text_input("أدخل الدالة (مثال: x^2 - 4x + 3)")
    x_min, x_max = st.slider("اختر نطاق x", -100, 100, (-10, 10))
    y_min, y_max = st.slider("اختر نطاق y", -100, 100, (-10, 10))
    color = st.color_picker("اختر لون المنحنى", "#1f77b4")
    example = st.button("✨ جرب مثال جاهز")
    draw_button = st.button("ارسم الدالة")

    func_text = "x^2 - 4x + 3" if example else func_text_input

    if draw_button:
        try:
            # تحويل الصياغة التقليدية إلى SymPy
            func_text_sympy = convert_math_to_python(func_text)
            allowed_functions = {"sin": sin, "cos": cos, "exp": exp, "log": log, "sqrt": lambda x: x**0.5}
            f = sympify(func_text_sympy, locals=allowed_functions)

            # قيم x و y
            xs = np.linspace(x_min, x_max, 500)
            ys = []
            for val in xs:
                try:
                    y_val = float(f.subs(x, val))
                    ys.append(y_val)
                except:
                    ys.append(np.nan)  # تجاهل القيم غير الممكنة
            ys = np.array(ys)

            # نقاط التقاطع (x-axis)
            roots = solve(f, x)
            real_roots = [float(r.evalf()) for r in roots if r.is_real]

            # النقاط الحرجة
            df = diff(f, x)
            crit_points = solve(df, x)
            real_crit = [float(p.evalf()) for p in crit_points if p.is_real]
            crit_vals = [float(f.subs(x, p)) for p in real_crit]

            # إعادة تشكيل النص العربي
            title_text = get_display(arabic_reshaper.reshape(f"رسم الدالة: {func_text}"))
            label_func = get_display(arabic_reshaper.reshape("الدالة"))
            label_roots = get_display(arabic_reshaper.reshape("نقاط التقاطع"))
            label_crit = get_display(arabic_reshaper.reshape("النقاط الحرجة"))

            # ضبط matplotlib لدعم العربية
            plt.rcParams['axes.unicode_minus'] = False

            # رسم التمثيل البياني
            fig, ax = plt.subplots(figsize=(8,5))
            ax.plot(xs, ys, label=label_func, color=color)
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(0, color='black', linewidth=1)
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_xlabel(get_display(arabic_reshaper.reshape('x')), fontsize=12)
            ax.set_ylabel(get_display(arabic_reshaper.reshape('y')), fontsize=12)
            ax.set_title(title_text, fontsize=14, fontweight='bold')

            # نقاط التقاطع والنقاط الحرجة
            if real_roots:
                ax.scatter(real_roots, [0]*len(real_roots), color='red', label=label_roots)
            if real_crit:
                ax.scatter(real_crit, crit_vals, color='green', label=label_crit)

            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)
            ax.legend(fontsize=10)
            st.pyplot(fig)

            # جدول قيم x و y (11 نقطة)
            table_x = np.linspace(x_min, x_max, 11)
            table_y = []
            for val in table_x:
                try:
                    table_y.append(float(f.subs(x, val)))
                except:
                    table_y.append(np.nan)
            st.subheader(get_display(arabic_reshaper.reshape("📋 جدول قيم x و y")))
            st.table({"x": table_x, "y": table_y})

            # عرض نقاط التقاطع والنقاط الحرجة
            st.subheader(label_roots)
            st.write(real_roots)
            st.subheader(label_crit)
            st.write(list(zip(real_crit, crit_vals)))

        except Exception as e:
            st.error(f"❌ خطأ في الدالة: {e}")
