-- =========================================================
-- CHANGE2.COM DATABASE
-- =========================================================

create extension if not exists "pgcrypto";


-- =========================================================
-- PROFILES
-- =========================================================

create table if not exists public.profiles (
    id uuid primary key references auth.users(id) on delete cascade,
    full_name text,
    phone text,
    role text not null default 'customer'
        check (role in ('customer', 'admin')),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);


-- =========================================================
-- PRODUCTS
-- =========================================================

create table if not exists public.products (
    id uuid primary key default gen_random_uuid(),

    name text not null,
    description text default '',
    category text default 'General',

    price numeric(12,2) not null default 0
        check (price >= 0),

    stock integer not null default 0
        check (stock >= 0),

    image_url text default '',

    active boolean not null default true,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);


-- =========================================================
-- ORDERS
-- =========================================================

create table if not exists public.orders (
    id uuid primary key default gen_random_uuid(),

    user_id uuid not null
        references auth.users(id)
        on delete restrict,

    full_name text not null,
    phone text not null,
    email text not null,

    address text not null,
    state text not null,
    city text not null,

    additional_info text default '',

    subtotal numeric(12,2) not null default 0,
    delivery_fee numeric(12,2) not null default 0,
    total numeric(12,2) not null default 0,

    status text not null default 'pending'
        check (
            status in (
                'pending',
                'confirmed',
                'processing',
                'shipped',
                'delivered',
                'cancelled'
            )
        ),

    payment_status text not null default 'pending'
        check (
            payment_status in (
                'pending',
                'approved',
                'rejected'
            )
        ),

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);


-- =========================================================
-- ORDER ITEMS
-- =========================================================

create table if not exists public.order_items (
    id uuid primary key default gen_random_uuid(),

    order_id uuid not null
        references public.orders(id)
        on delete cascade,

    product_id uuid
        references public.products(id)
        on delete set null,

    product_name text not null,
    unit_price numeric(12,2) not null default 0,
    quantity integer not null
        check (quantity > 0),

    subtotal numeric(12,2) not null default 0,

    created_at timestamptz not null default now()
);


-- =========================================================
-- PAYMENT METHODS
-- =========================================================

create table if not exists public.payment_methods (
    id uuid primary key default gen_random_uuid(),

    name text not null unique,
    instructions text default '',

    enabled boolean not null default true,

    sort_order integer not null default 0,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);


-- =========================================================
-- PAYMENT PROOFS
-- =========================================================

create table if not exists public.payment_proofs (
    id uuid primary key default gen_random_uuid(),

    order_id uuid not null
        references public.orders(id)
        on delete cascade,

    user_id uuid not null
        references auth.users(id)
        on delete cascade,

    payment_method text not null,

    file_reference jsonb,

    verification_status text not null default 'pending'
        check (
            verification_status in (
                'pending',
                'approved',
                'rejected'
            )
        ),

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);


-- =========================================================
-- STORE SETTINGS
-- =========================================================

create table if not exists public.store_settings (
    id uuid primary key default gen_random_uuid(),

    setting_key text not null unique,
    setting_value text not null default '',

    updated_at timestamptz not null default now()
);


-- =========================================================
-- INDEXES
-- =========================================================

create index if not exists products_category_idx
on public.products(category);

create index if not exists products_active_idx
on public.products(active);

create index if not exists orders_user_id_idx
on public.orders(user_id);

create index if not exists orders_status_idx
on public.orders(status);

create index if not exists payment_proofs_order_id_idx
on public.payment_proofs(order_id);

create index if not exists payment_proofs_status_idx
on public.payment_proofs(verification_status);


-- =========================================================
-- PROFILE CREATION TRIGGER
-- =========================================================

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin

    insert into public.profiles (
        id,
        full_name
    )

    values (
        new.id,
        coalesce(
            new.raw_user_meta_data ->> 'full_name',
            ''
        )
    )

    on conflict (id)
    do nothing;

    return new;

end;
$$;


drop trigger if exists on_auth_user_created
on auth.users;


create trigger on_auth_user_created

after insert on auth.users

for each row

execute procedure public.handle_new_user();


-- =========================================================
-- ADMIN CHECK
-- =========================================================

create or replace function public.is_admin()
returns boolean
language sql
stable
security definer
set search_path = public
as $$

    select exists (
        select 1
        from public.profiles
        where id = auth.uid()
        and role = 'admin'
    );

$$;


-- =========================================================
-- UPDATED_AT FUNCTION
-- =========================================================

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$

begin

    new.updated_at = now();

    return new;

end;

$$;


-- =========================================================
-- UPDATED_AT TRIGGERS
-- =========================================================

drop trigger if exists profiles_updated_at
on public.profiles;

create trigger profiles_updated_at

before update on public.profiles

for each row

execute procedure public.set_updated_at();


drop trigger if exists products_updated_at
on public.products;

