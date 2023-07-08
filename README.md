# warwick-asoc
Web application for Warwick Asian Society built with Flask.

## About

### Software Architecture

This Flask application makes use of the **MVC** architectural pattern:
- Model (database): PostgreSQL (using SQLAlchemy as an ORM)
- View (frontend): HTML, CSS, JavaScript
- Controller (backend): Python

### External Resources

- [GitHub](https://github.com/warwick-asoc/warwick-asoc) - version control
- [Black](https://black.readthedocs.io/en/stable/) - PEP 8 compliant opinionated formatter
- [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/) - specific UI components (e.g. navbar)
- [Stripe](https://dashboard.stripe.com/dashboard) - payment handling
- [Zoho mail](https://www.zoho.com/mail/) - email service provider
- [Heroku](https://dashboard.heroku.com/apps/warwick-asoc) - hosting
- [Cloudflare](https://dash.cloudflare.com/604c65132a8f8ad4e86863c4c1042053/warwick-asoc.co.uk) - provides HTTPS support (required for Stripe)
- [Google Domains](https://domains.google.com/) - domain name provider

### Scripts

This repository contains several Python scripts used to automate recurring processes:

- [`send_data.py`](send_data.py): sends a message to the ASOC Tech WhatsApp groupchat with the numbers of current members and account holders
- [`email_newsletter.py`](email_newsletter.py): sends an email to the newsletter editor with a CSV file containing the email addresses of all ASOC members

---

## How Tos

### Local Set Up and Running Instructions

Note: steps 1-2 are only required to be executed when running the application for the first time

1. In a Terminal window, execute the following from within the `warwick-asoc/` directory:

```
python3 -m venv .venv
source .venv/bin/activate
```

2. Install the required Python modules into the virtual environment:

```
pip install -r requirements.txt
```

- Note: the `requirements.txt` file can be generated/updated by executing `pip freeze > requirements.txt` from within the virtual environment

3. Export the following environment variables via the Terminal:

```
export FLASK_DEBUG=True
export FLASK_ENV=development
export SECRET_KEY=e617f901bb846ad01eb6aa446b1c203f
export DATABASE_URL=sqlite:///asoc.sqlite
export MAIL_PASSWORD=
export STRIPE_SECRET_KEY= 
export STRIPE_PUBLISHABLE_KEY= 
export STRIPE_ENDPOINT_SECRET= 
```

- Notes:
  - The Stripe API keys must be provided to enable payment functionality
  - In development, reloading the server will reset the database by default. To prevent this, execute the following: `export RESET_DB=false`
  - In production, the environment variables can be updated in Heroku via the [settings](https://dashboard.heroku.com/apps/warwick-asoc/settings) page

4. Change configuration settings:
- In `app/__init__.py`, change `ProductionConfig` to `DevelopmentConfig`
- Note: this must be **reverted before deployment**

5. Run the application:
```
flask run
```
- Note: if the port is already in use (e.g. `OSError: [Errno 48] Address already in use`), use the following command instead:
```
flask run --host=0.0.0.0 --port=80
```

### GitHub Development Workflow

- Make a new branch from `main`
    - **Do not** edit `main` branch directly
    - Naming convention: `name/feature-being-worked-on` (e.g. `neil/add-events-page`)
- Make edits from new branch
- Make Pull Request (PR) when code is ready to be reviewed
    - Use the black formatter before submitting a PR (command: `black .`)
    - Try to keep PRs short (< 100 new lines of code)
    - If necessary, make multiple PRs for easy review
- Make necessary changes suggested by reviewer
- Merge PR and delete branch

### Hosting and Deployment

- The application is hosted by Heroku and is integrated with the GitHub repository
- Hosting with Heroku requires a [Procfile](Procfile)
- The database the Heroku Postgres Mini add-on, which currently costs $5.00 per month (circumvented by enrolling in the [GitHub Student Developer Pack](https://www.heroku.com/github-students))
- New versions of the application are **deployed automatically** by Heroku when changes are pushed to the GitHub repository's `main` branch
  - The maximum allowed slug size (after compression) is 500 MB
  - The configuration settings (specified in `app/__init__.py`) in the `main` branch must always be set to `ProductionConfig` 

### Interacting with the Production Database

The production database served by Heroku can be interacted with via [Heroku dataclips](https://data.heroku.com/dataclips) or the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli). While the former supports read-only transactions with the ability to export results as a CSV file, the latter can be used to perform all manner of transactions.

Common transaction examples (executed in a Terminal window from any directory):
```
# Select all users
heroku pg:psql -a warwick-asoc -c "SELECT * FROM users;"

# Update membership status of specific user
heroku pg:psql -a warwick-asoc -c "UPDATE users SET membership='Student', student_id=2111111 WHERE email='testing@gmail.com';"

# Delete unverified users
heroku pg:psql -a warwick-asoc -c "DELETE FROM users WHERE NOT verified AND date_joined < date_trunc('day', now() - interval '0.5 month');"

# Add new column to table
heroku pg:psql -a warwick-asoc -c "ALTER TABLE users ADD member_since DATE;"
```

### Database Backups

The production database is backed up daily at midnight, using [Heroku PGBackups](https://devcenter.heroku.com/articles/heroku-postgres-backups).

Common commands (executed in a Terminal window from any directory):
```
# View recent backups
heroku pg:backups --app warwick-asoc

# View backup schedule
heroku pg:backups:schedules --app warwick-asoc

# Create manual backup
heroku pg:backups:capture --app warwick-asoc
```

### Managing Payments
- Payments are handled by [Stripe Checkout](https://stripe.com/docs/payments/checkout)
- Details of all payments, as well as the ability to issue refunds, are available on the [Stripe Dashboard](https://dashboard.stripe.com/dashboard)
- See this [tutorial](https://testdriven.io/blog/flask-stripe-tutorial/) for integrating Stripe with Flask
- Note: Stripe deducts a **fee** for every transaction (see pricing details [here](https://stripe.com/en-gb/pricing))
