import streamlit as st
from .auth import get_supabase


# =========================================================
# PRODUCTS
# =========================================================

def get_products(limit=None):
    """Get available products."""

    try:
        supabase = get_supabase()

        query = (
            supabase
            .table("products")
            .select("*")
            .order("created_at", desc=True)
        )

        if limit:
            query = query.limit(limit)

        response = query.execute()

        return response.data or []

    except Exception as e:
        st.error(f"Unable to load products: {e}")
        return []


def get_product(product_id):
    """Get one product by ID."""

    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("products")
            .select("*")
            .eq("id", str(product_id))
            .single()
            .execute()
        )

        return response.data

    except Exception:
        return None


def search_products(search="", category="All"):
    """Search and filter products."""

    try:
        supabase = get_supabase()

        query = (
            supabase
            .table("products")
            .select("*")
            .order("created_at", desc=True)
        )

        if search:
            search = search.strip()

            query = query.or_(
                f"name.ilike.%{search}%,"
                f"description.ilike.%{search}%"
            )

        if category and category != "All":
            query = query.eq("category", category)

        response = query.execute()

        return response.data or []

    except Exception as e:
        st.error(f"Unable to search products: {e}")
        return []


def get_categories():
    """Return product categories."""

    products = get_products()

    categories = sorted(
        {
            product.get("category")
            for product in products
            if product.get("category")
        }
    )

    return ["All"] + categories


# =========================================================
# ADMIN PRODUCT MANAGEMENT
# =========================================================

def create_product(
    name,
    description,
    price,
    image_url,
    category,
    stock,
):
    """Create a product."""

    try:
        supabase = get_supabase()

        data = {
            "name": name.strip(),
            "description": description.strip(),
            "price": float(price),
            "image_url": image_url.strip(),
            "category": category.strip(),
            "stock": int(stock),
        }

        response = (
            supabase
            .table("products")
            .insert(data)
            .execute()
        )

        return response.data

    except Exception as e:
        st.error(f"Unable to create product: {e}")
        return None


def update_product(
    product_id,
    name,
    description,
    price,
    image_url,
    category,
    stock,
):
    """Update an existing product."""

    try:
        supabase = get_supabase()

        data = {
            "name": name.strip(),
            "description": description.strip(),
            "price": float(price),
            "image_url": image_url.strip(),
            "category": category.strip(),
            "stock": int(stock),
        }

        response = (
            supabase
            .table("products")
            .update(data)
            .eq("id", str(product_id))
            .execute()
        )

        return response.data

    except Exception as e:
        st.error(f"Unable to update product: {e}")
        return None


def delete_product(product_id):
    """Delete a product."""

    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("products")
            .delete()
            .eq("id", str(product_id))
            .execute()
        )

        return response.data

    except Exception as e:
        st.error(f"Unable to delete product: {e}")
        return None


# =========================================================
# PROFILE
# =========================================================

def get_profile(user_id):
    """Get a customer profile."""

    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("profiles")
            .select("*")
            .eq("id", str(user_id))
            .single()
            .execute()
        )

        return response.data

    except Exception:
        return None


def update_profile(
    user_id,
    full_name,
    phone,
):
    """Update customer profile."""

    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("profiles")
            .update(
                {
                    "full_name": full_name.strip(),
                    "phone": phone.strip(),
                }
            )
            .eq("id", str(user_id))
            .execute()
        )

        return response.data

    except Exception as e:
        st.error(f"Unable to update profile: {e}")
        return None


# =========================================================
# ORDERS
# =========================================================

def create_order(
    user_id,
    customer_name,
    email,
    phone,
    delivery_address,
    city,
    state,
    country,
    delivery_instructions,
    payment_method,
    cart_items,
):
    """
    Creates an order through the secure Supabase RPC.

    Prices, stock and totals are calculated server-side.
    """

    try:
        supabase = get_supabase()

        items = []

        for item in cart_items:

            items.append(
                {
                    "product_id": str(item["product_id"]),
                    "quantity": int(item["quantity"]),
                }
            )

        response = supabase.rpc(
            "create_order_secure",
            {
                "p_items": items,
                "p_customer_name": customer_name.strip(),
                "p_email": email.strip().lower(),
                "p_phone": phone.strip(),
                "p_delivery_address": delivery_address.strip(),
                "p_city": city.strip(),
                "p_state": state.strip(),
                "p_country": country.strip(),
                "p_delivery_instructions": (
                    delivery_instructions.strip()
                ),
                "p_payment_method": payment_method.strip(),
            },
        ).execute()

        return response.data

    except Exception as e:
        st.error(f"Unable to create order: {e}")
        return None


def get_my_orders(user_id):
    """Get orders belonging to the current customer."""

    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("orders")
            .select("*")
            .eq("user_id", str(user_id))
            .order("created_at", desc=True)
            .execute()
        )

        return response.data or []

    except Exception as e:
        st.error(f"Unable to load orders: {e}")
        return []


def get_order(order_id, user_id=None):
    """
    Get an order.

    When user_id is supplied, the query is restricted
    to that customer.
    """

    try:
        supabase = get_supabase()

        query = (
            supabase
            .table("orders")
            .select("*")
            .eq("id", str(order_id))
        )

        if user_id:
            query = query.eq(
                "user_id",
                str(user_id)
            )

        response = query.single().execute()

        return response.data

    except Exception:
        return None


def get_order_items(order_id):
    """Get items belonging to an order."""

    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("order_items")
            .select("*")
            .eq("order_id", str(order_id))
            .order("id")
            .execute()
        )

        return response.data or []

    except Exception:
        return []


