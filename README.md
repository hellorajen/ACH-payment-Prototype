# ACH-payment-Prototype
ACH payment Prototype app
ACH vs. SWIFT: Understanding the Differences
No, ACH (Automated Clearing House) does not use the SWIFT protocol. They are completely separate payment systems with different purposes, technologies, and operational networks.

Key Differences Between ACH and SWIFT
Feature	ACH Network	SWIFT Network
Primary Use	Domestic transfers within one country	International transfers between countries
Geographic Scope	Single country (e.g., U.S. ACH)	Global (200+ countries)
Speed	1-3 business days	1-5 business days
Message Protocol	NACHA file formats	SWIFT MT/MX messages (ISO 20022)
Cost	Low (
0.20
−
0.20−1.50 per transaction)	Higher (
15
−
15−50 per transaction)
Participants	Banks within the same country	Banks worldwide
Regulation	National (e.g., NACHA in U.S.)	International (SWIFT coop)
Technical Differences
ACH Protocol
Uses standardized file formats (NACHA in the U.S.)

Batch processing system

Typically communicates through direct bank connections or intermediaries like the Federal Reserve

No universal messaging protocol - each country has its own ACH standards

SWIFT Protocol
Uses standardized message types (MT for legacy, MX/ISO 20022 for modern)

Real-time message exchange (though settlement may take time)

Global network with standardized identifiers (BIC/SWIFT codes)

Financial messaging system (doesn't actually move money - instructs transfers)

When Each System Is Used
Use ACH when:

Paying bills domestically

Direct deposit of payroll

Transferring money between your own accounts at different banks

Business-to-business payments within the same country

Use SWIFT when:

Sending money internationally

Making large corporate cross-border payments

Transactions requiring currency exchange

When the recipient's bank isn't part of your domestic clearing system

Hybrid Cases
Some scenarios combine both systems:

International ACH Transactions (IAT): Uses ACH network but with additional SWIFT-like information for cross-border compliance

Some banks may use SWIFT messages to communicate between their own international branches while using local ACH for settlement

------------------
Option 1: Run the scripts directly without execute permission
bash Create_Django_project_and_app.sh
bash Init_Django_proj.sh

# to clear cache - bash
python manage.py shell -c "from django.template.loaders.cached import Loader; Loader.reset()"

# to bypass credential check do following
python manage.py createsuperuser --username=dev --email=dev@example.com --noinput
echo "from django.contrib.auth.models import User; user=User.objects.get(username='dev'); user.set_password('dev'); user.save()" | python manage.py shell

# to reset your database:
# Delete the database file (SQLite only)
rm db.sqlite3

# Then recreate everything
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# run the app again 
python manage.py runserver

# to query audit logs -Audit logs are critical for security, compliance (e.g., PCI-DSS, SOX)

