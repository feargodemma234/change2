import streamlit as st

from utils.auth import require_login, get_user_email
from utils.cart import cart_summary, validate_cart, clear_cart
from utils.database import (
    get_profile,
    update_profile,
    get_payment_methods,
    create_order,
    submit_payment_proof,
)
from utils.security import (
    clean_text,
    validate_phone,
    validate_proof,
)
from utils.ui import (
    inject_css,
    money,
    page_title,
)

st.set_page_config(
    page_title="Checkout | Change2.com",
    page_icon="💳",
    layout="wide",
)

inject_css()

user = require_login()
user_id = str(user.id)

summary = cart_summary()

if not summary["items"]:
    st.warning("Your cart is empty.")

    if st.button(
        "← Continue Shopping",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/products.py")

    st.stop()


page_title(
    "Checkout",
    "Enter your delivery information and choose a payment method.",
)


# -------------------------------------------------
# VERIFY CART
# -------------------------------------------------

valid, errors = validate_cart()

if not valid:

    for error in errors:
        st.error(error)

    if st.button(
        "Return to Cart",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/cart.py")

    st.stop()


# -------------------------------------------------
# LOAD PROFILE
# -------------------------------------------------

profile = get_profile(user_id) or {}

saved_name = profile.get("full_name", "")
saved_phone = profile.get("phone", "")

email = get_user_email() or ""


# -------------------------------------------------
# LAYOUT
# -------------------------------------------------

left, right = st.columns(
    [1.7, 1]
)


# =================================================
# CUSTOMER INFORMATION
# =================================================

with left:

    st.subheader("Delivery Information")

    full_name = st.text_input(
        "Full name",
        value=saved_name,
        placeholder="Your full name",
    )

    phone = st.text_input(
        "Phone number",
        value=saved_phone,
        placeholder="+234...",
    )

    customer_email = st.text_input(
        "Email address",
        value=email,
        disabled=True,
    )

    st.write("")

    address = st.text_area(
        "Delivery address",
        placeholder="House number, street, area...",
        height=100,
    )

    state = st.text_input(
        "State",
        placeholder="e.g. FCT",
    )

    city = st.text_input(
        "City",
        placeholder="e.g. Abuja",
    )

    additional_info = st.text_area(
        "Additional delivery information",
        placeholder="Optional instructions for delivery...",
        height=80,
    )


# =================================================
# PAYMENT METHODS
# =================================================

payment_methods = get_payment_methods(
    enabled_only=True
)

with left:

    st.write("")

    st.subheader("Payment Method")

    if not payment_methods:

        st.error(
            "No payment methods are currently available."
        )

        st.stop()

    payment_names = [
        method["name"]
        for method in payment_methods
    ]

    selected_payment = st.radio(
        "Choose how you want to pay",
        payment_names,
    )

    selected_method = next(
        (
            method
            for method in payment_methods
            if method["name"] == selected_payment
        ),
        None,
    )

    if selected_method:

        instructions = selected_method.get(
            "instructions",
            "",
        )

        if instructions:

            st.info(
                instructions
            )


# =================================================
# PAYMENT PROOF
# =================================================

with left:

    st.write("")

    st.subheader(
        "Payment Proof"
    )

    st.caption(
        "After making your payment, upload the receipt, "
        "screenshot or other accepted proof."
    )

    uploaded_file = st.file_uploader(
        "Upload payment proof",
        type=[
            "jpg",
            "jpeg",
            "png",
            "pdf",
        ],
    )


# =================================================
# ORDER SUMMARY
# =================================================

with right:

    st.markdown(
        f"""
        <div class="cart-summary">

            <h3>
                Order Summary
            </h3>

            <div class="summary-row">
                <span>
                    Products
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

    st.warning(
        "Please make sure your delivery information "
        "is correct before placing the order."
    )


# =================================================
# PLACE ORDER
# =================================================

st.write("")
st.divider()

place_order = st.button(
    "Place Order & Submit Payment →",
    type="primary",
    use_container_width=True,
)


if place_order:

    # -----------------------------
    # VALIDATE CUSTOMER
    # -----------------------------

    full_name = clean_text(
        full_name,
        150,
    )

    phone = clean_text(
        phone,
        30,
    )

    address = clean_text(
        address,
        500,
    )

    state = clean_text(
        state,
        100,
    )

    city = clean_text(
        city,
        100,
    )

    additional_info = clean_text(
        additional_info,
        500,
    )

    if not full_name:

        st.error(
            "Please enter your full name."
        )
        st.stop()

    if not validate_phone(phone):

        st.error(
            "Please enter a valid phone number."
        )
        st.stop()

    if not address:

        st.error(
            "Please enter your delivery address."
        )
        st.stop()

    if not state:

        st.error(
            "Please enter your state."
        )
        st.stop()

    if not city:

        st.error(
            "Please enter your city."
        )
        st.stop()

    if not uploaded_file:

        st.error(
            "Please upload your payment proof."
        )
        st.stop()


    # -----------------------------
    # VALIDATE FILE
    # -----------------------------

    valid_file, file_message = validate_proof(
        uploaded_file
    )

    if not valid_file:

        st.error(
            file_message
        )
        st.stop()


    # -----------------------------
    # SAVE PROFILE
    # -----------------------------

    try:

        update_profile(
            user_id,
            full_name,
            phone,
        )

    except Exception:
        pass


    # -----------------------------
    # CREATE ORDER
    # -----------------------------

    cart_items = []

    for item in summary["items"]:

        cart_items.append(
            {
                "product_id": item["product_id"],
                "quantity": int(item["quantity"]),
            }
        )


    try:

        order = create_order(
            user_id=user_id,
            full_name=full_name,
            phone=phone,
            email=customer_email,
            address=address,
            state=state,
            city=city,
            additional_info=additional_info,
            cart_items=cart_items,
        )

    except Exception as e:

        st.error(
            "We could not create your order. "
            "Please try again."
        )

        st.stop()


    # ------------------------------------------------
    # GET ORDER ID
    # ------------------------------------------------

    order_id = None

    if isinstance(order, dict):

        order_id = (
            order.get("id")
            or order.get("order_id")
        )

    elif isinstance(order, list) and order:

        first = order[0]

        if isinstance(first, dict):

            order_id = (
                first.get("id")
                or first.get("order_id")
            )


    if not order_id:

        st.error(
            "The order was created, but no order ID was returned."
        )

        st.stop()


    # ------------------------------------------------
    # SUBMIT PAYMENT PROOF
    # ------------------------------------------------

    try:

        # This passes the uploaded file metadata.
        # The secure backend should associate it with
        # the authenticated order.

        file_reference = {
            "filename": uploaded_file.name,
            "size": uploaded_file.size,
            "type": uploaded_file.type,
        }

        submit_payment_proof(
            order_id=order_id,
            payment_method=selected_payment,
            file_reference=file_reference,
        )

    except Exception:

        st.warning(
            "Your order was created, but the payment proof "
            "could not be registered. Please contact support."
        )


    # ------------------------------------------------
    # CLEAR CART
    # ------------------------------------------------

    clear_cart()

    st.session_state.last_order_id = str(
        order_id
    )

    st.session_state.last_order_total = float(
        summary["total"]
    )

    st.session_state.last_payment_method = (
        selected_payment
    )

    st.switch_page(
        "pages/order_success.py"
    )