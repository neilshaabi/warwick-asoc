# warwick-asoc
Web application for Warwick Asian Society built with Flask, viewable at www.warwick-asoc.co.uk.

## Software Architecture

This application makes use of the **MVC** architectural pattern:
- Model: Flask-SQLAlchemy (database)
- View: HTML, CSS, JavaScript (frontend)
- Controller: Flask/Python (backend)

## External Services

- Bootstrap: specific UI components (e.g. navbar)
- Stripe: payment handling
- Zoho mail - email service provider
- Heroku - hosting ([details](https://dashboard.heroku.com/apps/warwick-asoc))
- Cloudflare - provides HTTPS support (required for Stripe)
- Google Domains - domain name provider

## GitHub Development Workflow

- Make new branch
    - **Do not** edit main branch directly
    - Naming convention: name/feature-being-worked-on (e.g. neil/add-events-page)
- Make Pull Request (PR) when code is ready to be reviewed
    - Try to keep PRs short (< 100 new lines of code) - if necessary, make multiple PRs for easy review
- Make necessary changes suggested by reviewer
- Merge PR and delete branch after approval
- Note: new version will be **deployed automatically** by Heroku when changes are pushed to main

## Local Set Up and Running Instructions

1. In a Terminal window, execute the following from within the `warwick-asoc/` directory:

```
python3 -m venv .venv
source .venv/bin/activate
```

2. Change configuration settings:
- In `app/__init__.py`, change `ProductionConfig` to `DevelopmentConfig`
- Note: this must be **reverted before deployment**

3. Export the following environment variables via the Terminal:

```
export FLASK_DEBUG=True
export SECRET_KEY=e617f901bb846ad01eb6aa446b1c203f
export DATABASE_URL= 
export MAIL_PASSWORD=
export STRIPE_SECRET_KEY= 
export STRIPE_PUBLISHABLE_KEY= 
export STRIPE_ENDPOINT_SECRET= 
```
- Notes:
  - The Zoho mail account password for no-reply@warwick-asoc.co.uk must be provided to enable mail functionality
  - The Stripe API keys must be provided to enable payment functionality
  - In developmnent, the database will be reset by default. To prevent this, execute: `export RESET_DB=false`
  - In production, the environment variables are retrieved by Heroku via the [settings](https://dashboard.heroku.com/apps/warwick-asoc/settings) page

4. Run the application:
```
flask run
```
- Note: if the port is already in use, use the following command instead:
```
flask run --host=0.0.0.0 --port=80
```

## Interacting with the Production Database

The production database served by Heroku can be interacted with via [Heroku dataclips](https://data.heroku.com/dataclips) or the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli). While the former supports read-only transactions with the ability to export results as a CSV file, the latter can be used to perform all manner of transactions.

Common transactions (executed in a Terminal window from any directory):
- Select all users: `heroku pg:psql -a warwick-asoc -c "SELECT * FROM users;"`
- Update membership status of specific user: `heroku pg:psql -a warwick-asoc -c "UPDATE users SET membership='Student', student_id=2107085 WHERE email='testing@gmail.com';"`
- Delete unverified users: `heroku pg:psql -a warwick-asoc -c "DELETE FROM users WHERE NOT verified AND date_joined < date_trunc('day', now() - interval '0.5 month');"`


### Database Backups

The production database is backed up daily at midnight, using [Heroku PGBackups](https://devcenter.heroku.com/articles/heroku-postgres-backups).
- View recent backups: `heroku pg:backups --app warwick-asoc`
- View backup schedule: `heroku pg:backups:schedules --app warwick-asoc`
- Create manual backup: `heroku pg:backups:capture --app warwick-asoc`
