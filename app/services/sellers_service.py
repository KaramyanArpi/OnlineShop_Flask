from app.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    InvalidInputError
)

from app.db import get_db

class SellerService:
    @staticmethod
    def register(name, rating):
        if not name or not rating:
            raise InvalidInputError("name", "rating")

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM sellers WHERE name = ?", (name, ))
        candidate = cursor.fetchone()

        if candidate:
            raise AlreadyExistsError("name", name)

        cursor.execute(
            "INSERT INTO sellers (name, rating) VALUES (?, ?)",
            (name, rating)
        )

        cursor.execute("SELECT * FROM sellers WHERE name = ?", (name, ))
        seller = cursor.fetchone()

        db.commit()
        db.close()

        return dict(seller)

    @staticmethod
    def update_name(seller_id, new_name):

        if not seller_id or not new_name:
            raise InvalidInputError("seller_id", "new_name")

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM sellers WHERE id = ?", (seller_id, ))
        candidate = cursor.fetchone()

        if not candidate:
            raise NotFoundError("Seller", "id", seller_id)

        cursor.execute(
            "UPDATE sellers SET name = ? WHERE id = ?",
            (new_name, seller_id)
        )

        cursor.execute("SELECT * FROM sellers WHERE id = ?", (seller_id, ))
        updated_seller = cursor.fetchone()

        db.commit()
        db.close()

        return dict(updated_seller)