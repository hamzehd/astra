**Get Started with Astra!**
==========================

To begin your journey with Astra, follow these simple steps:

### Step 1: Install Dependencies

Run the following command to install the required packages:
`pip install -r requirements/common.txt within your virtual environment`


### Step 2: Setup your database

Run the following command to setup your sqlite database:
`python manage.py migrate`


### Step 3: Setup your admin user

Run the following command to create your admin user:
`python manage.py createsuperuser`


### Step 4: Test the application

Run the command and then Navigate to the below address on your device, unless specified otherwise in the runserver
`python manage.py runserver`
Navigate to `localhost:8000`