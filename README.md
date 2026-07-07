# Inventory & Order Management System

A full-stack web application to manage a product catalog, track stock levels,
flag low-stock items automatically, and place orders that update inventory
in real time — built with **Flask** and **SQLite**.

## Features

- **Product Catalog (CRUD):** Add, edit, view, and delete products.
- **Stock Tracking:** Each product has a quantity and a configurable
  low-stock threshold. Products at or below the threshold are flagged
  as "Low Stock" on the dashboard.
- **Order Placement:** Place orders against a product. The system
  validates stock availability before confirming, and automatically
  decrements inventory on a successful order.
- **Order History:** View all past orders with product name, quantity,
  date, and status.

## Project Structure

```
inventory-management-system/
├── app.py                  # Flask routes / application logic
├── database.py              # SQLite connection, schema, seed data
├── templates/
│   ├── base.html             # shared layout + styling
│   ├── index.html            # product dashboard
│   ├── add_product.html
│   ├── edit_product.html
│   ├── place_order.html
│   └── orders.html
├── requirements.txt
└── README.md
```

## Database Schema

**products**: id, name, category, price, quantity, low_stock_threshold

**orders**: id, product_id (FK), quantity_ordered, order_date, status



## Tech Stack

Python, Flask, SQLite, Jinja2 templates, HTML/CSS


