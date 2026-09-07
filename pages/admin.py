import streamlit as st

from utils.auth import require_admin
from utils.database import (
    get_products,
    create_product,
    update_product,
    delete_product,
    get_all_orders,
    update_order_status,
    get_payment_proofs,
    update_payment_status,
    get_payment_methods,
    create_payment_method,
    update_payment_method,
    get_store_setting,
    update_store_setting,
    get_sales_statistics,
)
from utils.ui import (
    inject_css,
    money,
    page_title,
)

st.set_page_config(
    page_title="Admin | Change2.com",
    page_icon="⚙️",
    layout="wide",
)

inject_css()

require_admin()

page_title(
    "Admin Dashboard",
    "Manage your Change2.com store.",
)


# ==================================================
# DASHBOARD STATISTICS
# ==================================================

stats = get_sales_statistics() or {}

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Orders",
        stats.get("orders", 0),
    )

with c2:
    st.metric(
        "Revenue",
        money(stats.get("revenue", 0)),
    )

with c3:
    st.metric(
        "Products",
        stats.get("products", 0),
    )

with c4:
    st.metric(
        "Pending Payments",
        stats.get("pending_payments", 0),
    )


st.divider()


# ==================================================
# TABS
# ==================================================

(
    products_tab,
    orders_tab,
    payments_tab,
    methods_tab,
    settings_tab,
) = st.tabs(
    [
        "Products",
        "Orders",
        "Payments",
        "Payment Methods",
        "Settings",
    ]
)


# ==================================================
# PRODUCTS
# ==================================================

with products_tab:

    st.subheader("Add Product")

    with st.form("add_product_form"):

        name = st.text_input(
            "Product name"
        )

        description = st.text_area(
            "Description"
        )

        category = st.text_input(
            "Category"
        )

        price = st.number_input(
            "Price",
            min_value=0.0,
            step=100.0,
        )

        stock = st.number_input(
            "Stock",
            min_value=0,
            step=1,
        )

        image_url = st.text_input(
            "Image URL",
            placeholder="https://..."
        )

        submitted = st.form_submit_button(
            "Add Product",
            type="primary",
        )

        if submitted:

            if not name.strip():

                st.error(
                    "Product name is required."
                )

            else:

                success = create_product(
                    name=name,
                    description=description,
                    category=category,
                    price=price,
                    stock=stock,
                    image_url=image_url,
                )

                if success:

                    st.success(
                        "Product added successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unable to add product."
                    )


    st.divider()

    st.subheader(
        "Existing Products"
    )

    products = get_products()

    if not products:

        st.info(
            "There are no products yet."
        )

    else:

        for product in products:

            product_id = product["id"]

            with st.expander(
                f"{product.get('name', 'Product')} — "
                f"{money(product.get('price', 0))}"
            ):

                new_name = st.text_input(
                    "Name",
                    value=product.get(
                        "name",
                        "",
                    ),
                    key=f"name_{product_id}",
                )

                new_description = st.text_area(
                    "Description",
                    value=product.get(
                        "description",
                        "",
                    ),
                    key=f"description_{product_id}",
                )

                new_category = st.text_input(
                    "Category",
                    value=product.get(
                        "category",
                        "",
                    ),
                    key=f"category_{product_id}",
                )

                new_price = st.number_input(
                    "Price",
                    min_value=0.0,
                    value=float(
                        product.get(
                            "price",
                            0,
                        )
                    ),
                    key=f"price_{product_id}",
                )

                new_stock = st.number_input(
                    "Stock",
                    min_value=0,
                    value=int(
                        product.get(
                            "stock",
                            0,
                        )
                    ),
                    key=f"stock_{product_id}",
                )

                new_image = st.text_input(
                    "Image URL",
                    value=product.get(
                        "image_url",
                        "",
                    ),
                    key=f"image_{product_id}",
                )

                a, b = st.columns(2)

                with a:

                    if st.button(
                        "Save Product",
                        key=f"save_{product_id}",
                        type="primary",
                        use_container_width=True,
                    ):

                        success = update_product(
                            product_id,
                            new_name,
                            new_description,
                            new_category,
                            new_price,
                            new_stock,
                            new_image,
                        )

                        if success:
                            st.success(
                                "Product updated."
                            )
                            st.rerun()
                        else:
                            st.error(
                                "Update failed."
                            )

                with b:

                    if st.button(
                        "Delete Product",
                        key=f"delete_{product_id}",
                        use_container_width=True,
                    ):

                        success = delete_product(
                            product_id
                        )

                        if success:
                            st.success(
                                "Product deleted."
                            )
                            st.rerun()
                        else:
                            st.error(
                                "Delete failed."
                            )


# ==================================================
# ORDERS
# ==================================================

