if st.button("ارسم", key="plot_btn"):
    try:
        if not func_text:
            st.warning("⚠ أدخل دالة أولاً")
        else:
            func_python = convert_math_to_python(func_text)
            f_sym = sympify(func_python)

            f = lambdify(x, f_sym, "numpy")
            xs = np.linspace(-10, 10, 400)
            ys = np.array([f(val) for val in xs])

            fig, ax = plt.subplots(figsize=(7,5))
            ax.plot(xs, ys, color="#FF6347", linewidth=2, label="function")
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(0, color='black', linewidth=1)
            ax.set_facecolor("#F5F5F5")
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_title(f" {func_text}", fontsize=14, color="#4B0082")
            ax.set_xlabel("x", fontsize=12)
            ax.set_ylabel("y", fontsize=12)
            
            # =====================
            # تحديد نقاط على المنحنى
            # =====================
            num_points = 10  # عدد النقاط المراد تحديدها
            xs_points = np.linspace(-10, 10, num_points)
            ys_points = np.array([f(val) for val in xs_points])
            ax.scatter(xs_points, ys_points, color="blue", s=50, zorder=5)  # رسم النقاط
            for xp, yp in zip(xs_points, ys_points):
                ax.text(xp, yp, f"({xp:.2f},{yp:.2f})", fontsize=9, color="darkblue", ha='right', va='bottom')

            ax.legend()
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ خطأ في الرسم: {e}")
