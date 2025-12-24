import streamlit as st

def add_footer():
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            color: #888888;
            background-color: #f0f2f6;
            padding: 10px 0;
            box-shadow: 0 -1px 5px rgba(0,0,0,0.1);
        }
        </style>
        <div class="footer">
            © 2025 Ghada Inc. | جميع الحقوق محفوظة
        </div>
        """,
        unsafe_allow_html=True
    )

