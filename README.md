# Sample Vk Web Application

## Requirements

Python 3 + venv, Sqlite, NGrok


## Usage

1. Register application here:
https://vk.com/editapp?act=create

2. Specify API_SECRET_KEY (see here https://vk.com/editapp?id=YourAppID&section=options) in settings/local.py

3. Run application server:
```bash
make initdev migrate run
ngrok http 8000
```

4. Set up IFrame address here:
https://vk.com/editapp?id=YourAppID&section=options

5. Set up payment callback address here:
https://vk.com/editapp?id=YourAppID&section=payments

6. Go to application page
https://vk.com/appYourAppID


## Some tips

Admin page is available at http://localhost:8000/admin.
You can there create items and see orders and notifications.

To create superuser for login in admin:
```bash
venv/bin/python manage.py createsuperuser
```

To load some initial data:
```bash
venv/bin/python manage.py loaddata contrib/data.json
```

To overwrite some settings use app/settings/local.py.
