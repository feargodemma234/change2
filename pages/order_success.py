import streamlit as st

from utils.auth import require_login
from utils.database import get_order
from utils.ui import (
    inject_css,
    money,
    page_title,
)

st.set_page_config(
    page_title="Order Confirmed | Change2.com",
    page_icon="✅",
    layout="wide",
)

inject_css()

user = require_login()

order_id = st.session_state.get(
    "last_order_id"
)

if not order_id:

    st.warning(
        "No recent order was found."
    )

    if st.button(
        "View My Orders",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page(
            "pages/orders.py"
        )

    st.stop()


order = get_order(
    order_id,
    str(user.id),
)


page_title(
    "Order Confirmed",
    "Thank you for shopping with Change2.com.",
)


st.markdown(
    """
    <div class="empty-state">

        <div class="empty-icon">
            ✅
        </div>

        <h2>
            Your order has been received!
        </h2>

        <p>
            We have received your order and payment information.
            Your payment will be reviewed before the order is processed.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


col1, col2 = st.columns(2)

with col1:

    st.markdown(
        f"""
        <div class="cart-summary">

            <h3>
                Order Details
            </h3>

            <div class="summary-row">
                <span>
                    Order ID
                </span>

                <strong>
                    {order_id}
                </strong>
            </div>

            <div class="summary-row">
                <span>
                    Payment
                </span>

                <strong>
                    {st.session_state.get(
                        "last_payment_method",
                        "Selected payment method"
                    )}
                </strong>
            </div>

            <div class="summary-total">
                <span>
                    Total
                </span>

                <span>
                    {money(
                        st.session_state.get(
                            "last_order_total",
                            0
                        )
                    )}
                </span>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:

    st.markdown(
        """
        <div class="cart-summary">

            <h3>
                What's next?
            </h3>

            <p>
                Your payment proof will be reviewed by the
                Change2.com store team.
            </p>

            <p>
                You can check your order status from your
                Orders page.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")

c1, c2, c3 = st.columns(3)

with c1:

    if st.button(
        "View My Orders",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page(
            "pages/orders.py"
        )

with c2:

    if st.button(
        "Continue Shopping",
        use_container_width=True,
    ):
        st.switch_page(
            "pages/products.py"
        )

with c3:

    if st.button(
        "My Account",
        use_container_width=True,
    ):
        st.switch_page(
            "pages/account.py"
        )