# =========================================================
# ADMIN ORDERS
# =========================================================

def get_all_orders():
    """Get all orders for the admin dashboard."""

    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("orders")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        return response.data or []

    except Exception as e:
        st.error(f"Unable to load orders: {e}")
        return []


def update_order_status(
    order_id,
    status,
):
    """Update order status."""

    allowed_statuses = {
        "Order received",
        "Awaiting payment",
        "Payment submitted",
        "Payment under review",
        "Payment verified",
        "Processing",
        "Shipped",
        "Out for delivery",
        "Delivered",
        "Cancelled",
    }

    if status not in allowed_statuses:
        st.error("Invalid order status.")
        return None

    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("orders")
            .update(
                {
                    "order_status": status
                }
            )
            .eq("id", str(order_id))
            .execute()
        )

        return response.data

    except Exception as e:
        st.error(f"Unable to update order: {e}")
        return None


# =========================================================
# PAYMENT METHODS
# =========================================================

def get_payment_methods(enabled_only=True):
    """Get configured payment methods."""

    try:
        supabase = get_supabase()

        query = (
            supabase
            .table("payment_methods")
            .select("*")
            .order("sort_order")
        )

        if enabled_only:
            query = query.eq("enabled", True)

        response = query.execute()

        return response.data or []

    except Exception as e:
        st.error(f"Unable to load payment methods: {e}")
        return []


def create_payment_method(
    name,
    instructions,
):
    """Create a payment method."""

    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("payment_methods")
            .insert(
                {
                    "name": name.strip(),
                    "instructions": instructions.strip(),
                    "enabled": True,
                }
            )
            .execute()
        )

        return response.data

    except Exception as e:
        st.error(f"Unable to create payment method: {e}")
        return None


def update_payment_method(
    method_id,
    name,
    instructions,
    enabled,
):
    """Update payment method."""

    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("payment_methods")
            .update(
                {
                    "name": name.strip(),
                    "instructions": instructions.strip(),
                    "enabled": bool(enabled),
                }
            )
            .eq("id", str(method_id))
            .execute()
        )

        return response.data

    except Exception as e:
        st.error(f"Unable to update payment method: {e}")
        return None


# =========================================================
# PAYMENT PROOFS
# =========================================================

def submit_payment_proof(
    order_id,
    payment_method,
    file_reference,
):
    """
    Securely associates an uploaded payment proof
    with an order.
    """

    try:
        supabase = get_supabase()

        response = supabase.rpc(
            "submit_payment_proof_secure",
            {
                "p_order_id": str(order_id),
                "p_payment_method": payment_method.strip(),
                "p_file_reference": file_reference,
            },
        ).execute()

        return response.data

    except Exception as e:
        st.error(
            f"Unable to submit payment proof: {e}"
        )
        return None


def get_payment_proofs(order_id=None):
    """Get payment proofs."""

    try:
        supabase = get_supabase()

        query = (
            supabase
            .table("payment_proofs")
            .select("*")
            .order("uploaded_at", desc=True)
        )

        if order_id:
            query = query.eq(
                "order_id",
                str(order_id)
            )

        response = query.execute()

        return response.data or []

    except Exception as e:
        st.error(
            f"Unable to load payment proofs: {e}"
        )
        return []


def update_payment_status(
    proof_id,
    verification_status,
    order_id=None,
):
    """Admin updates payment verification."""

    allowed = {
        "pending",
        "verified",
        "rejected",
    }

    if verification_status not in allowed:
        st.error("Invalid verification status.")
        return None

    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("payment_proofs")
            .update(
                {
                    "verification_status":
                        verification_status
                }
            )
            .eq("id", str(proof_id))
            .execute()
        )

        if (
            order_id
            and verification_status == "verified"
        ):
            update_order_status(
                order_id,
                "Payment verified"
            )

        elif (
            order_id
            and verification_status == "rejected"
        ):
            update_order_status(
                order_id,
                "Awaiting payment"
            )

        return response.data

    except Exception as e:
        st.error(
            f"Unable to update payment status: {e}"
        )
        return None


# =========================================================
# STORE SETTINGS
# =========================================================

def get_store_setting(key):
    """Get one store setting."""

    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("store_settings")
            .select("value")
            .eq("key", key)
            .single()
            .execute()
        )

        if response.data:
            return response.data.get("value")

    except Exception:
        pass

    return None


def update_store_setting(
    key,
    value,
):
    """Update a store setting."""

    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("store_settings")
            .upsert(
                {
                    "key": key,
                    "value": str(value),
                }
            )
            .execute()
        )

        return response.data

    except Exception as e:
        st.error(
            f"Unable to update store setting: {e}"
        )
        return None


# =========================================================
# ADMIN STATISTICS
# =========================================================

def get_sales_statistics():
    """Calculate basic sales statistics."""

    orders = get_all_orders()

    completed = [
        order
        for order in orders
        if order.get("payment_status") == "verified"
        and order.get("order_status") != "Cancelled"
    ]

    total_sales = sum(
        float(order.get("total") or 0)
        for order in completed
    )

    total_orders = len(orders)

    paid_orders = len(completed)

    pending_orders = len(
        [
            order
            for order in orders
            if order.get("payment_status")
            in {
                "pending",
                "under_review",
            }
        ]
    )

    delivered_orders = len(
        [
            order
            for order in orders
            if order.get("order_status")
            == "Delivered"
        ]
    )

    return {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "paid_orders": paid_orders,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
    }