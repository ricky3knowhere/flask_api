from app import db
from app.model.dosen import Dosen


class Mahasiswa(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nim = db.Column(db.String(30), nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(13), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    first_dosen = db.Column(db.BigInteger, db.ForeignKey(Dosen.id, ondelete="CASCADE"))
    second_dosen = db.Column(db.BigInteger, db.ForeignKey(Dosen.id, ondelete="CASCADE"))

    def __repr__(self):
        return f"<Mahasiswa {self.full_name}>"
