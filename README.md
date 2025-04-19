# Shop Project
This project aims to build a website for small retail business owners to manage online shopping.
(Capstone project for the Tamwood Web Development course)

## Table of Contents
- [Summary](#summary)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Set Up](#set-up)
- [License](#license)
  
## Summary
In this application, master and staff users can register, view, update, and delete products. Customer users can add products to their own carts and place orders.

## Features
- Role-based access (Master, Staff, Customer)
- Masters can change user role
- Product CRUD for Master and Staff
- Cart system for customers
- Order placement and status tracking for signed-in users

## Tech Stack
- Python, Django
- SQLite
- HTML/CSS, Tailwind
- Javascript

## Setup
1. Clone repository
   `git clone https://github.com/harukaarai95/capstone_prj.git`
   `cd shop_prj`
3. Activate a virtual environment
   `python -m venv capstoneVenv`
   Windows: `venv\Scripts\activate`
   Mac: `source venv/bin/activate`
5. Install a required package
   `pip install -r requirements.txt`
7. Run development server
   `py manage.py runserver`
9. Demo account
   - Master
     Email: admin@mail.com
     Password: admin123
   - Staff
     Email: staff@mail.com
     Password: 95123pass
   - Customer
     Email: test@mail.com
     Password: 95123pass

## License
This project is licensed under the MIT License.