create trigger products_updated_at

before update on public.products

for each row

execute procedure public.set_updated_at();


drop trigger if exists orders_updated_at
on public.orders;

create trigger orders_updated_at

before update on public.orders

for each row

execute procedure public.set_updated_at();


drop trigger if exists payment_methods_updated_at
on public.payment_methods;

create trigger payment_methods_updated_at

before update on public.payment_methods

for each row

execute procedure public.set_updated_at();


drop trigger if exists payment_proofs_updated_at
on public.payment_proofs;

create trigger payment_proofs_updated_at

before update on public.payment_proofs

for each row

execute procedure public.set_updated_at();


-- =========================================================
-- ENABLE RLS
-- =========================================================

alter table public.profiles enable row level security;
alter table public.products enable row level security;
alter table public.orders enable row level security;
alter table public.order_items enable row level security;
alter table public.payment_methods enable row level security;
alter table public.payment_proofs enable row level security;
alter table public.store_settings enable row level security;


-- =========================================================
-- PROFILES POLICIES
-- =========================================================

drop policy if exists
"Users can view own profile"
on public.profiles;

create policy
"Users can view own profile"

on public.profiles

for select

to authenticated

using (
    id = auth.uid()
    or public.is_admin()
);


drop policy if exists
"Users can update own profile"
on public.profiles;

create policy
"Users can update own profile"

on public.profiles

for update

to authenticated

using (
    id = auth.uid()
    or public.is_admin()
)

with check (
    id = auth.uid()
    or public.is_admin()
);


-- =========================================================
-- PRODUCT POLICIES
-- =========================================================

drop policy if exists
"Anyone can view active products"
on public.products;

create policy
"Anyone can view active products"

on public.products

for select

using (
    active = true
    or public.is_admin()
);


drop policy if exists
"Admins can insert products"
on public.products;

create policy
"Admins can insert products"

on public.products

for insert

to authenticated

with check (
    public.is_admin()
);


drop policy if exists
"Admins can update products"
on public.products;

create policy
"Admins can update products"

on public.products

for update

to authenticated

using (
    public.is_admin()
)

with check (
    public.is_admin()
);


drop policy if exists
"Admins can delete products"
on public.products;

create policy
"Admins can delete products"

on public.products

for delete

to authenticated

using (
    public.is_admin()
);


-- =========================================================
-- ORDER POLICIES
-- =========================================================

drop policy if exists
"Users can view own orders"
on public.orders;

create policy
"Users can view own orders"

on public.orders

for select

to authenticated

using (
    user_id = auth.uid()
    or public.is_admin()
);


drop policy if exists
"Admins can update orders"
on public.orders;

create policy
"Admins can update orders"

on public.orders

for update

to authenticated

using (
    public.is_admin()
)

with check (
    public.is_admin()
);


-- =========================================================
-- ORDER ITEM POLICIES
-- =========================================================

drop policy if exists
"Users can view own order items"
on public.order_items;

create policy
"Users can view own order items"

on public.order_items

for select

to authenticated

using (
    exists (
        select 1
        from public.orders o
        where o.id = order_items.order_id
        and (
            o.user_id = auth.uid()
            or public.is_admin()
        )
    )
);


-- =========================================================
-- PAYMENT METHOD POLICIES
-- =========================================================

drop policy if exists
"Anyone can view enabled payment methods"
on public.payment_methods;

create policy
"Anyone can view enabled payment methods"

on public.payment_methods

for select

using (
    enabled = true
    or public.is_admin()
);


drop policy if exists
"Admins can insert payment methods"
on public.payment_methods;

create policy
"Admins can insert payment methods"

on public.payment_methods

for insert

to authenticated

with check (
    public.is_admin()
);


drop policy if exists
"Admins can update payment methods"
on public.payment_methods;

create policy
"Admins can update payment methods"

on public.payment_methods

for update

to authenticated

using (
    public.is_admin()
)

with check (
    public.is_admin()
);


-- =========================================================
-- PAYMENT PROOF POLICIES
-- =========================================================

drop policy if exists
"Users can view own payment proofs"
on public.payment_proofs;

create policy
"Users can view own payment proofs"

on public.payment_proofs

for select

to authenticated

using (
    user_id = auth.uid()
    or public.is_admin()
);


-- =========================================================
-- STORE SETTINGS
-- =========================================================

drop policy if exists
"Anyone can read store settings"
on public.store_settings;

create policy
"Anyone can read store settings"

on public.store_settings

for select

using (
    true
);


drop policy if exists
"Admins can update store settings"
on public.store_settings;

create policy
"Admins can update store settings"

on public.store_settings

for update

to authenticated

using (
    public.is_admin()
)

with check (
    public.is_admin()
);


drop policy if exists
"Admins can insert store settings"
on public.store_settings;

create policy
"Admins can insert store settings"

on public.store_settings

for insert

to authenticated

