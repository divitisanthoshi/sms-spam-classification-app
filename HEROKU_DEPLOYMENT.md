# Heroku Deployment Guide for SMS Spam Classifier

This guide explains how to deploy your Flask SMS spam classifier app on Heroku with PostgreSQL for scalable and accessible real-time processing.

## Prerequisites

- Heroku CLI installed: https://devcenter.heroku.com/articles/heroku-cli
- Git installed: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
- A Heroku account: https://signup.heroku.com/

## Steps

### 1. Login to Heroku CLI

```bash
heroku login
```

### 2. Create a new Heroku app

```bash
heroku create your-app-name
```

Replace `your-app-name` with a unique name.

### 3. Add PostgreSQL add-on

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

This provisions a free PostgreSQL database.

### 4. Verify DATABASE_URL environment variable

Heroku automatically sets the `DATABASE_URL` environment variable to point to the PostgreSQL database.

You can check it with:

```bash
heroku config:get DATABASE_URL
```

### 5. Prepare your app for deployment

- Ensure your `Procfile` contains:

```
web: gunicorn app:app
```

- Ensure `requirements.txt` includes all dependencies, including `psycopg2-binary`.

### 6. Initialize Git repository (if not already)

```bash
git init
git add .
git commit -m "Prepare app for Heroku deployment"
```

### 7. Add Heroku remote (if not added by `heroku create`)

```bash
heroku git:remote -a your-app-name
```

### 8. Push code to Heroku

```bash
git push heroku master
```

or if your default branch is main:

```bash
git push heroku main
```

### 9. Scale the web dyno

```bash
heroku ps:scale web=1
```

### 10. Open the app in browser

```bash
heroku open
```

### 11. View logs (optional)

```bash
heroku logs --tail
```

## Notes

- Your app will use PostgreSQL in production via the `DATABASE_URL` environment variable.
- The app runs with gunicorn as specified in the Procfile.
- For real-time SMS processing, configure your SMS gateway (e.g., Twilio) to send webhooks to your Heroku app URL.

---

This completes the deployment setup for your SMS spam classifier app on Heroku.



PS C:\Users\santh\OneDrive\Desktop\stuff\All In One\Projects\Spam Classification> heroku addons:create heroku-postgresql --app sms-spam-classification
 »   Warning: heroku update available from 7.69.1 to 10.10.1.
Creating heroku-postgresql on ⬢ sms-spam-classification... $5/month
Database should be available soon
postgresql-triangular-03404 is being created in the background. The app will restart when complete...
Use heroku addons:info postgresql-triangular-03404 to check creation progress
Use heroku addons:docs heroku-postgresql to view documentation



=== postgresql-triangular-03404

Attachments:  sms-spam-classification::DATABASE
Installed at: Sat Jun 21 2025 22:51:38 GMT+0530 (India Standard Time)
Max Price:    $5/month
Owning app:   sms-spam-classification
Plan:         heroku-postgresql:essential-0
Price:        ~$0.007/hour
State:        created


PS C:\Users\santh\OneDrive\Desktop\stuff\All In One\Projects\Spam Classification> heroku config:get DATABASE_URL --app sms-spam-classification
postgres://u4jt6li6hbd2kc:p74d4f89064dc153ecb81e0724d3a86d5fc35189d01ac2d76437874de640119bc@c7itisjfjj8ril.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dcp7ros53uc225
PS C:\Users\santh\OneDrive\Desktop\stuff\All In One\Projects\Spam Classification>  