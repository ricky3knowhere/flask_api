from app import db


class Picture(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    pathname = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Picture {self.name}"