with orders_tab:

    st.subheader("Customer Orders")

    orders = get_all_orders()

    if not orders:

        st.info(
            "There are no orders yet."
        )

    else:

        for order in orders:

            order_id = order.get("id")

            with st.expander(
                f"Order #{str(order_id)[:12]} — "
                f"{money(order.get('total', 0))}"
            ):

                st.write(
                    f"**Customer:** "
                    f"{order.get('full_name', '')}"
                )

                st.write(
                    f"**Email:** "
                    f"{order.get('email', '')}"
                )

                st.write(
                    f"**Phone:** "
                    f"{order.get('phone', '')}"
                )

                st.write(
                    f"**Address:** "
                    f"{order.get('address', '')}"
                )

                st.write(
                    f"**City:** "
                    f"{order.get('city', '')}"
                )

                st.write(
                    f"**State:** "
                    f"{order.get('state', '')}"
                )

                st.write(
                    f"**Total:** "
                    f"{money(order.get('total', 0))}"
                )

                current_status = order.get(
                    "status",
                    "pending",
                )

                statuses = [
                    "pending",
                    "confirmed",
                    "processing",
                    "shipped",
                    "delivered",
                    "cancelled",
                ]

                selected_status = st.selectbox(
                    "Order status",
                    statuses,
                    index=(
                        statuses.index(
                            current_status
                        )
                        if current_status in statuses
                        else 0
                    ),
                    key=f"order_status_{order_id}",
                )

                if st.button(
                    "Update Order",
                    key=f"update_order_{order_id}",
                    type="primary",
                ):

                    if update_order_status(
                        order_id,
                        selected_status,
                    ):

                        st.success(
                            "Order status updated."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Unable to update order."
                        )


# ==================================================
# PAYMENTS
# ==================================================

with payments_tab:

    st.subheader(
        "Payment Verification"
    )

    proofs = get_payment_proofs()

    if not proofs:

        st.info(
            "No payment proofs submitted."
        )

    else:

        for proof in proofs:

            proof_id = proof.get(
                "id"
            )

            order_id = proof.get(
                "order_id"
            )

            current = proof.get(
                "verification_status",
                "pending",
            )

            with st.expander(
                f"Payment #{str(proof_id)[:12]} — "
                f"Order #{str(order_id)[:12]}"
            ):

                st.write(
                    f"**Payment method:** "
                    f"{proof.get('payment_method', '')}"
                )

                st.write(
                    f"**Current status:** "
                    f"{current}"
                )

                reference = proof.get(
                    "file_reference"
                )

                if reference:

                    st.json(
                        reference
                    )

                statuses = [
                    "pending",
                    "approved",
                    "rejected",
                ]

                selected = st.selectbox(
                    "Verification status",
                    statuses,
                    index=(
                        statuses.index(current)
                        if current in statuses
                        else 0
                    ),
                    key=f"proof_status_{proof_id}",
                )

                if st.button(
                    "Save Verification",
                    key=f"verify_{proof_id}",
                    type="primary",
                ):

                    success = update_payment_status(
                        proof_id,
                        selected,
                        order_id,
                    )

                    if success:

                        st.success(
                            "Payment status updated."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Unable to update payment."
                        )


# ==================================================
# PAYMENT METHODS
# ==================================================

with methods_tab:

    st.subheader(
        "Payment Methods"
    )

    st.caption(
        "Only enable payment methods that your store "
        "actually supports."
    )

    with st.form(
        "new_payment_method"
    ):

        method_name = st.text_input(
            "Method name",
            placeholder="Example: Bank Transfer",
        )

        instructions = st.text_area(
            "Payment instructions",
            placeholder=(
                "Explain how customers should complete payment."
            ),
        )

        add_method = st.form_submit_button(
            "Add Payment Method",
            type="primary",
        )

        if add_method:

            if not method_name.strip():

                st.error(
                    "Enter a payment method name."
                )

            else:

                success = create_payment_method(
                    method_name,
                    instructions,
                )

                if success:

                    st.success(
                        "Payment method created."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unable to create payment method."
                    )


    st.divider()

    methods = get_payment_methods(
        enabled_only=False
    )

    for method in methods:

        method_id = method["id"]

        with st.expander(
            method.get(
                "name",
                "Payment method",
            )
        ):

            name = st.text_input(
                "Name",
                value=method.get(
                    "name",
                    "",
                ),
                key=f"method_name_{method_id}",
            )

            instructions = st.text_area(
                "Instructions",
                value=method.get(
                    "instructions",
                    "",
                ),
                key=f"method_instructions_{method_id}",
            )

            enabled = st.checkbox(
                "Enabled",
                value=bool(
                    method.get(
                        "enabled",
                        True,
                    )
                ),
                key=f"method_enabled_{method_id}",
            )

            if st.button(
                "Save",
                key=f"save_method_{method_id}",
                type="primary",
            ):

                success = update_payment_method(
                    method_id,
                    name,
                    instructions,
                    enabled,
                )

                if success:

                    st.success(
                        "Payment method updated."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Update failed."
                    )


# ==================================================
# SETTINGS
# ==================================================

with settings_tab:

    st.subheader(
        "Store Settings"
    )

    current_fee = get_store_setting(
        "delivery_fee"
    )

    try:
        current_fee = float(
            current_fee or 0
        )
    except Exception:
        current_fee = 0.0

    delivery_fee = st.number_input(
        "Delivery fee",
        min_value=0.0,
        value=current_fee,
        step=100.0,
    )

    if st.button(
        "Save Delivery Fee",
        type="primary",
    ):

        success = update_store_setting(
            "delivery_fee",
            str(delivery_fee),
        )

        if success:

            st.success(
                "Delivery fee updated."
            )

        else:

            st.error(
                "Unable to update delivery fee."
            )

    st.divider()

    st.info(
        "More store settings can be added here later, "
        "including store name, support email, currency and "
        "delivery regions."
    )