import streamlit as st

from utils.database import (
    get_categories,
    search_products,
)
from utils.cart import add_to_cart, cart_count
from utils.ui import (
    inject_css,
    product_card,
    page_title,
)

st.set_page_config(
    page_title="Products | Change2.com",
    page_icon="🛍️",
    layout="wide",
)

inject_css()

page_title(
    "Products",
    "Browse the Change2.com marketplace.",
)

top1, top2 = st.columns([4, 1])

with top1:

    search = st.text_input(
        "Search products",
        placeholder="Search for a product...",
        label_visibility="collapsed",
    )

with top2:

    if st.button(
        f"🛒 Cart ({cart_count()})",
        use_container_width=True,
    ):
        st.switch_page("pages/cart.py")


categories = get_categories()

category_options = ["All"] + categories

category = st.selectbox(
    "Category",
    category_options,
)

products = search_products(
    search=search,
    category=category,
)

st.write("")

if not products:

    st.markdown(
        """
        <div class="empty-state">

            <div class="empty-icon">
                🔎
            </div>

            <h3>
                No products found
            </h3>

            <p>
                Try another search or category.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

else:

    st.caption(
        f"{len(products)} product(s) found"
    )

    for start in range(
        0,
        len(products),
        4,
    ):

        row = products[start:start + 4]

        columns = st.columns(4)

        for column, product in zip(
            columns,
            row,
        ):

            with column:

                product_card(product)

                product_id = product["id"]

                if st.button(
                    "Add to Cart",
                    key=f"product_add_{product_id}",
                    use_container_width=True,
                ):

                    success, message = add_to_cart(
                        product_id,
                        1,
                    )

                    if success:
                        st.success(message)
                    else:
                        st.error(message)

st.write("")
st.write("")

if st.button(
    "← Back to Home",
    use_container_width=True,
):
    st.switch_page("app.py")