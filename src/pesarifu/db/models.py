import time
from datetime import timedelta
from enum import Enum, auto
from functools import partial
from typing import Any, Optional
from uuid import UUID, uuid4

import sqlalchemy
from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import ARRAY, DECIMAL, JSON, String


# TODO: figure out migration
class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON, float: DECIMAL}

    def __repr__(self) -> str:
        return self._repr(id=self.id)

    # https://stackoverflow.com/a/55749579
    def _repr(self, **fields: dict[str, Any]) -> str:
        field_strings = []
        for key, field in fields.items():
            try:
                if field:
                    field_strings.append(f"{key}={field!r}")
            except sqlalchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f"{key}=DetatchedInstanceError")
        return f"{self.__class__.__name__}({', '.join(field_strings)})"

    def as_dict(self):
        return {
            c.name: str(getattr(self, c.name))
            for c in self.__table__.columns
            if getattr(self, c.name) is not None
        }


class OrgType(Enum):
    BANK = auto()
    TELCO = auto()
    OTHER = auto()


class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(
        String(3), unique=True, comment="ISO 4217 Currency Code"
    )
    name: Mapped[str] = mapped_column(String(50))
    symbols = mapped_column(ARRAY(String(10)))

    def __repr__(self):
        return self._repr(
            id=self.id,
            code=self.code,
            name=self.name,
        )


class UserAccount(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(100), unique=True, comment="Email used to register."
    )
    phone_number: Mapped[Optional[str]] = mapped_column(
        String(30), comment="Email used to contact user or to send alerts to."
    )
    username: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[float] = mapped_column(
        default=time.time
    )  # Unix timestamp
    updated_at: Mapped[float] = mapped_column(
        default=time.time, onupdate=time.time
    )  # Unix timestamp
    active: Mapped[bool] = mapped_column(default=False)
    registered: Mapped[bool] = mapped_column(
        default=False, comment="Whether or not user has signed up"
    )
    extra: Mapped[Optional[dict[str, Any]]] = mapped_column(
        comment="Any extra information we may want to keep as JSON"
    )

    uuid: Mapped[UUID] = mapped_column(
        default=uuid4,
        unique=True,
        comment="Less guessable id to use in application",
    )

    accounts: Mapped[Optional[list["TransactionalAccount"]]] = relationship(
        back_populates="holder"
    )

    def __repr__(self):
        return self._repr(
            id=self.id,
            uuid=self.uuid,
            email=self.email,
            # created_at=datetime.fromtimestamp(int(self.created_at), timezone.utc),
            accounts=self.accounts,
        )


# TODO: define default subscription plans
class SubscriptionPlan(Base):
    __tablename__ = "subscription_plan"
    id: Mapped[int] = mapped_column(primary_key=True)

    duration: Mapped[timedelta] = mapped_column(
        comment="How long does a subscription last"
    )
    name: Mapped[str] = mapped_column(
        default=lambda: uuid4().hex,
        comment="For example basic, pro, enterprise",
    )

    price: Mapped[float]


class Provider(Base):
    __tablename__ = "account_provider"
    __table_args__ = (UniqueConstraint("name", "organization_type"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100),
        comment="Common name of provider e.g Safaricom or Standard Chartered",
    )
    organization_type: Mapped[OrgType] = mapped_column(default=OrgType.TELCO)

    accounts: Mapped[list["TransactionalAccount"]] = relationship(
        back_populates="provider"
    )

    def __repr__(self):
        return self._repr(
            id=self.id,
            name=self.name,
            organization_type=self.organization_type,
        )


# TODO: temporarily add way to keep track of PDFs
class WebReport(Base):
    __tablename__ = "web_report"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[float] = mapped_column(default=time.time)
    expires_after: Mapped[timedelta] = mapped_column(
        default=partial(timedelta, days=7),
        comment="How long a web report should stay live",
    )
    expired: Mapped[bool] = mapped_column(default=False)
    web_url: Mapped[str] = mapped_column(
        String(150), comment="URL for web report", unique=True
    )
    last_visit: Mapped[float] = mapped_column(default=time.time)

    account_id: Mapped[int] = mapped_column(
        ForeignKey("transactional_account.id")
    )
    account: Mapped["TransactionalAccount"] = relationship(
        back_populates="web_report"
    )


class TransactionalAccount(Base):
    __tablename__ = "transactional_account"
    __mapper_args__ = {
        "polymorphic_identity": "transactional_account",
        "polymorphic_on": "type",
    }

    id: Mapped[int] = mapped_column(primary_key=True)
    account_name: Mapped[str] = mapped_column(
        String(500),
        comment="Name associated with this account for example Facebook .inc or John Smith.",
    )
    type: Mapped[str]
    provider_id: Mapped[int] = mapped_column(ForeignKey("account_provider.id"))
    provider: Mapped["Provider"] = relationship(back_populates="accounts")

    holder_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id"), nullable=True
    )
    holder: Mapped["UserAccount"] = relationship(back_populates="accounts")

    web_report: Mapped["WebReport"] = relationship(back_populates="account")
    owned_transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="owner_account",
        foreign_keys="Transaction.owner_account_id",
    )
    participating_transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="participant_account",
        foreign_keys="Transaction.participant_account_id",
    )
    balance: Mapped[Optional[float]] = mapped_column(
        comment="Balance of account at last_checked"
    )
    last_checked: Mapped[Optional[float]] = mapped_column(onupdate=time.time)

    def __repr__(self):
        return self._repr(
            id=self.id,
            account_name=self.account_name,
            holder=self.holder,
            provider=self.provider_id,
        )


