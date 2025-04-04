from sqlalchemy import Integer, String, Boolean, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.api.models.Base import Base
from sqlalchemy_utils import EmailType, PasswordType
from typing import List, Optional, Dict


class User(Base):
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(
        type_=EmailType,
        unique=True,
        index=True,
    )
    password: Mapped[bytes] = mapped_column(nullable=True)
    token_verified: Mapped[str] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_confirm_to_support: Mapped[bool] = mapped_column(default=False)
    session_id: Mapped[str] = mapped_column(nullable=True, index=True)


USER_COLUMNS = User.__table__.columns.keys()