with check (
    public.is_admin()
);


-- =========================================================
-- SECURE ORDER CREATION
-- =========================================================

create or replace function public.create_order_secure(
    p_full_name text,
    p_phone text,
    p_email text,
    p_address text,
    p_state text,
    p_city text,
    p_additional_info text,
    p_items jsonb
)

returns jsonb

language plpgsql

security invoker

set search_path = public

as $$

declare

    v_order_id uuid;

    v_subtotal numeric(12,2) := 0;

    v_delivery_fee numeric(12,2) := 0;

    v_total numeric(12,2) := 0;

    v_item jsonb;

    v_product public.products%rowtype;

    v_quantity integer;

    v_item_subtotal numeric(12,2);

begin

    if auth.uid() is null then
        raise exception 'Authentication required';
    end if;


    if p_items is null
       or jsonb_array_length(p_items) = 0 then

        raise exception 'Cart is empty';

    end if;


    -- Lock products while checking stock.

    for v_item in
        select value
        from jsonb_array_elements(p_items)
    loop

        select *
        into v_product

        from public.products

        where id = (v_item ->> 'product_id')::uuid
        and active = true

        for update;


        if not found then

            raise exception
                'One of the products is unavailable';

        end if;


        v_quantity =
            (v_item ->> 'quantity')::integer;


        if v_quantity <= 0 then

            raise exception
                'Invalid product quantity';

        end if;


        if v_quantity > v_product.stock then

            raise exception
                'Not enough stock for %',
                v_product.name;

        end if;


        v_item_subtotal =
            v_product.price * v_quantity;


        v_subtotal =
            v_subtotal + v_item_subtotal;

    end loop;


    -- Delivery fee.

    select coalesce(
        nullif(setting_value, '')::numeric,
        0
    )

    into v_delivery_fee

    from public.store_settings

    where setting_key = 'delivery_fee';


    v_delivery_fee =
        coalesce(v_delivery_fee, 0);


    v_total =
        v_subtotal + v_delivery_fee;


    -- Create order.

    insert into public.orders (

        user_id,
        full_name,
        phone,
        email,

        address,
        state,
        city,
        additional_info,

        subtotal,
        delivery_fee,
        total

    )

    values (

        auth.uid(),
        p_full_name,
        p_phone,
        p_email,

        p_address,
        p_state,
        p_city,
        coalesce(p_additional_info, ''),

        v_subtotal,
        v_delivery_fee,
        v_total

    )

    returning id

    into v_order_id;


    -- Create order items and reduce stock.

    for v_item in
        select value
        from jsonb_array_elements(p_items)
    loop

        select *
        into v_product

        from public.products

        where id = (v_item ->> 'product_id')::uuid
        for update;


        v_quantity =
            (v_item ->> 'quantity')::integer;


        v_item_subtotal =
            v_product.price * v_quantity;


        insert into public.order_items (

            order_id,
            product_id,
            product_name,
            unit_price,
            quantity,
            subtotal

        )

        values (

            v_order_id,
            v_product.id,
            v_product.name,
            v_product.price,
            v_quantity,
            v_item_subtotal

        );


        update public.products

        set stock = stock - v_quantity

        where id = v_product.id;

    end loop;


    return jsonb_build_object(
        'id', v_order_id,
        'subtotal', v_subtotal,
        'delivery_fee', v_delivery_fee,
        'total', v_total
    );

end;

$$;


-- =========================================================
-- SECURE PAYMENT PROOF
-- =========================================================

create or replace function public.submit_payment_proof_secure(
    p_order_id uuid,
    p_payment_method text,
    p_file_reference jsonb
)

returns jsonb

language plpgsql

security invoker

set search_path = public

as $$

declare

    v_proof_id uuid;

begin

    if auth.uid() is null then
        raise exception 'Authentication required';
    end if;


    if not exists (

        select 1

        from public.orders

        where id = p_order_id

        and user_id = auth.uid()

    ) then

        raise exception
            'Order does not belong to current user';

    end if;


    insert into public.payment_proofs (

        order_id,
        user_id,
        payment_method,
        file_reference

    )

    values (

        p_order_id,
        auth.uid(),
        p_payment_method,
        p_file_reference

    )

    returning id

    into v_proof_id;


    return jsonb_build_object(
        'id', v_proof_id,
        'order_id', p_order_id,
        'status', 'pending'
    );

end;

$$;


-- =========================================================
-- DEFAULT STORE SETTINGS
-- =========================================================

insert into public.store_settings (
    setting_key,
    setting_value
)

values (
    'Bank Transfer',
    'Contact the store for the current bank payment details.',
    true,
    1
),

(
    'Gift Card',
    'Follow the store instructions for gift-card payment.',
    true,
    2
),

(
    'Bitcoin',
    'Contact the store for the current Bitcoin payment details.',
    true,
    3
)

on conflict (name)
do nothing;
   