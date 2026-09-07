import streamlit as st

from .database import get_product, get_store_setting


# =========================================================
# CART INITIALIZATION
# =========================================================

def init_cart():
    """Create the cart in Streamlit session state."""

    if "cart" not in st.session_state:
        st.session_state.cart = {}


# =========================================================
# CART COUNT
# =========================================================

def cart_count():
    """Return the total number of products in the cart."""

    init_cart()

    return sum(
        int(quantity)
        for quantity in st.session_state.cart.values()
    )


# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart(product_id, quantity=1):
    """
    Add a product to the cart.

    Stock is checked before adding.
    """

    init_cart()

    product = get_product(product_id)

    if not product:
        return False, "Product not found."

    stock = int(product.get("stock", 0))

    if stock <= 0:
        return False, "This product is out of stock."

    product_id = str(product_id)

    current_quantity = int(
        st.session_state.cart.get(product_id, 0)
    )

    new_quantity = current_quantity + int(quantity)

    if new_quantity > stock:
        return False, (
            f"Only {stock} unit(s) are currently available."
        )

    st.session_state.cart[product_id] = new_quantity

    return True, f"{product['name']} added to your cart."


# =========================================================
# REMOVE FROM CART
# =========================================================

def remove_from_cart(product_id):
    """Remove a product completely."""

    init_cart()

    product_id = str(product_id)

    if product_id in st.session_state.cart:
        del st.session_state.cart[product_id]

    return True


# =========================================================
# CLEAR CART
# =========================================================

def clear_cart():
    """Remove every product from the cart."""

    st.session_state.cart = {}


# =========================================================
# UPDATE QUANTITY
# =========================================================

def update_quantity(product_id, quantity):
    """
    Change the quantity of a product.

    Quantity cannot exceed current stock.
    """

    init_cart()

    product_id = str(product_id)

    product = get_product(product_id)

    if not product:
        remove_from_cart(product_id)
        return False, "Product no longer exists."

    stock = int(product.get("stock", 0))

    quantity = int(quantity)

    if quantity <= 0:
        remove_from_cart(product_id)
        return True, "Product removed."

    if stock <= 0:
        remove_from_cart(product_id)
        return False, "Product is out of stock."

    if quantity > stock:
        quantity = stock

    st.session_state.cart[product_id] = quantity

    return True, "Cart updated."


# =========================================================
# GET CART ITEMS
# =========================================================

def get_cart_items():
    """
    Build a complete cart using current database
    product information.

    Prices and stock are always refreshed from Supabase.
    """

    init_cart()

    items = []

    # Copy IDs because products may be removed
    product_ids = list(
        st.session_state.cart.keys()
    )

    for product_id in product_ids:

        quantity = int(
            st.session_state.cart.get(
                product_id,
                0
            )
        )

        if quantity <= 0:
            remove_from_cart(product_id)
            continue

        product = get_product(product_id)

        # Product was deleted
        if not product:
            remove_from_cart(product_id)
            continue

        stock = int(
            product.get("stock", 0)
        )

        # Product became out of stock
        if stock <= 0:
            remove_from_cart(product_id)
            continue

        # Product stock changed after it was added
        if quantity > stock:

            quantity = stock

            st.session_state.cart[
                product_id
            ] = quantity

        price = float(
            product.get("price", 0)
        )

        subtotal = price * quantity

        items.append(
            {
                "product_id": product_id,
                "name": product.get(
                    "name",
                    "Unnamed product"
                ),
                "description": product.get(
                    "description",
                    ""
                ),
                "image_url": product.get(
                    "image_url",
                    ""
                ),
                "category": product.get(
                    "category",
                    ""
                ),
                "price": price,
                "quantity": quantity,
                "stock": stock,
                "subtotal": subtotal,
            }
        )

    return items


# =========================================================
# SUBTOTAL
# =========================================================

def cart_subtotal():
    """Calculate cart subtotal."""

    items = get_cart_items()

    return sum(
        float(item["subtotal"])
        for item in items
    )


# =========================================================
# DELIVERY FEE
# =========================================================

def delivery_fee():
    """
    Get the configured delivery fee.

    The setting is stored in Supabase.
    """

    try:

        value = get_store_setting(
            "delivery_fee"
        )

        if value is None:
            return 0.0

        return float(value)

    except Exception:
        return 0.0


# =========================================================
# TOTAL
# =========================================================

def cart_total():
    """Calculate subtotal + delivery fee."""

    subtotal = cart_subtotal()

    fee = delivery_fee()

    return subtotal + fee


# =========================================================
# CART SUMMARY
# =========================================================

def cart_summary():
    """
    Return all important cart totals.
    """

    items = get_cart_items()

    subtotal = sum(
        float(item["subtotal"])
        for item in items
    )

    fee = delivery_fee()

    total = subtotal + fee

    quantity = sum(
        int(item["quantity"])
        for item in items
    )

    return {
        "items": items,
        "quantity": quantity,
        "subtotal": subtotal,
        "delivery_fee": fee,
        "total": total,
    }


# =========================================================
# CART VALIDATION
# =========================================================

def validate_cart():
    """
    Check whether every cart item is still valid.

    This is a client-side pre-check.

    The final checkout is still validated again
    by the secure database function.
    """

    init_cart()

    errors = []

    items = get_cart_items()

    if not items:
        errors.append(
            "Your cart is empty."
        )
        return False, errors

    for item in items:

        product = get_product(
            item["product_id"]
        )

        if not product:
            errors.append(
                f"{item['name']} is no longer available."
            )
            continue

        stock = int(
            product.get("stock", 0)
        )

        quantity = int(
            item["quantity"]
        )

        if stock <= 0:

            errors.append(
                f"{item['name']} is out of stock."
            )

        elif quantity > stock:

            errors.append(
                f"{item['name']} only has "
                f"{stock} unit(s) available."
            )

    return len(errors) == 0, errors


# =========================================================
# CHECK IF CART IS EMPTY
# =========================================================

def cart_is_empty():
    """Return True when there are no cart items."""

    init_cart()

    return len(
        st.session_state.cart
    ) == 0