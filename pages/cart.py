import streamlit as st

from utils.cart import (
    get_cart_items,
    update_quantity,
    remove_from_cart,
    cart_summary,
)

from utils.ui import (
    inject_css,
    money,
    page_title,
)

st.set_page_config(
    page_title="Cart | Change2.com",
    page_icon="🛒",
    layout="wide",
)

inject_css()

page_title(
    "Your Cart",
    "Review your products before checkout.",
)

summary = cart_summary()

items = summary["items"]

if not items:

    st.markdown(
        """
        <div class="empty-state">

            <div class="empty-icon">
                🛒
            </div>

            <h3>
                Your cart is empty
            </h3>

            <p>
                Add some products to your cart to get started.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "Start Shopping →",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/products.py")

    st.stop()


left, right = st.columns(
    [2.2, 1]
)

with left:

    st.subheader(
        f"Items ({summary['quantity']})"
    )

    for item in items:

        product_id = item["product_id"]

        st.markdown(
            f"""
            <div class="cart-item">

                <strong>
                    {item['name']}
                </strong>

                <br>

                <small>
                    {money(item['price'])} each
                </small>

            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(
            [1, 1, 1]
        )

        with c1:

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=max(
                    1,
                    int(item["stock"]),
                ),
                value=int(item["quantity"]),
                step=1,
                key=f"qty_{product_id}",
            )

        with c2:

            st.write("")
            st.write(
                f"Subtotal: **{money(item['subtotal'])}**"
            )

        with c3:

            st.write("")

            if st.button(
                "Remove",
                key=f"remove_{product_id}",
                use_container_width=True,
            ):

                remove_from_cart(
                    product_id
                )

                st.rerun()

        current_quantity = int(
            st.session_state.cart.get(
                str(product_id),
                0,
            )
        )

        if quantity != current_quantity:

            update_quantity(
                product_id,
                quantity,
            )

            st.rerun()


with right:

    summary = cart_summary()

    st.markdown(
        f"""
        <div class="cart-summary">

            <h3>
                Order Summary
            </h3>

            <div class="summary-row">
                <span>
                    Items
                </span>

                <span>
                    {summary['quantity']}
                </span>
            </div>

            <div class="summary-row">
                <span>
                    Subtotal
                </span>

                <span>
                    {money(summary['subtotal'])}
                </span>
            </div>

            <div class="summary-row">
                <span>
                    Delivery
                </span>

                <span>
                    {money(summary['delivery_fee'])}
                </span>
            </div>

            <div class="summary-total">
                <span>
                    Total
                </span>

                <span>
                    {money(summary['total'])}
                </span>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button(
        "Proceed to Checkout →",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page(
            "pages/checkout.py"
        )

    if st.button(
        "Continue Shopping",
        use_container_width=True,
    ):
        st.switch_page(
            "pages/products.py"
        )