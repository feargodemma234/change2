import streamlit as st

from utils.auth import require_login
from utils.database import (
    get_my_orders,
    get_order_items,
)
from utils.ui import (
    inject_css,
    money,
    page_title,
)

st.set_page_config(
    page_title="My Orders | Change2.com",
    page_icon="📦",
    layout="wide",
)

inject_css()

user = require_login()

user_id = str(user.id)

page_title(
    "My Orders",
    "Track your Change2.com purchases.",
)

orders = get_my_orders(user_id)

if not orders:

    st.markdown(
        """
        <div class="empty-state">

            <div class="empty-icon">
                📦
            </div>

            <h3>
                No orders yet
            </h3>

            <p>
                Your completed purchases will appear here.
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
        st.switch_page(
            "pages/products.py"
        )

    st.stop()


for order in orders:

    order_id = order.get("id")

    status = order.get(
        "status",
        "pending",
    )

    payment_status = order.get(
        "payment_status",
        "pending",
    )

    total = order.get(
        "total",
        0,
    )

    created_at = order.get(
        "created_at",
        "",
    )

    with st.expander(
        f"Order #{str(order_id)[:12]} — {money(total)}"
    ):

        c1, c2, c3 = st.columns(3)

        with c1:
            st.write("**Order status**")
            st.write(status)

        with c2:
            st.write("**Payment status**")
            st.write(payment_status)

        with c3:
            st.write("**Date**")
            st.write(str(created_at)[:10])

        st.divider()

        items = get_order_items(
            order_id
        )

        if items:

            st.write("**Products**")

            for item in items:

                name = item.get(
                    "product_name",
                    item.get(
                        "name",
                        "Product",
                    ),
                )

                quantity = item.get(
                    "quantity",
                    1,
                )

                price = item.get(
                    "unit_price",
                    0,
                )

                st.write(
                    f"• {name} × {quantity} — "
                    f"{money(price)}"
                )

        st.divider()

        st.write(
            f"**Delivery:** "
            f"{order.get('address', '')}, "
            f"{order.get('city', '')}, "
            f"{order.get('state', '')}"
        )


st.write("")

if st.button(
    "← Continue Shopping",
    use_container_width=True,
):
    st.switch_page(
        "pages/products.py"
    )