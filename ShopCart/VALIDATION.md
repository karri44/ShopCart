# Validation results

Test environment: Python 3.12, Django 5.2.18, SQLite and headless Chromium.

- `python manage.py test`: 10 integration tests passed.
- `python manage.py check`: no issues.
- `python manage.py makemigrations --check --dry-run`: no model drift.
- Rendered 38 storefront/auth/category/product pages with HTTP 200; all referenced product images resolve.
- Real browser flow: browse, filter, open product, add to bag, register, checkout, place order, view confirmation: passed.
- Mobile/tablet horizontal overflow checks at 390px and 768px: passed for home, catalogue, product, cart, orders and account route.
- No JavaScript exceptions during the browser flow.
- Desktop and mobile home screenshots visually inspected.

The Windows launcher has not been executed on a Windows machine in this Linux environment. Online payment and real delivery are not implemented. Test users, orders, sessions and the local database are excluded from this ZIP.
