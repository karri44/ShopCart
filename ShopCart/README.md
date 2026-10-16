# ShopCart — Everyday, upgraded

A complete local Django e-commerce portfolio project built on your original ShopCart source and product images. Responsive server-rendered HTML/CSS, a small progressive-enhancement JavaScript layer, Django authentication, SQLite, and a read-only JSON product API.

## Start on Windows (PowerShell or Command Prompt)

Install Python 3.10 or newer (tested with Python 3.12). Extract this ZIP first, then open a terminal in the ShopCart folder containing `manage.py`.

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py seed_demo
.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser. Keep the terminal open. Stop with Ctrl+C. To run it again, only the final command is needed. No PostgreSQL installation or database password is required. An internet connection is needed to install Django; product images, styling and scripts are local.

Alternatively, after installing Python and extracting the ZIP, double-click `start_windows.bat`. It creates the environment, installs Django, prepares the database and starts the server. It may need internet access for installation.

## macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_demo
.venv/bin/python manage.py runserver
```

## Admin dashboard

In a second terminal, run:

```powershell
.venv\Scripts\python.exe manage.py createsuperuser
```

Choose your own username and password, then sign in at http://127.0.0.1:8000/admin/. Manage categories, products, prices, stock, visibility and featured picks. View orders and change their status. Product images use local static paths such as `images/iphone16.png`; put new images in `static/images/` and enter that path in the product editor. This project does not include an image-upload service.

## Try the entire flow

1. Browse the home page or collection. Search by product, brand or category; apply category/sort filters and pagination.
2. Open a product, select a quantity and add it to your bag. Update quantities or remove items.
3. Create a customer account with a strong password. The existing guest bag survives registration/login.
4. Continue to checkout. Enter a sample Indian mobile number and PIN code, plus delivery details.
5. Place a **demo cash-on-delivery order**. The database saves the order and line-item price snapshots, stock decreases and the bag clears.
6. See the order in My orders. Change the status in admin and refresh the customer order page.

There are no shared demo passwords or pre-created users. The ZIP intentionally contains no customer database; migration and `seed_demo` create a fresh local store with 26 products in 5 categories. Re-running `seed_demo` adds missing entries but does not reset your edits or stock.

## What changed from the original

- Replaced individual hard-coded product templates with reusable, database-driven product cards, catalogue and detail pages.
- Rebuilt the interface with responsive green/cream styling, consistent navigation, form feedback, empty states and keyboard focus styles.
- Replaced the plain-text UserAccount login with Django's password hashing, password validation, authentication and sessions.
- Removed embedded database credentials and development secrets from the source. Rotate the old database password if it is still used elsewhere, and replace any previously deployed secret key.
- Replaced client-supplied prices and GET cart mutations with server-priced, CSRF-protected POST actions.
- Added order persistence, customer-only order access, price snapshots, validated addresses and atomic stock updates.
- Added admin management, migrations, repeatable demo data, setup guidance and automated integration tests.
- Reused the original product images. Original `.git` history, obsolete pages and unsafe custom-user migrations are not distributed.

## Project map

- `products/`: Category/Product models, catalogue views, admin, demo-data command.
- `cart/`: session cart, quantity actions and navbar count.
- `users/`: registration; Django handles login/logout and password hashing.
- `orders/`: checkout validation, stock transaction, Order/OrderItem, private order pages, tests and admin.
- `templates/`: shared layout, reusable cards and all storefront pages.
- `static/`: local CSS, JavaScript and original images.
- `shopcart_project/`: environment-aware settings and URL routes.

The browser sends a request to a Django URL/view. The view reads or changes model data, builds template context, and renders HTML. Cart storage uses Django sessions; orders and catalogue records use SQLite. The product JSON endpoint is an additional read API, not a separate frontend framework.

## API

`GET /api/products/?q=phone&category=mobiles&sort=price_low&page=1`

Returns `count`, `page`, `pages`, and `results` (id, name, slug, decimal price string, category, stock). Uses the same filter rules as the storefront. Sort values: `featured`, `price_low`, `price_high`, `name`. Page size: 12. This is a read-only Django JsonResponse API; no DRF dependency is required.

## Checks

```powershell
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py test
.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Integration tests cover search/API rendering, cart quantities, price tampering, CSRF, hashed-password registration, authentication, order ownership, stock rollback, order snapshots and repeated checkout submission.

## Scope and deployment

This is a working local portfolio/demo store, not a live commercial storefront. Product names/images are inherited from the original project; prices, stock and descriptions are illustrative and are not verified merchant specifications. Clothing uses one demo variant without size selection. No real payments, shipments, tax calculation, email sending, refunds, cancellations or password-reset emails are integrated. Delivery is always free in the demo. Cart state is session-based, not synchronized across devices, and logout clears it.

SQLite is intentionally used for simple local setup. For a live site, configure a production database, a real payment/shipping provider, email service, login rate limiting, monitoring, backups and HTTPS. Set OS environment variables `DJANGO_DEBUG=0`, a strong unique `DJANGO_SECRET_KEY`, and `DJANGO_ALLOWED_HOSTS`. `.env.example` is a reference; `.env` files are not auto-loaded. Collect and serve static files via a production server, and run `manage.py check --deploy`. The included development server is for local use only.

This refresh is for a **fresh database**. It does not migrate existing PostgreSQL customers/orders or the old plain-text password table. Keep any old database separately if needed; do not copy it over this one. No existing external database or GitHub repository was modified.

## Updating your GitHub project

Extract to a new folder and test locally first. Copy the updated source into your existing clone (preserving its `.git` folder), review the changes, then commit and push. Do not upload `.venv`, `db.sqlite3`, environment secrets or customer data. The included `.gitignore` excludes these. No GitHub changes have been pushed for you.

## Interview walkthrough

Explain the request flow: URL → view → model/query → template. Demonstrate registration, adding products, checkout and admin status updates. Discuss why prices are loaded from the database, why order items keep price snapshots, how conditional stock updates inside a transaction avoid overselling, and why each order query is scoped to its owner. Only claim features you have run and understand.
