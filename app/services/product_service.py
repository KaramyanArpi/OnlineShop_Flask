from app.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    InvalidInputError
)
from app.db import get_db


class ProductService:

    @staticmethod
    def register(title, price, sellers):
        if not title or not price or not sellers:
            raise InvalidInputError("sellers, title", "price")

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM products WHERE title = ?", (title, ))
        candidate = cursor.fetchone()

        if candidate:
            raise AlreadyExistsError("title", title)

        cursor.execute(
            "INSERT INTO products (title, price) VALUES (?, ?)",
            (title, price)
        )

        cursor.execute("SELECT * FROM products WHERE title = ?", (title, ))
        product = dict(cursor.fetchone())

        print(product)

        for seller_id in sellers:
            print(seller_id)
            cursor.execute("INSERT INTO seller_products (product_id, seller_id) VALUES (?, ?)", (product["id"], seller_id))

        db.commit()
        db.close()

        return {
            **product,
            "sellers": sellers
        }

    @staticmethod
    def update_product_title(product_id, new_title):
        if not product_id or not new_title:
            raise InvalidInputError("product_id", "new_title")

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id, ))
        candidate = cursor.fetchone()

        if not candidate:
            raise NotFoundError("Product", "id", product_id)

        cursor.execute(
            "UPDATE products SET title = ? WHERE id = ?",
            (new_title, product_id)
        )

        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id, ))
        updated_product = cursor.fetchone()

        db.commit()
        db.close()

        return dict(updated_product)


