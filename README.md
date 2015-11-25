# Proxmate

## Configuration

- `apt-get install ipython git python-setuptools python-pip python-mysqldb python-dev memcached python-memcache`
- `apt-get install apache2 phpmyadmin mysql-server nginx uwsgi-plugin-python libjpeg8-dev zlib1g-dev`

___

- `pip install -r requirements.txt`

___

- `python manage.py migrate`
- `python manage.py runserver`

___

## Stripe ( API Keys ) Configuration

- `pip install --index-url https://code.stripe.com --upgrade stripe`

- when adding new test / live API keys, add them in `settings.py`, `index.html` and run the following commands in console:

1. `export STRIPE_SECRET_KEY=sk_live_or_test_secret_key`
2. `export STRIPE_PUBLISHABLE_KEY=pk_live_or_test_publishable_key`

