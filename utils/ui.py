import html
import streamlit as st


def inject_css():

    st.markdown(
        """
        <style>

        /* =========================
           GLOBAL
        ========================= */

        .stApp {
            background: #f7f8fa;
        }

        .main .block-container {
            max-width: 1400px;
            padding-top: 1.5rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3, h4 {
            letter-spacing: -0.03em;
        }

        /* =========================
           HEADER
        ========================= */

        .change2-header {
            width: 100%;
            padding: 10px 0 18px 0;
        }

        .change2-logo {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 25px;
            font-weight: 800;
            color: #171717;
        }

        .logo-mark {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #111111;
            color: white;
            font-size: 15px;
            font-weight: 800;
        }

        .nav-brand {
            font-size: 18px;
            font-weight: 800;
            padding-top: 7px;
        }

        /* =========================
           BUTTONS
        ========================= */

        .stButton > button {
            border-radius: 10px;
            min-height: 42px;
            font-weight: 650;
            transition: 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
        }

        /* =========================
           HERO
        ========================= */

        .hero {
            margin-top: 20px;
            min-height: 390px;
            border-radius: 28px;
            padding: 70px;
            display: flex;
            align-items: center;

            background:
                radial-gradient(
                    circle at 80% 20%,
                    rgba(255,255,255,0.20),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    #171717,
                    #303030
                );

            color: white;
            overflow: hidden;
            position: relative;
        }

        .hero:after {
            content: "";
            position: absolute;
            width: 300px;
            height: 300px;
            right: -100px;
            bottom: -130px;
            border-radius: 50%;
            border: 60px solid rgba(255,255,255,0.05);
        }

        .hero-content {
            max-width: 720px;
            position: relative;
            z-index: 2;
        }

        .hero-badge {
            display: inline-block;
            padding: 7px 13px;
            border-radius: 999px;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.15);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.12em;
            margin-bottom: 18px;
        }

        .hero h1 {
            font-size: clamp(42px, 6vw, 72px);
            line-height: 0.98;
            margin: 0;
            font-weight: 850;
        }

        .hero h1 span {
            color: #cfcfcf;
        }

        .hero p {
            max-width: 600px;
            margin-top: 22px;
            color: #d5d5d5;
            font-size: 17px;
            line-height: 1.7;
        }

        /* =========================
           SECTIONS
        ========================= */

        .section-heading {
            margin: 20px 0 20px 0;
        }

        .section-label {
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.14em;
            color: #777777;
        }

        .section-heading h2 {
            margin: 3px 0 0 0;
            font-size: 30px;
        }

        /* =========================
           FEATURES
        ========================= */

        .feature-card {
            background: white;
            border: 1px solid #e7e7e7;
            border-radius: 18px;
            padding: 25px;
            min-height: 190px;
            box-shadow: 0 6px 24px rgba(0,0,0,0.04);
        }

        .feature-icon {
            font-size: 30px;
            margin-bottom: 12px;
        }

        .feature-card h3 {
            margin: 0 0 8px 0;
            font-size: 20px;
        }

        .feature-card p {
            color: #777777;
            line-height: 1.6;
            margin: 0;
        }

        /* =========================
           PRODUCT CARD
        ========================= */

        .product-card {
            background: white;
            border: 1px solid #e8e8e8;
            border-radius: 18px;
            overflow: hidden;
            margin-bottom: 8px;
            box-shadow: 0 6px 22px rgba(0,0,0,0.04);
            transition: 0.2s ease;
        }

        .product-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 32px rgba(0,0,0,0.08);
        }

        .product-image {
            width: 100%;
            height: 210px;
            object-fit: cover;
            display: block;
            background: #eeeeee;
        }

        .product-image-placeholder {
            width: 100%;
            height: 210px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #eeeeee;
            font-size: 50px;
        }

        .product-info {
            padding: 17px;
        }

        .product-category {
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-weight: 800;
            color: #888888;
        }

        .product-name {
            font-size: 18px;
            font-weight: 750;
            margin-top: 5px;
            color: #161616;
        }

        .product-description {
            color: #777777;
            font-size: 13px;
            line-height: 1.5;
            margin-top: 7px;
            min-height: 39px;
        }

        .product-price {
            font-size: 21px;
            font-weight: 850;
            margin-top: 13px;
            color: #111111;
        }

        .product-stock {
            font-size: 12px;
            color: #777777;
            margin-top: 5px;
        }

        /* =========================
           EMPTY STATE
        ========================= */

        .empty-state {
            text-align: center;
            background: white;
            border: 1px dashed #d6d6d6;
            border-radius: 20px;
            padding: 55px 20px;
            margin: 20px 0;
        }

        .empty-icon {
            font-size: 45px;
            margin-bottom: 10px;
        }

        .empty-state h3 {
            margin-bottom: 5px;
        }

        .empty-state p {
            color: #777777;
        }

        /* =========================
           CTA
        ========================= */

        .cta-section {
            border-radius: 24px;
            background: #eeeeee;
            padding: 45px;
            margin-top: 20px;
        }

        .cta-section h2 {
            font-size: 35px;
            margin: 5px 0;
        }

        .cta-section p {
            color: #666666;
        }

        /* =========================
           FORMS
        ========================= */

        .form-card {
            background: white;
            border: 1px solid #e6e6e6;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 6px 25px rgba(0,0,0,0.04);
        }

        .form-title {
            font-size: 30px;
            font-weight: 800;
            margin-bottom: 5px;
        }

        .form-subtitle {
            color: #777777;
            margin-bottom: 25px;
        }

        /* =========================
           CART
        ========================= */

        .cart-item {
            background: white;
            border: 1px solid #e8e8e8;
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 12px;
        }

        .cart-summary {
            background: white;
            border: 1px solid #e5e5e5;
            border-radius: 18px;
            padding: 25px;
            box-shadow: 0 6px 24px rgba(0,0,0,0.04);
        }

        .summary-row {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            color: #666666;
        }

        .summary-total {
            display: flex;
            justify-content: space-between;
            border-top: 1px solid #eeeeee;
            padding-top: 15px;
            margin-top: 15px;
            font-size: 22px;
            font-weight: 800;
            color: #111111;
        }

        /* =========================
           STATUS
        ========================= */

        .status-badge {
            display: inline-block;
            border-radius: 999px;
            padding: 6px 12px;
            font-size: 11px;
            font-weight: 750;
            background: #eeeeee;
        }

        /* =========================
           FOOTER
        ========================= */

        .footer {
            margin-top: 50px;
            padding: 35px 0 15px 0;
            border-top: 1px solid #dddddd;
            color: #777777;
        }

        .footer-logo {
            font-size: 20px;
            font-weight: 800;
            color: #222222;
            margin-bottom: 15px;
        }

        .footer-links {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            font-size: 13px;
            margin-bottom: 20px;
        }

        .footer-copy {
            font-size: 12px;
        }

        /* =========================
           MOBILE
        ========================= */

        @media (max-width: 768px) {

            .main .block-container {
                padding-left: 12px;
                padding-right: 12px;
            }

            .hero {
                min-height: 330px;
                padding: 35px 25px;
                border-radius: 22px;
            }

            .hero h1 {
                font-size: 43px;
            }

            .hero p {
                font-size: 15px;
            }

            .feature-card {
                margin-bottom: 12px;
            }

            .cta-section {
                padding: 30px 22px;
            }

            .cta-section h2 {
                font-size: 28px;
            }

            .product-image,
            .product-image-placeholder {
                height: 180px;
            }

            .form-card {
                padding: 20px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def product_card(product):

    name = html.escape(str(product.get("name", "Unnamed product")))
    description = html.escape(
        str(product.get("description", ""))
    )

    category = html.escape(
        str(product.get("category", "General"))
    )

    image_url = str(product.get("image_url", "") or "").strip()

    try:
        price = float(product.get("price", 0))
    except Exception:
        price = 0.0

    try:
        stock = int(product.get("stock", 0))
    except Exception:
        stock = 0

    if image_url:
        safe_image_url = html.escape(image_url, quote=True)

        image_html = f"""
            <img
                class="product-image"
                src="{safe_image_url}"
                alt="{name}"
            >
        """
    else:
        image_html = """
            <div class="product-image-placeholder">
                📦
            </div>
        """

    if stock > 0:
        stock_text = f"{stock} available"
    else:
        stock_text = "Out of stock"

    st.markdown(
        f"""
        <div class="product-card">

            {image_html}

            <div class="product-info">

                <div class="product-category">
                    {category}
                </div>

                <div class="product-name">
                    {name}
                </div>

                <div class="product-description">
                    {description}
                </div>

                <div class="product-price">
                    ₦{price:,.2f}
                </div>

                <div class="product-stock">
                    {stock_text}
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


def page_title(title, subtitle=None):

    safe_title = html.escape(str(title))

    st.markdown(
        f"""
        <div class="section-heading">

            <span class="section-label">
                CHANGE2.COM
            </span>

            <h1>
                {safe_title}
            </h1>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if subtitle:
        st.caption(str(subtitle))


def money(value):

    try:
        value = float(value)
    except Exception:
        value = 0.0

    return f"₦{value:,.2f}"


def status_badge(status):

    safe_status = html.escape(str(status))

    st.markdown(
        f"""
        <span class="status-badge">
            {safe_status}
        </span>
        """,
        unsafe_allow_html=True,
    )