class BankAccount(TransactionalAccount):
    __tablename__ = "bank_account"

    __mapper_args__ = {
        "polymorphic_identity": "bank_account",
    }
    __table_args__ = (UniqueConstraint("identifier", "account_type"),)

    account_id: Mapped[int] = mapped_column(
        ForeignKey("transactional_account.id"), primary_key=True
    )
    account_type: Mapped[str] = mapped_column(
        String(30), comment="Type of the account e.g Hifadhi Current Account"
    )
    # TODO: figure out whether adding BIC/SWIFT code is necessary
    identifier: Mapped[str] = mapped_column(String(100))

    def __repr__(self):
        return self._repr(
            account_id=self.account_id,
            identifier=self.identifier,
        )


# TODO: figure out if refactor of TransactionalAccount necessary
class ProviderAccount(TransactionalAccount):
    __tablename__ = "provider_account"

    account_id: Mapped[int] = mapped_column(
        ForeignKey("transactional_account.id"), primary_key=True
    )
    __mapper_args__ = {
        "polymorphic_identity": "provider_account",
    }


class SafaricomPaybillAccount(TransactionalAccount):
    __tablename__ = "safaricom_paybill_account"

    __mapper_args__ = {
        "polymorphic_identity": "safaricom_paybill_account",
    }

    __table_args__ = (UniqueConstraint("paybill_number", "account_number"),)

    account_id: Mapped[int] = mapped_column(
        ForeignKey("transactional_account.id"), primary_key=True
    )
    paybill_number: Mapped[str] = mapped_column(String(10), unique=True)
    account_number: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        comment="May not always be present since sometimes organizations use them to partition accounts",
    )

    def __repr__(self):
        return self._repr(
            account_id=self.account_id,
            paybill_number=self.paybill_number,
            account_number=self.account_number,
        )


class SafaricomBuygoodsAccount(TransactionalAccount):
    __tablename__ = "safaricom_buygoods_account"

    __mapper_args__ = {
        "polymorphic_identity": "safaricom_buygoods_account",
    }

    account_id: Mapped[int] = mapped_column(
        ForeignKey("transactional_account.id"), primary_key=True
    )
    buygoods_number: Mapped[str] = mapped_column(String(10), unique=True)

    def __repr__(self):
        return self._repr(
            account_id=self.account_id,
            buygoods_number=self.buygoods_number,
        )


# FIXME: add unique constraint on account_name and maybe_number
class MobileMoneyAccount(TransactionalAccount):
    __tablename__ = "mobile_money_account"

    __mapper_args__ = {
        "polymorphic_identity": "mobile_money_account",
    }

    account_id: Mapped[int] = mapped_column(
        ForeignKey("transactional_account.id"), primary_key=True
    )
    # TODO: add trigger to set phone_number if maybe_number not obfuscated
    maybe_number: Mapped[str] = mapped_column(
        String(30),
        comment="May be obfuscated. Use phone_number for usable number",
    )
    phone_number: Mapped[Optional[str]] = mapped_column(
        String(30), unique=True
    )

    def __repr__(self):
        return self._repr(
            account_id=self.account_id,
            maybe_number=self.maybe_number,
            phone_number=self.phone_number,
        )


class Transaction(Base):
    __tablename__ = "transaction"

    __table_args__ = (
        UniqueConstraint(
            "amount",
            "initiated_at",
            "owner_account_id",
            "participant_account_id",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float]
    initiated_at: Mapped[float] = mapped_column(
        comment="When did this transaction happen"
    )
    owner_account_id: Mapped[int] = mapped_column(
        ForeignKey("transactional_account.id")
    )
    owner_account: Mapped["TransactionalAccount"] = relationship(
        back_populates="owned_transactions", foreign_keys=[owner_account_id]
    )
    participant_account_id: Mapped[int] = mapped_column(
        ForeignKey("transactional_account.id")
    )
    participant_account: Mapped["TransactionalAccount"] = relationship(
        back_populates="participating_transactions",
        foreign_keys=[participant_account_id],
    )
    # currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"))
    purpose: Mapped[Optional[str]]
    transaction_reference: Mapped[Optional[str]] = mapped_column(
        String(50), comment="Reference given along with transaction"
    )
    original_detail: Mapped[Optional[str]] = mapped_column(
        String(500),
        comment="Original text that was part of transaction message.",
    )
    extra: Mapped[Optional[dict[str, Any]]] = mapped_column(
        comment="Any extra information we may want to keep as JSON"
    )

    def __repr__(self):
        return self._repr(
            id=self.id,
            amount=self.amount,
            initiated_at=self.initiated_at,
            transaction_reference=self.transaction_reference,
        )


class IndividualProfile(Base):
    __tablename__ = "individual_profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    phone_number: Mapped[Optional[str]] = mapped_column(String(30))
    social_links = mapped_column(ARRAY(String(100)))

    def __repr__(self):
        return self._repr(
            id=self.id,
            email=self.email,
            name=f"{self.first_name} {self.last_name}",
        )


class CompanyProfile(Base):
    __tablename__ = "company_profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    email: Mapped[Optional[str]] = mapped_column(String(100))
    website: Mapped[Optional[str]] = mapped_column(String(100))
    address: Mapped[Optional[str]] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    tags = mapped_column(ARRAY(String(20)))

    def __repr__(self):
        return self._repr(
            id=self.id,
            name=self.name,
            address=self.address,
            website=self.website,
        )
