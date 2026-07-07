"""
Inventory & Order Management System
------------------------------------
A simple Flask + SQLite web app to manage a product catalog, track stock
levels, flag low-stock items, and place orders that automatically reduce
inventory.

Author: Sinjini Som
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_connection, init_db, seed_if_empty

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # fine for a local demo project


@app.before_request
def setup():
    init_db()
    seed_if_empty()


@app.route("/")
def index():
    with get_connection() as conn:
        products = conn.execute("SELECT * FROM products ORDER BY id").fetchall()
    return render_template("index.html", products=products)


@app.route("/product/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"].strip()
        category = request.form["category"].strip()
        price = float(request.form["price"])
        quantity = int(request.form["quantity"])
        threshold = int(request.form.get("low_stock_threshold") or 5)

        with get_connection() as conn:
            conn.execute(
                "INSERT INTO products (name, category, price, quantity, low_stock_threshold) "
                "VALUES (?, ?, ?, ?, ?)",
                (name, category, price, quantity, threshold),
            )
        flash(f"Product '{name}' added successfully.", "success")
        return redirect(url_for("index"))

    return render_template("add_product.html")


@app.route("/product/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    with get_connection() as conn:
        product = conn.execute(
            "SELECT * FROM products WHERE id = ?", (product_id,)
        ).fetchone()

        if product is None:
            flash("Product not found.", "error")
            return redirect(url_for("index"))

        if request.method == "POST":
            name = request.form["name"].strip()
            category = request.form["category"].strip()
            price = float(request.form["price"])
            quantity = int(request.form["quantity"])
            threshold = int(request.form.get("low_stock_threshold") or 5)

            conn.execute(
                "UPDATE products SET name=?, category=?, price=?, quantity=?, "
                "low_stock_threshold=? WHERE id=?",
                (name, category, price, quantity, threshold, product_id),
            )
            flash(f"Product '{name}' updated.", "success")
            return redirect(url_for("index"))

    return render_template("edit_product.html", product=product)


@app.route("/product/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    flash("Product deleted.", "success")
    return redirect(url_for("index"))


@app.route("/order/place", methods=["GET", "POST"])
def place_order():
    with get_connection() as conn:
        products = conn.execute("SELECT * FROM products ORDER BY name").fetchall()

        if request.method == "POST":
            product_id = int(request.form["product_id"])
            quantity_ordered = int(request.form["quantity_ordered"])

            product = conn.execute(
                "SELECT * FROM products WHERE id = ?", (product_id,)
            ).fetchone()

            if product is None:
                flash("Product not found.", "error")
            elif quantity_ordered <= 0:
                flash("Order quantity must be greater than zero.", "error")
            elif product["quantity"] < quantity_ordered:
                flash(
                    f"Cannot place order: only {product['quantity']} units of "
                    f"'{product['name']}' in stock.",
                    "error",
                )
            else:
                conn.execute(
                    "INSERT INTO orders (product_id, quantity_ordered, status) "
                    "VALUES (?, ?, 'PLACED')",
                    (product_id, quantity_ordered),
                )
                conn.execute(
                    "UPDATE products SET quantity = quantity - ? WHERE id = ?",
                    (quantity_ordered, product_id),
                )
                flash(
                    f"Order placed: {quantity_ordered} x '{product['name']}'.",
                    "success",
                )
            return redirect(url_for("place_order"))

    return render_template("place_order.html", products=products)


@app.route("/orders")
def view_orders():
    with get_connection() as conn:
        orders = conn.execute("""
            SELECT orders.id, products.name AS product_name, orders.quantity_ordered,
                   orders.order_date, orders.status
            FROM orders
            JOIN products ON orders.product_id = products.id
            ORDER BY orders.id DESC
        """).fetchall()
    return render_template("orders.html", orders=orders)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
