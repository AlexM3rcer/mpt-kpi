import os
import enum
from pathlib import Path
from config import Config
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db


class Position(db.Model):
    __tablename__ = 'position'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    score_threshold = db.Column(db.Integer, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
    phone_number = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    position = db.relationship('Position', backref=db.backref('users', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Criterion(db.Model):
    __tablename__ = 'criterion'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(511), nullable=False)
    mark_from = db.Column(db.Integer, nullable=False, default=0)
    mark_to = db.Column(db.Integer, nullable=False, default=10)


class CertificateStatusEnum(enum.Enum):
    approved = 'approved'
    rejected = 'rejected'
    sent = 'sent'


class CertificateMark(db.Model):
    __tablename__ = 'certificate_marks'

    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.String(511), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    certificate_id = db.Column(db.Integer, db.ForeignKey('certificate.id'), nullable=False)
    # certificate = db.relationship('Certificate', back_populates='marks')

    @property
    def status(self) -> CertificateStatusEnum:
        if self.mark is not None:
            return CertificateStatusEnum.approved
        if self.comment is not None:
            return CertificateStatusEnum.rejected
        raise ValueError(__name__, ' unexpected status.')


class CertificateMediaFiles(db.Model):
    __tablename__ = 'certificate_media_files'

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('media_file.id'), nullable=False)
    certificate_id = db.Column(db.Integer, db.ForeignKey('certificate.id'), nullable=False)

    # certificate_id = db.relationship('Certificate', back_populates='files')
    # file_id = db.relationship('MediaFile', back_populates='certificates')


class MediaFile(db.Model):
    __tablename__ = 'media_file'

    id = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.String(255), nullable=False, unique=True)
    original_name = db.Column(db.String(255), nullable=True)
    preview_id = db.Column(db.Integer, db.ForeignKey('media_file.id'), nullable=True)

    preview = db.relationship('MediaFile', remote_side=id, backref='previewed')
    # certificates = db.relationship('Certificate', secondary=CertificateMediaFiles.__table__, back_populates='files')

    # def __del__(self):
    #     os.remove(Path(Config.MEDIA_ROOT, self.src))
    #     return super().__del__()

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'url': self.url,
            'original_name': self.original_name,
            'preview_url': self.preview_url,
        }
 
    @property
    def url(self) -> str:
        return str(Path('/', Config.MEDIA_URL, self.src))

    @property
    def preview_url(self) -> str | None:
        return None


class Certificate(db.Model):
    __tablename__ = 'certificate'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    criterion_id = db.Column(db.Integer, db.ForeignKey('criterion.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # sender = db.relationship('User', back_populates='certificates')
    # criterion = db.relationship('Criterion', back_populates='certificates')
    # marks = db.relationship('CertificateMark', back_populates='certificate')
    # files = db.relationship('MediaFile', secondary=CertificateMediaFiles.__table__, back_populates='certificates')

    @property
    def preview_url(self) -> str | None:
        files_with_preview = MediaFile.query.filter(MediaFile.preview.isnot(None))
        return files_with_preview[0].src if files_with_preview else None

    @property
    def sorted_marks(self) -> list[CertificateMark]:
        return CertificateMark.query.order_by(CertificateMark.created_at.desc()).all()

    @property
    def latest_mark(self) -> CertificateMark | None:
        return self.sorted_marks[0] if self.sorted_marks else None

    @property
    def status(self) -> CertificateStatusEnum:
        return self.latest_mark.status if self.latest_mark else CertificateStatusEnum.sent
