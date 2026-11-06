from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime, date
import os

database_url = os.getenv("DATABASE_PATH", "sqlite:///outputs/databases/novabank_digital_checking_savings.db")
engine = create_engine("sqlite:////mnt/genming/training-eight-paired-resampling-20261106/seed-303/cases/banking_6_2/before/final.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(
    title="NovaBank Digital Checking & Savings API",
    description="Simplified NovaBank backend for a single demo user (user_id=1).",
    version="1.0.0",
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(Text, nullable=False, unique=True)
    email = Column(Text, nullable=False, unique=True)
    full_name = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    legal_name = Column(Text, nullable=False)
    date_of_birth = Column(Text, nullable=False)
    ssn_last4 = Column(Text, nullable=False)
    address_line1 = Column(Text, nullable=False)
    address_line2 = Column(Text)
    city = Column(Text, nullable=False)
    state = Column(Text, nullable=False)
    postal_code = Column(Text, nullable=False)
    country = Column(Text, nullable=False)
    mobile_number = Column(Text, nullable=False)
    kyc_status = Column(Text, nullable=False)
    kyc_last_reviewed_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    account_number = Column(Text, nullable=False, unique=True)
    account_type = Column(Text, nullable=False)
    currency = Column(Text, nullable=False)
    current_balance = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    is_primary = Column(Integer, nullable=False)
    status = Column(Text, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    card_type = Column(Text, nullable=False)
    last4 = Column(Text, nullable=False)
    network = Column(Text)
    spending_limit = Column(Float)
    currency = Column(Text, nullable=False)
    card_status = Column(Text, nullable=False)
    home_country = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class CardControl(Base):
    __tablename__ = "card_controls"
    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False, unique=True)
    international_allowed = Column(Integer, nullable=False)
    allowed_countries = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Payee(Base):
    __tablename__ = "payees"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(Text, nullable=False)
    category = Column(Text)
    default_memo = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class PayeeRoutingInfo(Base):
    __tablename__ = "payee_routing_info"
    id = Column(Integer, primary_key=True)
    payee_id = Column(Integer, ForeignKey("payees.id"), nullable=False)
    bank_name = Column(Text, nullable=False)
    routing_number = Column(Text, nullable=False)
    account_number = Column(Text, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class ScheduledTransfer(Base):
    __tablename__ = "scheduled_transfers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    to_account_id = Column(Integer, ForeignKey("accounts.id"))
    payee_id = Column(Integer, ForeignKey("payees.id"))
    transfer_type = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(Text, nullable=False)
    schedule_type = Column(Text, nullable=False)
    recurrence_rule = Column(Text)
    start_date = Column(Text, nullable=False)
    end_date = Column(Text)
    next_run_date = Column(Text)
    state = Column(Text, nullable=False)
    tag = Column(Text)
    memo = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Transfer(Base):
    __tablename__ = "transfers"
    id = Column(Integer, primary_key=True)
    scheduled_transfer_id = Column(Integer, ForeignKey("scheduled_transfers.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    to_account_id = Column(Integer, ForeignKey("accounts.id"))
    payee_id = Column(Integer, ForeignKey("payees.id"))
    transfer_type = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(Text, nullable=False)
    state = Column(Text, nullable=False)
    failure_reason = Column(Text)
    executed_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    transfer_id = Column(Integer, ForeignKey("transfers.id"))
    card_id = Column(Integer, ForeignKey("cards.id"))
    type = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(Text, nullable=False)
    description = Column(Text)
    merchant_metadata = Column(Text)
    posted_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TransactionTag(Base):
    __tablename__ = "transaction_tags"
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    tag = Column(Text, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class AlertPreference(Base):
    __tablename__ = "alert_preferences"
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    alert_type = Column(Text, nullable=False)
    threshold_amount = Column(Float, nullable=False)
    channel_email = Column(Integer, nullable=False)
    channel_push = Column(Integer, nullable=False)
    channel_sms = Column(Integer, nullable=False)
    is_enabled = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class CardHold(Base):
    __tablename__ = "card_holds"
    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(Text, nullable=False)
    merchant_metadata = Column(Text)
    state = Column(Text, nullable=False)
    authorized_at = Column(DateTime, nullable=False)
    captured_at = Column(DateTime)
    released_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class DirectDepositConfig(Base):
    __tablename__ = "direct_deposit_configs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    employer_id = Column(Text, nullable=False)
    employer_name = Column(Text)
    allocation_type = Column(Text, nullable=False)
    is_active = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class DirectDepositAllocation(Base):
    __tablename__ = "direct_deposit_allocations"
    id = Column(Integer, primary_key=True)
    direct_deposit_config_id = Column(Integer, ForeignKey("direct_deposit_configs.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    percentage = Column(Float, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


Base.metadata.create_all(bind=engine)


def now_utc_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def parse_date_string(value: str) -> date:
    return date.fromisoformat(value)


def date_to_string(value: Optional[str]) -> Optional[str]:
    return value


def datetime_to_iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.replace(microsecond=0).isoformat() + "Z"


class CustomerModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Customer ID", example=10)
    user_id: int = Field(..., description="Linked users.id", example=1)
    legal_name: str = Field(..., description="Legal full name", example="Jordan Smith")
    date_of_birth: str = Field(..., description="Date of birth in ISO format", example="1990-04-12")
    ssn_last4: str = Field(..., description="Last 4 digits of SSN", example="1234")
    address_line1: str = Field(..., description="Primary street address", example="1200 Elm Street")
    address_line2: Optional[str] = Field(None, description="Secondary address line", example="Apt 5B")
    city: str = Field(..., description="City name", example="Austin")
    state: str = Field(..., description="State or province code", example="TX")
    postal_code: str = Field(..., description="Postal or ZIP code", example="78701")
    country: str = Field(..., description="Country code", example="US")
    mobile_number: str = Field(..., description="Mobile phone number in E.164 format", example="+1-512-555-0199")
    kyc_status: str = Field(..., description="KYC review status", example="pending")
    kyc_last_reviewed_at: Optional[str] = Field(None, description="Last KYC review timestamp or null", example="2026-01-15T10:03:00Z")
    created_at: str = Field(..., description="Creation timestamp", example="2026-01-10T09:00:00Z")
    updated_at: str = Field(..., description="Last update timestamp", example="2026-01-15T10:03:00Z")


class CustomerResponse(BaseModel):
    customer: CustomerModel = Field(..., description="Customer profile", example={})


class CustomerCreateRequest(BaseModel):
    legal_name: str = Field(..., description="Legal full name for KYC", example="Jordan Smith")
    date_of_birth: str = Field(..., description="Date of birth in ISO format YYYY-MM-DD", example="1990-04-12")
    ssn_last4: str = Field(..., description="Last 4 digits of SSN", example="1234")
    address_line1: str = Field(..., description="Primary street address", example="1200 Elm Street")
    address_line2: Optional[str] = Field(None, description="Secondary address line if any", example=None)
    city: str = Field(..., description="City name", example="Austin")
    state: str = Field(..., description="State or province code", example="TX")
    postal_code: str = Field(..., description="Postal or ZIP code", example="78701")
    country: Optional[str] = Field("US", description="Country code, defaults to US", example="US")
    mobile_number: str = Field(..., description="Mobile phone number in E.164 format", example="+1-512-555-0199")


class KYCStatusResponse(BaseModel):
    kyc_status: str = Field(..., description="KYC review status for the customer", example="approved")
    kyc_last_reviewed_at: Optional[str] = Field(None, description="Timestamp when KYC was last reviewed", example="2026-01-15T10:03:00Z")


class AccountModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Account ID", example=101)
    customer_id: int = Field(..., description="Linked customers.id", example=10)
    account_number: str = Field(..., description="Unique account number", example="000000001023")
    account_type: str = Field(..., description="Account type (checking or savings)", example="checking")
    currency: str = Field(..., description="Three-letter currency code", example="USD")
    current_balance: float = Field(..., description="Current available balance", example=1520.75)
    interest_rate: float = Field(..., description="Annual interest rate for this account", example=0.015)
    is_primary: bool = Field(..., description="True if this is the primary account of its type", example=True)
    status: str = Field(..., description="Account status", example="open")
    created_at: str = Field(..., description="Creation timestamp", example="2026-01-01T08:00:00Z")
    updated_at: str = Field(..., description="Last update timestamp", example="2026-01-20T12:00:00Z")


class AccountsListResponse(BaseModel):
    accounts: List[AccountModel] = Field(..., description="List of accounts", example=[])


class AccountCreateRequest(BaseModel):
    account_type: str = Field(..., description="Account type to create (checking or savings)", example="savings")
    currency: str = Field(..., description="Three-letter currency code", example="USD")
    is_primary: Optional[int] = Field(0, description="1 to mark as primary, 0 otherwise", example=0)
    interest_rate: Optional[float] = Field(None, description="Optional explicit interest rate", example=0.01)


class AccountResponse(BaseModel):
    account: AccountModel = Field(..., description="Account details", example={})


class AccountBalanceResponse(BaseModel):
    account_id: int = Field(..., description="Account ID", example=101)
    current_balance: float = Field(..., description="Current account balance", example=1280.0)
    currency: str = Field(..., description="Currency of the balance", example="USD")


class CardModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Card ID", example=301)
    account_id: int = Field(..., description="Linked accounts.id", example=101)
    card_type: str = Field(..., description="Card type", example="virtual")
    last4: str = Field(..., description="Last 4 digits of the card PAN", example="4456")
    network: Optional[str] = Field(None, description="Card network brand", example="VISA")
    spending_limit: Optional[float] = Field(None, description="Card spending limit if set", example=2000.0)
    currency: str = Field(..., description="Card currency", example="USD")
    card_status: str = Field(..., description="Card status", example="inactive")
    home_country: Optional[str] = Field(None, description="Home country for this card", example="US")
    created_at: str = Field(..., description="Creation timestamp", example="2026-02-01T10:00:00Z")
    updated_at: str = Field(..., description="Last update timestamp", example="2026-02-01T10:00:00Z")


class CardResponse(BaseModel):
    card: CardModel = Field(..., description="Card details", example={})


class CardCreateRequest(BaseModel):
    account_id: int = Field(..., description="Account ID that this card should be linked to", example=101)
    card_type: str = Field(..., description="Type of card (virtual or physical)", example="virtual")
    last4: str = Field(..., description="Last 4 digits of the card number", example="4456")
    network: Optional[str] = Field(None, description="Card network brand", example="VISA")
    spending_limit: Optional[float] = Field(None, description="Optional card-level spending limit", example=2000.0)
    currency: str = Field(..., description="Card currency, usually same as account", example="USD")
    home_country: Optional[str] = Field(None, description="Card's home country for controls", example="US")


class CardStatusUpdateRequest(BaseModel):
    card_status: str = Field(..., description="New status: inactive, active, blocked, or closed", example="active")


class CardSpendingLimitUpdateRequest(BaseModel):
    spending_limit: float = Field(..., description="New monthly spending limit amount", example=2000.0)


class CardSpendingLimitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Card ID", example=301)
    spending_limit: Optional[float] = Field(None, description="Updated spending limit", example=2000.0)
    currency: str = Field(..., description="Card currency", example="USD")
    card_status: str = Field(..., description="Card status", example="active")
    updated_at: str = Field(..., description="Last update timestamp", example="2026-02-01T10:10:00Z")


class CardsListResponse(BaseModel):
    cards: List[CardModel] = Field(..., description="List of cards", example=[])


class CardControlModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Card controls ID", example=401)
    card_id: int = Field(..., description="Linked cards.id", example=301)
    international_allowed: bool = Field(..., description="International transactions allowed flag", example=False)
    allowed_countries: Optional[str] = Field(None, description="Comma-separated allowed countries", example="US,CA")
    created_at: str = Field(..., description="Creation timestamp", example="2026-02-01T10:15:00Z")
    updated_at: str = Field(..., description="Last update timestamp", example="2026-02-01T10:15:00Z")


class CardControlResponse(BaseModel):
    card_controls: CardControlModel = Field(..., description="Card controls details", example={})


class CardControlCreateRequest(BaseModel):
    card_id: int = Field(..., description="Card ID to attach controls to", example=301)
    international_allowed: Optional[int] = Field(1, description="1 to allow international, 0 to restrict", example=0)
    allowed_countries: Optional[str] = Field(None, description="Comma-separated list of allowed country codes", example="US,CA")


class CardControlUpdateRequest(BaseModel):
    international_allowed: Optional[int] = Field(None, description="1 to allow all international, 0 to enforce allowed countries", example=0)
    allowed_countries: Optional[str] = Field(None, description="Updated comma-separated list of allowed countries", example="US,CA")


class PayeeModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Payee ID", example=501)
    user_id: int = Field(..., description="Owner users.id", example=1)
    name: str = Field(..., description="Payee name", example="Downtown Utilities")
    category: Optional[str] = Field(None, description="Payee category", example="utilities")
    default_memo: Optional[str] = Field(None, description="Default memo", example="Water and electric bill")
    created_at: str = Field(..., description="Created at", example="2026-02-01T11:00:00Z")
    updated_at: str = Field(..., description="Updated at", example="2026-02-01T11:00:00Z")


class PayeeResponse(BaseModel):
    payee: PayeeModel = Field(..., description="Payee details", example={})


class PayeeCreateRequest(BaseModel):
    name: str = Field(..., description="Payee display name", example="Downtown Utilities")
    category: Optional[str] = Field(None, description="Category label for this payee", example="utilities")
    default_memo: Optional[str] = Field(None, description="Default memo to use for transfers", example="Water and electric bill")


class PayeeRoutingInfoModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Routing info ID", example=601)
    payee_id: int = Field(..., description="Linked payees.id", example=501)
    bank_name: str = Field(..., description="Bank name", example="Metro Bank")
    routing_number: str = Field(..., description="Routing number", example="021000021")
    account_number: str = Field(..., description="Account number", example="9988776655")
    created_at: str = Field(..., description="Created at", example="2026-02-01T11:05:00Z")
    updated_at: str = Field(..., description="Updated at", example="2026-02-01T11:05:00Z")


class PayeeRoutingInfoResponse(BaseModel):
    routing_info: PayeeRoutingInfoModel = Field(..., description="Routing info details", example={})


class PayeeRoutingInfoCreateRequest(BaseModel):
    bank_name: str = Field(..., description="Destination bank name", example="Metro Bank")
    routing_number: str = Field(..., description="ABA routing number", example="021000021")
    account_number: str = Field(..., description="Destination bank account number", example="9988776655")


class PayeesListResponse(BaseModel):
    payees: List[PayeeModel] = Field(..., description="List of payees", example=[])


class ScheduledTransferModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Scheduled transfer ID", example=701)
    user_id: int = Field(..., description="Owner users.id", example=1)
    from_account_id: int = Field(..., description="Source accounts.id", example=101)
    to_account_id: Optional[int] = Field(None, description="Destination accounts.id for internal transfers", example=202)
    payee_id: Optional[int] = Field(None, description="Destination payees.id for external transfers", example=501)
    transfer_type: str = Field(..., description="Transfer type", example="external")
    amount: float = Field(..., description="Transfer amount", example=120.75)
    currency: str = Field(..., description="Currency code", example="USD")
    schedule_type: str = Field(..., description="Schedule type", example="recurring")
    recurrence_rule: Optional[str] = Field(None, description="Recurrence rule string", example="FREQ=MONTHLY;BYMONTHDAY=5")
    start_date: str = Field(..., description="Start date", example="2026-02-05")
    end_date: Optional[str] = Field(None, description="End date or null", example=None)
    next_run_date: Optional[str] = Field(None, description="Next execution date in YYYY-MM-DD", example="2026-02-05")
    state: str = Field(..., description="State of scheduled transfer", example="scheduled")
    tag: Optional[str] = Field(None, description="Tag", example="bills")
    memo: Optional[str] = Field(None, description="Memo", example="Downtown Utilities monthly bill")
    created_at: str = Field(..., description="Created at", example="2026-02-01T11:10:00Z")
    updated_at: str = Field(..., description="Updated at", example="2026-02-01T11:10:00Z")


class ScheduledTransferResponse(BaseModel):
    scheduled_transfer: ScheduledTransferModel = Field(..., description="Scheduled transfer details", example={})


class ScheduledTransferCreateRequest(BaseModel):
    from_account_id: int = Field(..., description="Source accounts.id", example=101)
    to_account_id: Optional[int] = Field(None, description="Destination accounts.id for internal transfers", example=202)
    payee_id: Optional[int] = Field(None, description="Destination payees.id for external transfers", example=501)
    transfer_type: str = Field(..., description="internal or external", example="external")
    amount: float = Field(..., description="Transfer amount", example=120.75)
    currency: str = Field(..., description="Currency code", example="USD")
    schedule_type: str = Field(..., description="one_time or recurring", example="recurring")
    recurrence_rule: Optional[str] = Field(None, description="Recurrence rule", example="FREQ=MONTHLY;BYMONTHDAY=5")
    start_date: str = Field(..., description="Scheduled start date in YYYY-MM-DD", example="2026-02-05")
    end_date: Optional[str] = Field(None, description="Optional end date in YYYY-MM-DD", example=None)
    tag: Optional[str] = Field(None, description="Tag label for this scheduled transfer", example="bills")
    memo: Optional[str] = Field(None, description="Optional descriptive memo", example="Downtown Utilities monthly bill")


class TransferModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Transfer ID", example=801)
    scheduled_transfer_id: Optional[int] = Field(None, description="Linked schedule if any", example=None)
    user_id: int = Field(..., description="Owner users.id", example=1)
    from_account_id: int = Field(..., description="Source accounts.id", example=101)
    to_account_id: Optional[int] = Field(None, description="Destination accounts.id for internal transfers", example=202)
    payee_id: Optional[int] = Field(None, description="Destination payee for external transfers", example=None)
    transfer_type: str = Field(..., description="Transfer type", example="internal")
    amount: float = Field(..., description="Amount", example=250.0)
    currency: str = Field(..., description="Currency", example="USD")
    state: str = Field(..., description="Transfer state", example="completed")
    failure_reason: Optional[str] = Field(None, description="Failure reason if state is failed", example=None)
    executed_at: Optional[str] = Field(None, description="Execution timestamp", example="2026-02-01T11:20:00Z")
    created_at: str = Field(..., description="Created at", example="2026-02-01T11:20:00Z")
    updated_at: str = Field(..., description="Updated at", example="2026-02-01T11:20:00Z")


class UpdatedAccountBalanceModel(BaseModel):
    id: int = Field(..., description="Account ID", example=101)
    current_balance: float = Field(..., description="Updated balance after transfer", example=1280.0)
    currency: str = Field(..., description="Account currency", example="USD")


class TransferCreateRequest(BaseModel):
    from_account_id: int = Field(..., description="Source accounts.id", example=101)
    to_account_id: Optional[int] = Field(None, description="Destination accounts.id for internal transfers", example=202)
    payee_id: Optional[int] = Field(None, description="Destination payees.id for external transfers", example=501)
    transfer_type: str = Field(..., description="internal or external", example="internal")
    amount: float = Field(..., description="Transfer amount", example=250.0)
    currency: str = Field(..., description="Currency code", example="USD")
    scheduled_transfer_id: Optional[int] = Field(None, description="Optional linked scheduled_transfers.id", example=None)


class TransferCreateResponse(BaseModel):
    transfer: TransferModel = Field(..., description="Transfer details", example={})
    updated_accounts: List[UpdatedAccountBalanceModel] = Field(..., description="Updated accounts", example=[])


class TransferResponse(BaseModel):
    transfer: TransferModel = Field(..., description="Transfer details", example={})


class TransactionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Transaction ID", example=901)
    account_id: int = Field(..., description="Linked accounts.id", example=101)
    transfer_id: Optional[int] = Field(None, description="Linked transfers.id if any", example=None)
    card_id: Optional[int] = Field(None, description="Linked cards.id for card transactions", example=301)
    type: str = Field(..., description="debit or credit", example="debit")
    amount: float = Field(..., description="Transaction amount", example=85.32)
    currency: str = Field(..., description="Currency", example="USD")
    description: Optional[str] = Field(None, description="Transaction description", example="CARD PURCHASE")
    merchant_metadata: Optional[str] = Field(None, description="Raw merchant data string", example="GROCERY MART AUSTIN TX")
    posted_at: Optional[str] = Field(None, description="Posting timestamp", example="2026-01-10T13:45:00Z")
    created_at: str = Field(..., description="Created at", example="2026-01-10T13:45:00Z")
    updated_at: str = Field(..., description="Updated at", example="2026-01-10T13:45:00Z")


class TransactionsListResponse(BaseModel):
    transactions: List[TransactionModel] = Field(..., description="List of transactions", example=[])


class TransactionTagModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Transaction tag ID", example=1001)
    transaction_id: int = Field(..., description="Linked transactions.id", example=901)
    tag: str = Field(..., description="Tag value", example="groceries")
    created_at: str = Field(..., description="Created timestamp", example="2026-01-10T14:00:00Z")
    updated_at: str = Field(..., description="Updated timestamp", example="2026-01-10T14:00:00Z")


class TransactionTagResponse(BaseModel):
    transaction_tag: TransactionTagModel = Field(..., description="Transaction tag details", example={})


class TransactionTagCreateRequest(BaseModel):
    transaction_id: int = Field(..., description="transactions.id to tag", example=901)
    tag: str = Field(..., description="Tag label to add", example="groceries")


class TransactionTagsListResponse(BaseModel):
    tags: List[TransactionTagModel] = Field(..., description="List of tags", example=[])


class AlertPreferenceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Alert preference ID", example=1101)
    account_id: int = Field(..., description="Linked accounts.id", example=101)
    alert_type: str = Field(..., description="Alert type", example="low_balance")
    threshold_amount: float = Field(..., description="Threshold amount", example=100.0)
    channel_email: bool = Field(..., description="Email channel enabled", example=True)
    channel_push: bool = Field(..., description="Push channel enabled", example=True)
    channel_sms: bool = Field(..., description="SMS channel enabled", example=False)
    is_enabled: bool = Field(..., description="Enabled flag", example=True)
    created_at: str = Field(..., description="Created at", example="2026-02-01T11:30:00Z")
    updated_at: str = Field(..., description="Updated at", example="2026-02-01T11:30:00Z")


class AlertPreferenceResponse(BaseModel):
    alert_preference: AlertPreferenceModel = Field(..., description="Alert preference details", example={})


class AlertPreferenceCreateRequest(BaseModel):
    account_id: int = Field(..., description="accounts.id the alert applies to", example=101)
    alert_type: str = Field(..., description="low_balance or large_transaction", example="low_balance")
    threshold_amount: float = Field(..., description="Threshold amount that triggers the alert", example=100.0)
    channel_email: Optional[int] = Field(0, description="1 to enable email notifications, 0 otherwise", example=1)
    channel_push: Optional[int] = Field(0, description="1 to enable push notifications, 0 otherwise", example=1)
    channel_sms: Optional[int] = Field(0, description="1 to enable SMS notifications, 0 otherwise", example=0)
    is_enabled: Optional[int] = Field(1, description="1 to enable this alert preference, 0 to disable", example=1)


class AlertPreferenceUpdateRequest(BaseModel):
    threshold_amount: Optional[float] = Field(None, description="New threshold amount", example=100.0)
    channel_email: Optional[int] = Field(None, description="Updated email channel flag", example=1)
    channel_push: Optional[int] = Field(None, description="Updated push channel flag", example=1)
    channel_sms: Optional[int] = Field(None, description="Updated SMS channel flag", example=0)
    is_enabled: Optional[int] = Field(None, description="Updated enabled flag", example=1)


class AlertPreferencesListResponse(BaseModel):
    alert_preferences: List[AlertPreferenceModel] = Field(..., description="List of alert preferences", example=[])


class CardHoldModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Hold ID", example=1201)
    card_id: int = Field(..., description="Linked cards.id that created the hold", example=301)
    account_id: int = Field(..., description="Linked accounts.id", example=101)
    amount: float = Field(..., description="Authorization amount", example=250.0)
    currency: str = Field(..., description="Currency code", example="USD")
    merchant_metadata: Optional[str] = Field(None, description="Merchant metadata string", example="HOTEL AUSTIN TX")
    state: str = Field(..., description="Hold state", example="authorized")
    authorized_at: str = Field(..., description="Authorization timestamp", example="2026-01-25T18:00:00Z")
    captured_at: Optional[str] = Field(None, description="Capture timestamp or null", example=None)
    released_at: Optional[str] = Field(None, description="Release timestamp or null", example=None)
    created_at: str = Field(..., description="Created at", example="2026-01-25T18:00:00Z")
    updated_at: str = Field(..., description="Updated at", example="2026-01-25T18:00:00Z")


class CardHoldsListResponse(BaseModel):
    holds: List[CardHoldModel] = Field(..., description="List of holds", example=[])


class CardHoldSummaryModel(BaseModel):
    card_id: int = Field(..., description="cards.id associated with the hold", example=301)
    amount: float = Field(..., description="Authorized hold amount", example=250.0)
    currency: str = Field(..., description="Currency of the hold", example="USD")
    merchant_metadata: Optional[str] = Field(None, description="Merchant metadata string", example="HOTEL AUSTIN TX")
    authorized_at: str = Field(..., description="Authorization timestamp", example="2026-01-25T18:00:00Z")


class CardHoldsSummaryResponse(BaseModel):
    holds_summary: List[CardHoldSummaryModel] = Field(..., description="Summary list of holds", example=[])


class DirectDepositConfigModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Direct deposit config ID", example=1301)
    user_id: int = Field(..., description="Owner users.id", example=1)
    employer_id: str = Field(..., description="Employer identifier", example="ACME-001")
    employer_name: Optional[str] = Field(None, description="Employer name", example="Acme Corp")
    allocation_type: str = Field(..., description="Allocation type", example="percentage")
    is_active: bool = Field(..., description="Active flag", example=True)
    created_at: str = Field(..., description="Created at", example="2026-02-01T11:40:00Z")
    updated_at: str = Field(..., description="Updated at", example="2026-02-01T11:40:00Z")


class DirectDepositConfigResponse(BaseModel):
    direct_deposit_config: DirectDepositConfigModel = Field(..., description="Direct deposit config details", example={})


class DirectDepositConfigCreateRequest(BaseModel):
    employer_id: str = Field(..., description="External employer identifier string", example="ACME-001")
    employer_name: Optional[str] = Field(None, description="Human-readable employer name", example="Acme Corp")
    allocation_type: Optional[str] = Field("percentage", description="Allocation type, currently only 'percentage'", example="percentage")
    is_active: Optional[int] = Field(1, description="1 to enable this config, 0 to disable", example=1)


class DirectDepositAllocationModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Allocation ID", example=1401)
    direct_deposit_config_id: int = Field(..., description="Linked direct_deposit_configs.id", example=1301)
    account_id: int = Field(..., description="Destination accounts.id", example=202)
    percentage: float = Field(..., description="Allocation percentage", example=70.0)
    created_at: str = Field(..., description="Created at", example="2026-02-01T11:45:00Z")
    updated_at: str = Field(..., description="Updated at", example="2026-02-01T11:45:00Z")


class DirectDepositAllocationResponse(BaseModel):
    direct_deposit_allocation: DirectDepositAllocationModel = Field(..., description="Direct deposit allocation details", example={})


class DirectDepositAllocationCreateRequest(BaseModel):
    direct_deposit_config_id: int = Field(..., description="direct_deposit_configs.id to attach this allocation to", example=1301)
    account_id: int = Field(..., description="accounts.id receiving this allocation", example=202)
    percentage: float = Field(..., description="Percentage of paycheck routed to this account", example=70.0)


class DirectDepositAllocationsListResponse(BaseModel):
    allocations: List[DirectDepositAllocationModel] = Field(..., description="List of allocations", example=[])


class DirectDepositSetupResponse(BaseModel):
    direct_deposit_config: DirectDepositConfigModel = Field(..., description="Direct deposit config", example={})
    allocations: List[DirectDepositAllocationModel] = Field(..., description="Allocations for this config", example=[])


@app.get(
    "/api/customers/me",
    response_model=CustomerResponse,
    summary="Get current user's customer profile",
    description="Retrieve the customer profile for the authenticated user_id=1.",
    tags=["customers"],
    operation_id="get_my_customer_profile",
)
async def get_my_customer_profile() -> CustomerResponse:
    session = SessionLocal()
    customer = session.query(Customer).filter(Customer.user_id == 1).first()
    if customer is None:
        session.close()
        now = datetime.utcnow()
        new_customer = Customer(
            user_id=1,
            legal_name="Demo User",
            date_of_birth="1990-01-01",
            ssn_last4="0000",
            address_line1="Unknown",
            address_line2=None,
            city="Unknown",
            state="NA",
            postal_code="00000",
            country="US",
            mobile_number="+10000000000",
            kyc_status="pending",
            kyc_last_reviewed_at=None,
            created_at=now,
            updated_at=now,
        )
        session.add(new_customer)
        session.commit()
        customer = new_customer
    customer_model = CustomerModel(
        id=customer.id,
        user_id=customer.user_id,
        legal_name=customer.legal_name,
        date_of_birth=customer.date_of_birth,
        ssn_last4=customer.ssn_last4,
        address_line1=customer.address_line1,
        address_line2=customer.address_line2,
        city=customer.city,
        state=customer.state,
        postal_code=customer.postal_code,
        country=customer.country,
        mobile_number=customer.mobile_number,
        kyc_status=customer.kyc_status,
        kyc_last_reviewed_at=datetime_to_iso(customer.kyc_last_reviewed_at),
        created_at=datetime_to_iso(customer.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(customer.updated_at) or now_utc_iso(),
    )
    session.close()
    return CustomerResponse(customer=customer_model)


@app.post(
    "/api/customers",
    response_model=CustomerResponse,
    summary="Create customer profile for current user",
    description="Create the customer row for authenticated user_id=1 with KYC attributes.",
    tags=["customers"],
    operation_id="create_my_customer_profile",
)
async def create_my_customer_profile(payload: CustomerCreateRequest = Body(...)) -> CustomerResponse:
    session = SessionLocal()
    existing = session.query(Customer).filter(Customer.user_id == 1).first()
    now = datetime.utcnow()
    if existing is None:
        customer = Customer(
            user_id=1,
            legal_name=payload.legal_name,
            date_of_birth=payload.date_of_birth,
            ssn_last4=payload.ssn_last4,
            address_line1=payload.address_line1,
            address_line2=payload.address_line2,
            city=payload.city,
            state=payload.state,
            postal_code=payload.postal_code,
            country=payload.country or "US",
            mobile_number=payload.mobile_number,
            kyc_status="pending",
            kyc_last_reviewed_at=None,
            created_at=now,
            updated_at=now,
        )
        session.add(customer)
        session.commit()
    else:
        customer = existing
        customer.legal_name = payload.legal_name
        customer.date_of_birth = payload.date_of_birth
        customer.ssn_last4 = payload.ssn_last4
        customer.address_line1 = payload.address_line1
        customer.address_line2 = payload.address_line2
        customer.city = payload.city
        customer.state = payload.state
        customer.postal_code = payload.postal_code
        customer.country = payload.country or customer.country
        customer.mobile_number = payload.mobile_number
        customer.updated_at = now
        session.commit()
    customer_model = CustomerModel(
        id=customer.id,
        user_id=customer.user_id,
        legal_name=customer.legal_name,
        date_of_birth=customer.date_of_birth,
        ssn_last4=customer.ssn_last4,
        address_line1=customer.address_line1,
        address_line2=customer.address_line2,
        city=customer.city,
        state=customer.state,
        postal_code=customer.postal_code,
        country=customer.country,
        mobile_number=customer.mobile_number,
        kyc_status=customer.kyc_status,
        kyc_last_reviewed_at=datetime_to_iso(customer.kyc_last_reviewed_at),
        created_at=datetime_to_iso(customer.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(customer.updated_at) or now_utc_iso(),
    )
    session.close()
    return CustomerResponse(customer=customer_model)


@app.get(
    "/api/customers/me/kyc-status",
    response_model=KYCStatusResponse,
    summary="Get my customer KYC status",
    description="Return only the kyc_status and kyc_last_reviewed_at for current user.",
    tags=["customers"],
    operation_id="get_my_kyc_status",
)
async def get_my_kyc_status() -> KYCStatusResponse:
    session = SessionLocal()
    customer = session.query(Customer).filter(Customer.user_id == 1).first()
    if customer is None:
        session.close()
        return KYCStatusResponse(kyc_status="pending", kyc_last_reviewed_at=None)
    response = KYCStatusResponse(
        kyc_status=customer.kyc_status,
        kyc_last_reviewed_at=datetime_to_iso(customer.kyc_last_reviewed_at),
    )
    session.close()
    return response


@app.get(
    "/api/accounts",
    response_model=AccountsListResponse,
    summary="List all accounts for current user",
    description="Retrieve all accounts for current user's customer, with filters.",
    tags=["accounts"],
    operation_id="list_my_accounts",
)
async def list_my_accounts(
    account_type: Optional[str] = Query(None, description="Filter by account_type", example="checking"),
    status: Optional[str] = Query(None, description="Filter by status", example="open"),
) -> AccountsListResponse:
    session = SessionLocal()
    customer = session.query(Customer).filter(Customer.user_id == 1).first()
    if customer is None:
        session.close()
        return AccountsListResponse(accounts=[])
    query = session.query(Account).filter(Account.customer_id == customer.id)
    if account_type is not None:
        query = query.filter(Account.account_type == account_type)
    if status is not None:
        query = query.filter(Account.status == status)
    accounts = query.all()
    result: List[AccountModel] = []
    for acc in accounts:
        result.append(
            AccountModel(
                id=acc.id,
                customer_id=acc.customer_id,
                account_number=acc.account_number,
                account_type=acc.account_type,
                currency=acc.currency,
                current_balance=acc.current_balance,
                interest_rate=acc.interest_rate,
                is_primary=bool(acc.is_primary),
                status=acc.status,
                created_at=datetime_to_iso(acc.created_at) or now_utc_iso(),
                updated_at=datetime_to_iso(acc.updated_at) or now_utc_iso(),
            )
        )
    session.close()
    return AccountsListResponse(accounts=result)


def generate_account_number(session) -> str:
    base = "000000000000"
    last = session.query(Account).order_by(Account.id.desc()).first()
    next_id = 1 if last is None else last.id + 1
    padded = str(next_id).rjust(4, "0")
    return base[:-4] + padded


@app.post(
    "/api/accounts",
    response_model=AccountResponse,
    summary="Create a new account for current user",
    description="Create a new checking or savings account for current user's customer.",
    tags=["accounts"],
    operation_id="create_account_for_current_customer",
)
async def create_account_for_current_customer(payload: AccountCreateRequest = Body(...)) -> AccountResponse:
    session = SessionLocal()
    customer = session.query(Customer).filter(Customer.user_id == 1).first()
    now = datetime.utcnow()
    if customer is None:
        customer = Customer(
            user_id=1,
            legal_name="Demo User",
            date_of_birth="1990-01-01",
            ssn_last4="0000",
            address_line1="Unknown",
            address_line2=None,
            city="Unknown",
            state="NA",
            postal_code="00000",
            country="US",
            mobile_number="+10000000000",
            kyc_status="pending",
            kyc_last_reviewed_at=None,
            created_at=now,
            updated_at=now,
        )
        session.add(customer)
        session.commit()
    rate = payload.interest_rate if payload.interest_rate is not None else (0.0 if payload.account_type == "checking" else 0.01)
    is_primary_value = payload.is_primary if payload.is_primary is not None else 0
    acc_number = generate_account_number(session)
    new_acc = Account(
        customer_id=customer.id,
        account_number=acc_number,
        account_type=payload.account_type,
        currency=payload.currency,
        current_balance=0.0,
        interest_rate=rate,
        is_primary=is_primary_value,
        status="open",
        created_at=now,
        updated_at=now,
    )
    session.add(new_acc)
    session.commit()
    model = AccountModel(
        id=new_acc.id,
        customer_id=new_acc.customer_id,
        account_number=new_acc.account_number,
        account_type=new_acc.account_type,
        currency=new_acc.currency,
        current_balance=new_acc.current_balance,
        interest_rate=new_acc.interest_rate,
        is_primary=bool(new_acc.is_primary),
        status=new_acc.status,
        created_at=datetime_to_iso(new_acc.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(new_acc.updated_at) or now_utc_iso(),
    )
    session.close()
    return AccountResponse(account=model)


@app.get(
    "/api/accounts/by-last4/{account_last4}",
    response_model=AccountResponse,
    summary="Get my account details by last 4 digits",
    description="Look up an account for current user using the last 4 of account_number.",
    tags=["accounts"],
    operation_id="get_account_by_last4_for_current_user",
)
async def get_account_by_last4_for_current_user(
    account_last4: str = Path(..., description="Last 4 digits of the account_number", example="1023")
) -> AccountResponse:
    session = SessionLocal()
    customer = session.query(Customer).filter(Customer.user_id == 1).first()
    if customer is None:
        session.close()
        empty = AccountModel(
            id=0,
            customer_id=0,
            account_number="",
            account_type="checking",
            currency="USD",
            current_balance=0.0,
            interest_rate=0.0,
            is_primary=False,
            status="open",
            created_at=now_utc_iso(),
            updated_at=now_utc_iso(),
        )
        return AccountResponse(account=empty)
    accounts = session.query(Account).filter(Account.customer_id == customer.id).all()
    found = None
    for acc in accounts:
        if acc.account_number.endswith(account_last4):
            found = acc
            break
    if found is None:
        session.close()
        empty = AccountModel(
            id=0,
            customer_id=customer.id,
            account_number="",
            account_type="checking",
            currency="USD",
            current_balance=0.0,
            interest_rate=0.0,
            is_primary=False,
            status="open",
            created_at=now_utc_iso(),
            updated_at=now_utc_iso(),
        )
        return AccountResponse(account=empty)
    model = AccountModel(
        id=found.id,
        customer_id=found.customer_id,
        account_number=found.account_number,
        account_type=found.account_type,
        currency=found.currency,
        current_balance=found.current_balance,
        interest_rate=found.interest_rate,
        is_primary=bool(found.is_primary),
        status=found.status,
        created_at=datetime_to_iso(found.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(found.updated_at) or now_utc_iso(),
    )
    session.close()
    return AccountResponse(account=model)


@app.get(
    "/api/accounts/{account_id}",
    response_model=AccountResponse,
    summary="Get a specific account by ID",
    description="Retrieve a single account by ID after verifying ownership.",
    tags=["accounts"],
    operation_id="get_account_by_id_for_current_user",
)
async def get_account_by_id_for_current_user(
    account_id: int = Path(..., description="accounts.id to retrieve", example=101)
) -> AccountResponse:
    session = SessionLocal()
    account = session.query(Account).filter(Account.id == account_id).first()
    if account is None:
        session.close()
        empty = AccountModel(
            id=0,
            customer_id=0,
            account_number="",
            account_type="checking",
            currency="USD",
            current_balance=0.0,
            interest_rate=0.0,
            is_primary=False,
            status="open",
            created_at=now_utc_iso(),
            updated_at=now_utc_iso(),
        )
        return AccountResponse(account=empty)
    customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
    if customer is None:
        session.close()
        empty = AccountModel(
            id=0,
            customer_id=0,
            account_number="",
            account_type=account.account_type,
            currency=account.currency,
            current_balance=0.0,
            interest_rate=0.0,
            is_primary=False,
            status="open",
            created_at=now_utc_iso(),
            updated_at=now_utc_iso(),
        )
        return AccountResponse(account=empty)
    model = AccountModel(
        id=account.id,
        customer_id=account.customer_id,
        account_number=account.account_number,
        account_type=account.account_type,
        currency=account.currency,
        current_balance=account.current_balance,
        interest_rate=account.interest_rate,
        is_primary=bool(account.is_primary),
        status=account.status,
        created_at=datetime_to_iso(account.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(account.updated_at) or now_utc_iso(),
    )
    session.close()
    return AccountResponse(account=model)


@app.get(
    "/api/accounts/{account_id}/balance",
    response_model=AccountBalanceResponse,
    summary="Get balance for a specific account",
    description="Return only the current_balance and currency for an account.",
    tags=["accounts"],
    operation_id="get_account_balance_for_current_user",
)
async def get_account_balance_for_current_user(
    account_id: int = Path(..., description="accounts.id whose balance to retrieve", example=101)
) -> AccountBalanceResponse:
    session = SessionLocal()
    account = session.query(Account).filter(Account.id == account_id).first()
    if account is None:
        session.close()
        return AccountBalanceResponse(account_id=0, current_balance=0.0, currency="USD")
    customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
    if customer is None:
        session.close()
        return AccountBalanceResponse(account_id=0, current_balance=0.0, currency=account.currency)
    response = AccountBalanceResponse(account_id=account.id, current_balance=account.current_balance, currency=account.currency)
    session.close()
    return response


@app.post(
    "/api/cards",
    response_model=CardResponse,
    summary="Create a new card for an account",
    description="Create a virtual or physical card tied to an account.",
    tags=["cards"],
    operation_id="create_card_for_account",
)
async def create_card_for_account(payload: CardCreateRequest = Body(...)) -> CardResponse:
    session = SessionLocal()
    account = session.query(Account).filter(Account.id == payload.account_id).first()
    if account is None:
        now = datetime.utcnow()
        dummy_card = Card(
            account_id=0,
            card_type=payload.card_type,
            last4=payload.last4,
            network=payload.network,
            spending_limit=payload.spending_limit,
            currency=payload.currency,
            card_status="inactive",
            home_country=payload.home_country or "US",
            created_at=now,
            updated_at=now,
        )
        session.add(dummy_card)
        session.commit()
        card = dummy_card
    else:
        customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
        now = datetime.utcnow()
        if customer is None:
            dummy_card = Card(
                account_id=0,
                card_type=payload.card_type,
                last4=payload.last4,
                network=payload.network,
                spending_limit=payload.spending_limit,
                currency=payload.currency,
                card_status="inactive",
                home_country=payload.home_country or "US",
                created_at=now,
                updated_at=now,
            )
            session.add(dummy_card)
            session.commit()
            card = dummy_card
        else:
            card = Card(
                account_id=account.id,
                card_type=payload.card_type,
                last4=payload.last4,
                network=payload.network,
                spending_limit=payload.spending_limit,
                currency=payload.currency,
                card_status="inactive",
                home_country=payload.home_country or "US",
                created_at=now,
                updated_at=now,
            )
            session.add(card)
            session.commit()
    model = CardModel(
        id=card.id,
        account_id=card.account_id,
        card_type=card.card_type,
        last4=card.last4,
        network=card.network,
        spending_limit=card.spending_limit,
        currency=card.currency,
        card_status=card.card_status,
        home_country=card.home_country,
        created_at=datetime_to_iso(card.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(card.updated_at) or now_utc_iso(),
    )
    session.close()
    return CardResponse(card=model)


@app.patch(
    "/api/cards/{card_id}/status",
    response_model=CardResponse,
    summary="Update a card's status",
    description="Change card_status for a card owned by the current user.",
    tags=["cards"],
    operation_id="update_card_status",
)
async def update_card_status(
    card_id: int = Path(..., description="cards.id to update", example=301),
    payload: CardStatusUpdateRequest = Body(...),
) -> CardResponse:
    session = SessionLocal()
    card = session.query(Card).filter(Card.id == card_id).first()
    now = datetime.utcnow()
    if card is not None:
        account = session.query(Account).filter(Account.id == card.account_id).first()
        if account is not None:
            customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
            if customer is not None:
                card.card_status = payload.card_status
                card.updated_at = now
                session.commit()
    if card is None:
        card = Card(
            account_id=0,
            card_type="virtual",
            last4="0000",
            network=None,
            spending_limit=None,
            currency="USD",
            card_status=payload.card_status,
            home_country="US",
            created_at=now,
            updated_at=now,
        )
        session.add(card)
        session.commit()
    model = CardModel(
        id=card.id,
        account_id=card.account_id,
        card_type=card.card_type,
        last4=card.last4,
        network=card.network,
        spending_limit=card.spending_limit,
        currency=card.currency,
        card_status=card.card_status,
        home_country=card.home_country,
        created_at=datetime_to_iso(card.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(card.updated_at) or now_utc_iso(),
    )
    session.close()
    return CardResponse(card=model)


@app.patch(
    "/api/cards/{card_id}/spending-limit",
    response_model=CardSpendingLimitResponse,
    summary="Update card spending limit",
    description="Set or change the spending_limit field for a card.",
    tags=["cards"],
    operation_id="update_card_spending_limit",
)
async def update_card_spending_limit(
    card_id: int = Path(..., description="cards.id whose spending limit to update", example=301),
    payload: CardSpendingLimitUpdateRequest = Body(...),
) -> CardSpendingLimitResponse:
    session = SessionLocal()
    card = session.query(Card).filter(Card.id == card_id).first()
    now = datetime.utcnow()
    if card is not None:
        account = session.query(Account).filter(Account.id == card.account_id).first()
        if account is not None:
            customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
            if customer is not None:
                card.spending_limit = payload.spending_limit
                card.updated_at = now
                session.commit()
    if card is None:
        card = Card(
            account_id=0,
            card_type="virtual",
            last4="0000",
            network=None,
            spending_limit=payload.spending_limit,
            currency="USD",
            card_status="inactive",
            home_country="US",
            created_at=now,
            updated_at=now,
        )
        session.add(card)
        session.commit()
    response = CardSpendingLimitResponse(
        id=card.id,
        spending_limit=card.spending_limit,
        currency=card.currency,
        card_status=card.card_status,
        updated_at=datetime_to_iso(card.updated_at) or now_utc_iso(),
    )
    session.close()
    return response


@app.get(
    "/api/cards/by-account-last4/{account_last4}",
    response_model=CardsListResponse,
    summary="List cards by account last4 for current user",
    description="Return all cards linked to the account whose account_number ends with last4.",
    tags=["cards"],
    operation_id="list_cards_by_account_last4",
)
async def list_cards_by_account_last4(
    account_last4: str = Path(..., description="Last 4 digits of the parent account_number", example="4456")
) -> CardsListResponse:
    session = SessionLocal()
    customer = session.query(Customer).filter(Customer.user_id == 1).first()
    if customer is None:
        session.close()
        return CardsListResponse(cards=[])
    accounts = session.query(Account).filter(Account.customer_id == customer.id).all()
    account_ids = []
    for acc in accounts:
        if acc.account_number.endswith(account_last4):
            account_ids.append(acc.id)
    if not account_ids:
        session.close()
        return CardsListResponse(cards=[])
    cards = session.query(Card).filter(Card.account_id.in_(account_ids)).all()
    result: List[CardModel] = []
    for card in cards:
        result.append(
            CardModel(
                id=card.id,
                account_id=card.account_id,
                card_type=card.card_type,
                last4=card.last4,
                network=card.network,
                spending_limit=card.spending_limit,
                currency=card.currency,
                card_status=card.card_status,
                home_country=card.home_country,
                created_at=datetime_to_iso(card.created_at) or now_utc_iso(),
                updated_at=datetime_to_iso(card.updated_at) or now_utc_iso(),
            )
        )
    session.close()
    return CardsListResponse(cards=result)


@app.post(
    "/api/card-controls",
    response_model=CardControlResponse,
    summary="Create card controls for a card",
    description="Initialize card_controls row for a card.",
    tags=["card_controls"],
    operation_id="create_card_controls",
)
async def create_card_controls(payload: CardControlCreateRequest = Body(...)) -> CardControlResponse:
    session = SessionLocal()
    card = session.query(Card).filter(Card.id == payload.card_id).first()
    now = datetime.utcnow()
    international_value = payload.international_allowed if payload.international_allowed is not None else 1
    allowed_countries_value = payload.allowed_countries
    if card is None:
        controls = CardControl(
            card_id=0,
            international_allowed=international_value,
            allowed_countries=allowed_countries_value,
            created_at=now,
            updated_at=now,
        )
        session.add(controls)
        session.commit()
    else:
        account = session.query(Account).filter(Account.id == card.account_id).first()
        if account is None:
            controls = CardControl(
                card_id=0,
                international_allowed=international_value,
                allowed_countries=allowed_countries_value,
                created_at=now,
                updated_at=now,
            )
            session.add(controls)
            session.commit()
        else:
            customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
            if customer is None:
                controls = CardControl(
                    card_id=0,
                    international_allowed=international_value,
                    allowed_countries=allowed_countries_value,
                    created_at=now,
                    updated_at=now,
                )
                session.add(controls)
                session.commit()
            else:
                existing = session.query(CardControl).filter(CardControl.card_id == card.id).first()
                if existing is None:
                    controls = CardControl(
                        card_id=card.id,
                        international_allowed=international_value,
                        allowed_countries=allowed_countries_value,
                        created_at=now,
                        updated_at=now,
                    )
                    session.add(controls)
                    session.commit()
                else:
                    controls = existing
    model = CardControlModel(
        id=controls.id,
        card_id=controls.card_id,
        international_allowed=bool(controls.international_allowed),
        allowed_countries=controls.allowed_countries,
        created_at=datetime_to_iso(controls.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(controls.updated_at) or now_utc_iso(),
    )
    session.close()
    return CardControlResponse(card_controls=model)


@app.patch(
    "/api/card-controls/{card_id}",
    response_model=CardControlResponse,
    summary="Update controls for a card",
    description="Change international_allowed and allowed_countries fields.",
    tags=["card_controls"],
    operation_id="update_card_controls",
)
async def update_card_controls(
    card_id: int = Path(..., description="cards.id whose controls to update", example=301),
    payload: CardControlUpdateRequest = Body(...),
) -> CardControlResponse:
    session = SessionLocal()
    controls = session.query(CardControl).filter(CardControl.card_id == card_id).first()
    now = datetime.utcnow()
    if controls is not None:
        card = session.query(Card).filter(Card.id == card_id).first()
        if card is not None:
            account = session.query(Account).filter(Account.id == card.account_id).first()
            if account is not None:
                customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
                if customer is not None:
                    if payload.international_allowed is not None:
                        controls.international_allowed = payload.international_allowed
                    if payload.allowed_countries is not None:
                        controls.allowed_countries = payload.allowed_countries
                    controls.updated_at = now
                    session.commit()
    if controls is None:
        controls = CardControl(
            card_id=card_id,
            international_allowed=payload.international_allowed if payload.international_allowed is not None else 1,
            allowed_countries=payload.allowed_countries,
            created_at=now,
            updated_at=now,
        )
        session.add(controls)
        session.commit()
    model = CardControlModel(
        id=controls.id,
        card_id=controls.card_id,
        international_allowed=bool(controls.international_allowed),
        allowed_countries=controls.allowed_countries,
        created_at=datetime_to_iso(controls.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(controls.updated_at) or now_utc_iso(),
    )
    session.close()
    return CardControlResponse(card_controls=model)


@app.post(
    "/api/payees",
    response_model=PayeeResponse,
    summary="Create a new payee for current user",
    description="Create a payees row for the current user.",
    tags=["payees"],
    operation_id="create_payee_for_current_user",
)
async def create_payee_for_current_user(payload: PayeeCreateRequest = Body(...)) -> PayeeResponse:
    session = SessionLocal()
    now = datetime.utcnow()
    payee = Payee(
        user_id=1,
        name=payload.name,
        category=payload.category,
        default_memo=payload.default_memo,
        created_at=now,
        updated_at=now,
    )
    session.add(payee)
    session.commit()
    model = PayeeModel(
        id=payee.id,
        user_id=payee.user_id,
        name=payee.name,
        category=payee.category,
        default_memo=payee.default_memo,
        created_at=datetime_to_iso(payee.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(payee.updated_at) or now_utc_iso(),
    )
    session.close()
    return PayeeResponse(payee=model)


@app.post(
    "/api/payees/{payee_id}/routing-info",
    response_model=PayeeRoutingInfoResponse,
    summary="Create routing info for a payee",
    description="Create payee_routing_info row for a given payee.",
    tags=["payees"],
    operation_id="create_payee_routing_info",
)
async def create_payee_routing_info(
    payee_id: int = Path(..., description="payees.id for which to add routing info", example=501),
    payload: PayeeRoutingInfoCreateRequest = Body(...),
) -> PayeeRoutingInfoResponse:
    session = SessionLocal()
    payee = session.query(Payee).filter(Payee.id == payee_id, Payee.user_id == 1).first()
    now = datetime.utcnow()
    if payee is None:
        routing = PayeeRoutingInfo(
            payee_id=0,
            bank_name=payload.bank_name,
            routing_number=payload.routing_number,
            account_number=payload.account_number,
            created_at=now,
            updated_at=now,
        )
        session.add(routing)
        session.commit()
    else:
        routing = PayeeRoutingInfo(
            payee_id=payee.id,
            bank_name=payload.bank_name,
            routing_number=payload.routing_number,
            account_number=payload.account_number,
            created_at=now,
            updated_at=now,
        )
        session.add(routing)
        session.commit()
    model = PayeeRoutingInfoModel(
        id=routing.id,
        payee_id=routing.payee_id,
        bank_name=routing.bank_name,
        routing_number=routing.routing_number,
        account_number=routing.account_number,
        created_at=datetime_to_iso(routing.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(routing.updated_at) or now_utc_iso(),
    )
    session.close()
    return PayeeRoutingInfoResponse(routing_info=model)


@app.get(
    "/api/payees",
    response_model=PayeesListResponse,
    summary="List all payees for current user",
    description="Retrieve all payees belonging to current user, with filters.",
    tags=["payees"],
    operation_id="list_payees_for_current_user",
)
async def list_payees_for_current_user(
    name: Optional[str] = Query(None, description="Optional substring filter on payee name", example="Downtown"),
    category: Optional[str] = Query(None, description="Optional filter by category", example="utilities"),
) -> PayeesListResponse:
    session = SessionLocal()
    query = session.query(Payee).filter(Payee.user_id == 1)
    if name is not None:
        query = query.filter(Payee.name.contains(name))
    if category is not None:
        query = query.filter(Payee.category == category)
    payees = query.all()
    result: List[PayeeModel] = []
    for p in payees:
        result.append(
            PayeeModel(
                id=p.id,
                user_id=p.user_id,
                name=p.name,
                category=p.category,
                default_memo=p.default_memo,
                created_at=datetime_to_iso(p.created_at) or now_utc_iso(),
                updated_at=datetime_to_iso(p.updated_at) or now_utc_iso(),
            )
        )
    session.close()
    return PayeesListResponse(payees=result)


@app.post(
    "/api/scheduled-transfers",
    response_model=ScheduledTransferResponse,
    summary="Create a new scheduled transfer",
    description="Create scheduled_transfers row for internal or external transfers.",
    tags=["scheduled_transfers"],
    operation_id="create_scheduled_transfer",
)
async def create_scheduled_transfer(payload: ScheduledTransferCreateRequest = Body(...)) -> ScheduledTransferResponse:
    session = SessionLocal()
    from_account = session.query(Account).filter(Account.id == payload.from_account_id).first()
    now = datetime.utcnow()
    next_run = payload.start_date
    to_account_id_value = payload.to_account_id
    payee_id_value = payload.payee_id
    if from_account is None:
        scheduled = ScheduledTransfer(
            user_id=1,
            from_account_id=0,
            to_account_id=to_account_id_value,
            payee_id=payee_id_value,
            transfer_type=payload.transfer_type,
            amount=payload.amount,
            currency=payload.currency,
            schedule_type=payload.schedule_type,
            recurrence_rule=payload.recurrence_rule,
            start_date=payload.start_date,
            end_date=payload.end_date,
            next_run_date=next_run,
            state="scheduled",
            tag=payload.tag,
            memo=payload.memo,
            created_at=now,
            updated_at=now,
        )
        session.add(scheduled)
        session.commit()
    else:
        customer = session.query(Customer).filter(Customer.id == from_account.customer_id, Customer.user_id == 1).first()
        if customer is None:
            scheduled = ScheduledTransfer(
                user_id=1,
                from_account_id=0,
                to_account_id=to_account_id_value,
                payee_id=payee_id_value,
                transfer_type=payload.transfer_type,
                amount=payload.amount,
                currency=payload.currency,
                schedule_type=payload.schedule_type,
                recurrence_rule=payload.recurrence_rule,
                start_date=payload.start_date,
                end_date=payload.end_date,
                next_run_date=next_run,
                state="scheduled",
                tag=payload.tag,
                memo=payload.memo,
                created_at=now,
                updated_at=now,
            )
            session.add(scheduled)
            session.commit()
        else:
            scheduled = ScheduledTransfer(
                user_id=1,
                from_account_id=from_account.id,
                to_account_id=to_account_id_value,
                payee_id=payee_id_value,
                transfer_type=payload.transfer_type,
                amount=payload.amount,
                currency=payload.currency,
                schedule_type=payload.schedule_type,
                recurrence_rule=payload.recurrence_rule,
                start_date=payload.start_date,
                end_date=payload.end_date,
                next_run_date=next_run,
                state="scheduled",
                tag=payload.tag,
                memo=payload.memo,
                created_at=now,
                updated_at=now,
            )
            session.add(scheduled)
            session.commit()
    model = ScheduledTransferModel(
        id=scheduled.id,
        user_id=scheduled.user_id,
        from_account_id=scheduled.from_account_id,
        to_account_id=scheduled.to_account_id,
        payee_id=scheduled.payee_id,
        transfer_type=scheduled.transfer_type,
        amount=scheduled.amount,
        currency=scheduled.currency,
        schedule_type=scheduled.schedule_type,
        recurrence_rule=scheduled.recurrence_rule,
        start_date=scheduled.start_date,
        end_date=scheduled.end_date,
        next_run_date=scheduled.next_run_date,
        state=scheduled.state,
        tag=scheduled.tag,
        memo=scheduled.memo,
        created_at=datetime_to_iso(scheduled.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(scheduled.updated_at) or now_utc_iso(),
    )
    session.close()
    return ScheduledTransferResponse(scheduled_transfer=model)


@app.get(
    "/api/scheduled-transfers/{scheduled_transfer_id}",
    response_model=ScheduledTransferResponse,
    summary="Get scheduled transfer by ID",
    description="Retrieve one scheduled_transfers row for current user by its ID.",
    tags=["scheduled_transfers"],
    operation_id="get_scheduled_transfer_by_id",
)
async def get_scheduled_transfer_by_id(
    scheduled_transfer_id: int = Path(..., description="scheduled_transfers.id to fetch", example=701)
) -> ScheduledTransferResponse:
    session = SessionLocal()
    scheduled = session.query(ScheduledTransfer).filter(ScheduledTransfer.id == scheduled_transfer_id, ScheduledTransfer.user_id == 1).first()
    if scheduled is None:
        now_str = now_utc_iso()
        empty = ScheduledTransferModel(
            id=0,
            user_id=1,
            from_account_id=0,
            to_account_id=None,
            payee_id=None,
            transfer_type="internal",
            amount=0.0,
            currency="USD",
            schedule_type="one_time",
            recurrence_rule=None,
            start_date=date.today().isoformat(),
            end_date=None,
            next_run_date=None,
            state="scheduled",
            tag=None,
            memo=None,
            created_at=now_str,
            updated_at=now_str,
        )
        session.close()
        return ScheduledTransferResponse(scheduled_transfer=empty)
    model = ScheduledTransferModel(
        id=scheduled.id,
        user_id=scheduled.user_id,
        from_account_id=scheduled.from_account_id,
        to_account_id=scheduled.to_account_id,
        payee_id=scheduled.payee_id,
        transfer_type=scheduled.transfer_type,
        amount=scheduled.amount,
        currency=scheduled.currency,
        schedule_type=scheduled.schedule_type,
        recurrence_rule=scheduled.recurrence_rule,
        start_date=scheduled.start_date,
        end_date=scheduled.end_date,
        next_run_date=scheduled.next_run_date,
        state=scheduled.state,
        tag=scheduled.tag,
        memo=scheduled.memo,
        created_at=datetime_to_iso(scheduled.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(scheduled.updated_at) or now_utc_iso(),
    )
    session.close()
    return ScheduledTransferResponse(scheduled_transfer=model)


@app.post(
    "/api/transfers",
    response_model=TransferCreateResponse,
    summary="Create an immediate transfer",
    description="Create transfers row and optionally update balances atomically.",
    tags=["transfers"],
    operation_id="create_immediate_transfer",
)
async def create_immediate_transfer(payload: TransferCreateRequest = Body(...)) -> TransferCreateResponse:
    session = SessionLocal()
    now = datetime.utcnow()
    from_account = session.query(Account).filter(Account.id == payload.from_account_id).first()
    customer_valid = False
    if from_account is not None:
        customer = session.query(Customer).filter(Customer.id == from_account.customer_id, Customer.user_id == 1).first()
        if customer is not None:
            customer_valid = True
    to_account = None
    if payload.to_account_id is not None:
        to_account = session.query(Account).filter(Account.id == payload.to_account_id).first()
    if not customer_valid:
        transfer = Transfer(
            scheduled_transfer_id=payload.scheduled_transfer_id,
            user_id=1,
            from_account_id=0,
            to_account_id=payload.to_account_id,
            payee_id=payload.payee_id,
            transfer_type=payload.transfer_type,
            amount=payload.amount,
            currency=payload.currency,
            state="failed",
            failure_reason="invalid_source_account",
            executed_at=now,
            created_at=now,
            updated_at=now,
        )
        session.add(transfer)
        session.commit()
        transfer_model = TransferModel(
            id=transfer.id,
            scheduled_transfer_id=transfer.scheduled_transfer_id,
            user_id=transfer.user_id,
            from_account_id=transfer.from_account_id,
            to_account_id=transfer.to_account_id,
            payee_id=transfer.payee_id,
            transfer_type=transfer.transfer_type,
            amount=transfer.amount,
            currency=transfer.currency,
            state=transfer.state,
            failure_reason=transfer.failure_reason,
            executed_at=datetime_to_iso(transfer.executed_at),
            created_at=datetime_to_iso(transfer.created_at) or now_utc_iso(),
            updated_at=datetime_to_iso(transfer.updated_at) or now_utc_iso(),
        )
        updated_accounts: List[UpdatedAccountBalanceModel] = []
        session.close()
        return TransferCreateResponse(transfer=transfer_model, updated_accounts=updated_accounts)
    from_account.current_balance = from_account.current_balance - payload.amount
    updated_accounts: List[UpdatedAccountBalanceModel] = []
    updated_accounts.append(
        UpdatedAccountBalanceModel(
            id=from_account.id,
            current_balance=from_account.current_balance,
            currency=from_account.currency,
        )
    )
    if payload.transfer_type == "internal" and to_account is not None:
        to_account.current_balance = to_account.current_balance + payload.amount
        updated_accounts.append(
            UpdatedAccountBalanceModel(
                id=to_account.id,
                current_balance=to_account.current_balance,
                currency=to_account.currency,
            )
        )
    transfer = Transfer(
        scheduled_transfer_id=payload.scheduled_transfer_id,
        user_id=1,
        from_account_id=from_account.id,
        to_account_id=to_account.id if to_account is not None else None,
        payee_id=payload.payee_id,
        transfer_type=payload.transfer_type,
        amount=payload.amount,
        currency=payload.currency,
        state="completed",
        failure_reason=None,
        executed_at=now,
        created_at=now,
        updated_at=now,
    )
    session.add(transfer)
    session.commit()
    transfer_model = TransferModel(
        id=transfer.id,
        scheduled_transfer_id=transfer.scheduled_transfer_id,
        user_id=transfer.user_id,
        from_account_id=transfer.from_account_id,
        to_account_id=transfer.to_account_id,
        payee_id=transfer.payee_id,
        transfer_type=transfer.transfer_type,
        amount=transfer.amount,
        currency=transfer.currency,
        state=transfer.state,
        failure_reason=transfer.failure_reason,
        executed_at=datetime_to_iso(transfer.executed_at),
        created_at=datetime_to_iso(transfer.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(transfer.updated_at) or now_utc_iso(),
    )
    session.close()
    return TransferCreateResponse(transfer=transfer_model, updated_accounts=updated_accounts)


@app.get(
    "/api/transfers/{transfer_id}",
    response_model=TransferResponse,
    summary="Get transfer by ID",
    description="Retrieve a transfers row belonging to the current user by its ID.",
    tags=["transfers"],
    operation_id="get_transfer_by_id",
)
async def get_transfer_by_id(
    transfer_id: int = Path(..., description="transfers.id to retrieve", example=801)
) -> TransferResponse:
    session = SessionLocal()
    transfer = session.query(Transfer).filter(Transfer.id == transfer_id, Transfer.user_id == 1).first()
    if transfer is None:
        now_str = now_utc_iso()
        empty = TransferModel(
            id=0,
            scheduled_transfer_id=None,
            user_id=1,
            from_account_id=0,
            to_account_id=None,
            payee_id=None,
            transfer_type="internal",
            amount=0.0,
            currency="USD",
            state="failed",
            failure_reason="not_found",
            executed_at=now_str,
            created_at=now_str,
            updated_at=now_str,
        )
        session.close()
        return TransferResponse(transfer=empty)
    model = TransferModel(
        id=transfer.id,
        scheduled_transfer_id=transfer.scheduled_transfer_id,
        user_id=transfer.user_id,
        from_account_id=transfer.from_account_id,
        to_account_id=transfer.to_account_id,
        payee_id=transfer.payee_id,
        transfer_type=transfer.transfer_type,
        amount=transfer.amount,
        currency=transfer.currency,
        state=transfer.state,
        failure_reason=transfer.failure_reason,
        executed_at=datetime_to_iso(transfer.executed_at),
        created_at=datetime_to_iso(transfer.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(transfer.updated_at) or now_utc_iso(),
    )
    session.close()
    return TransferResponse(transfer=model)


@app.get(
    "/api/transactions",
    response_model=TransactionsListResponse,
    summary="List account transactions with filters",
    description="Retrieve transactions for an account with optional filters.",
    tags=["transactions"],
    operation_id="list_transactions_for_account",
)
async def list_transactions_for_account(
    account_id: int = Query(..., description="accounts.id whose transactions to list", example=101),
    start_date: Optional[str] = Query(None, description="Posted_at start date in YYYY-MM-DD", example="2026-01-01"),
    end_date: Optional[str] = Query(None, description="Posted_at end date in YYYY-MM-DD", example="2026-01-31"),
    card_only: Optional[bool] = Query(False, description="If true, only card transactions", example=True),
    merchant_search: Optional[str] = Query(None, description="Substring to match in merchant_metadata", example="GROCERY"),
) -> TransactionsListResponse:
    session = SessionLocal()
    account = session.query(Account).filter(Account.id == account_id).first()
    if account is None:
        session.close()
        return TransactionsListResponse(transactions=[])
    customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
    if customer is None:
        session.close()
        return TransactionsListResponse(transactions=[])
    query = session.query(Transaction).filter(Transaction.account_id == account_id)
    if start_date is not None:
        start_dt = datetime.fromisoformat(start_date + "T00:00:00")
        query = query.filter(Transaction.posted_at >= start_dt)
    if end_date is not None:
        end_dt = datetime.fromisoformat(end_date + "T23:59:59")
        query = query.filter(Transaction.posted_at <= end_dt)
    if card_only:
        query = query.filter(Transaction.card_id.isnot(None))
    if merchant_search is not None:
        query = query.filter(Transaction.merchant_metadata.contains(merchant_search))
    txs = query.all()
    result: List[TransactionModel] = []
    for t in txs:
        result.append(
            TransactionModel(
                id=t.id,
                account_id=t.account_id,
                transfer_id=t.transfer_id,
                card_id=t.card_id,
                type=t.type,
                amount=t.amount,
                currency=t.currency,
                description=t.description,
                merchant_metadata=t.merchant_metadata,
                posted_at=datetime_to_iso(t.posted_at),
                created_at=datetime_to_iso(t.created_at) or now_utc_iso(),
                updated_at=datetime_to_iso(t.updated_at) or now_utc_iso(),
            )
        )
    session.close()
    return TransactionsListResponse(transactions=result)


@app.post(
    "/api/transaction-tags",
    response_model=TransactionTagResponse,
    summary="Add a tag to a transaction",
    description="Create transaction_tags row to tag a transaction for the current user.",
    tags=["transaction_tags"],
    operation_id="add_tag_to_transaction",
)
async def add_tag_to_transaction(payload: TransactionTagCreateRequest = Body(...)) -> TransactionTagResponse:
    session = SessionLocal()
    tx = session.query(Transaction).filter(Transaction.id == payload.transaction_id).first()
    now = datetime.utcnow()
    if tx is None:
        tag_row = TransactionTag(
            transaction_id=0,
            tag=payload.tag,
            created_at=now,
            updated_at=now,
        )
        session.add(tag_row)
        session.commit()
        model = TransactionTagModel(
            id=tag_row.id,
            transaction_id=tag_row.transaction_id,
            tag=tag_row.tag,
            created_at=datetime_to_iso(tag_row.created_at) or now_utc_iso(),
            updated_at=datetime_to_iso(tag_row.updated_at) or now_utc_iso(),
        )
        session.close()
        return TransactionTagResponse(transaction_tag=model)
    account = session.query(Account).filter(Account.id == tx.account_id).first()
    if account is None:
        tag_row = TransactionTag(
            transaction_id=0,
            tag=payload.tag,
            created_at=now,
            updated_at=now,
        )
        session.add(tag_row)
        session.commit()
        model = TransactionTagModel(
            id=tag_row.id,
            transaction_id=tag_row.transaction_id,
            tag=tag_row.tag,
            created_at=datetime_to_iso(tag_row.created_at) or now_utc_iso(),
            updated_at=datetime_to_iso(tag_row.updated_at) or now_utc_iso(),
        )
        session.close()
        return TransactionTagResponse(transaction_tag=model)
    customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
    if customer is None:
        tag_row = TransactionTag(
            transaction_id=0,
            tag=payload.tag,
            created_at=now,
            updated_at=now,
        )
        session.add(tag_row)
        session.commit()
        model = TransactionTagModel(
            id=tag_row.id,
            transaction_id=tag_row.transaction_id,
            tag=tag_row.tag,
            created_at=datetime_to_iso(tag_row.created_at) or now_utc_iso(),
            updated_at=datetime_to_iso(tag_row.updated_at) or now_utc_iso(),
        )
        session.close()
        return TransactionTagResponse(transaction_tag=model)
    existing = session.query(TransactionTag).filter(TransactionTag.transaction_id == tx.id, TransactionTag.tag == payload.tag).first()
    if existing is not None:
        model = TransactionTagModel(
            id=existing.id,
            transaction_id=existing.transaction_id,
            tag=existing.tag,
            created_at=datetime_to_iso(existing.created_at) or now_utc_iso(),
            updated_at=datetime_to_iso(existing.updated_at) or now_utc_iso(),
        )
        session.close()
        return TransactionTagResponse(transaction_tag=model)
    tag_row = TransactionTag(
        transaction_id=tx.id,
        tag=payload.tag,
        created_at=now,
        updated_at=now,
    )
    session.add(tag_row)
    session.commit()
    model = TransactionTagModel(
        id=tag_row.id,
        transaction_id=tag_row.transaction_id,
        tag=tag_row.tag,
        created_at=datetime_to_iso(tag_row.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(tag_row.updated_at) or now_utc_iso(),
    )
    session.close()
    return TransactionTagResponse(transaction_tag=model)


@app.get(
    "/api/transaction-tags",
    response_model=TransactionTagsListResponse,
    summary="List tags for a transaction",
    description="Retrieve all transaction_tags rows for a given transaction.",
    tags=["transaction_tags"],
    operation_id="list_tags_for_transaction",
)
async def list_tags_for_transaction(
    transaction_id: int = Query(..., description="transactions.id whose tags to list", example=901)
) -> TransactionTagsListResponse:
    session = SessionLocal()
    tx = session.query(Transaction).filter(Transaction.id == transaction_id).first()
    if tx is None:
        session.close()
        return TransactionTagsListResponse(tags=[])
    account = session.query(Account).filter(Account.id == tx.account_id).first()
    if account is None:
        session.close()
        return TransactionTagsListResponse(tags=[])
    customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
    if customer is None:
        session.close()
        return TransactionTagsListResponse(tags=[])
    tags_rows = session.query(TransactionTag).filter(TransactionTag.transaction_id == transaction_id).all()
    result: List[TransactionTagModel] = []
    for row in tags_rows:
        result.append(
            TransactionTagModel(
                id=row.id,
                transaction_id=row.transaction_id,
                tag=row.tag,
                created_at=datetime_to_iso(row.created_at) or now_utc_iso(),
                updated_at=datetime_to_iso(row.updated_at) or now_utc_iso(),
            )
        )
    session.close()
    return TransactionTagsListResponse(tags=result)


@app.post(
    "/api/alert-preferences",
    response_model=AlertPreferenceResponse,
    summary="Create alert preference for an account",
    description="Create an alert_preferences row for the given account and type.",
    tags=["alert_preferences"],
    operation_id="create_alert_preference",
)
async def create_alert_preference(payload: AlertPreferenceCreateRequest = Body(...)) -> AlertPreferenceResponse:
    session = SessionLocal()
    account = session.query(Account).filter(Account.id == payload.account_id).first()
    now = datetime.utcnow()
    channel_email_value = payload.channel_email if payload.channel_email is not None else 0
    channel_push_value = payload.channel_push if payload.channel_push is not None else 0
    channel_sms_value = payload.channel_sms if payload.channel_sms is not None else 0
    is_enabled_value = payload.is_enabled if payload.is_enabled is not None else 1
    if account is None:
        pref = AlertPreference(
            account_id=0,
            alert_type=payload.alert_type,
            threshold_amount=payload.threshold_amount,
            channel_email=channel_email_value,
            channel_push=channel_push_value,
            channel_sms=channel_sms_value,
            is_enabled=is_enabled_value,
            created_at=now,
            updated_at=now,
        )
        session.add(pref)
        session.commit()
    else:
        customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
        if customer is None:
            pref = AlertPreference(
                account_id=0,
                alert_type=payload.alert_type,
                threshold_amount=payload.threshold_amount,
                channel_email=channel_email_value,
                channel_push=channel_push_value,
                channel_sms=channel_sms_value,
                is_enabled=is_enabled_value,
                created_at=now,
                updated_at=now,
            )
            session.add(pref)
            session.commit()
        else:
            existing = session.query(AlertPreference).filter(AlertPreference.account_id == account.id, AlertPreference.alert_type == payload.alert_type).first()
            if existing is None:
                pref = AlertPreference(
                    account_id=account.id,
                    alert_type=payload.alert_type,
                    threshold_amount=payload.threshold_amount,
                    channel_email=channel_email_value,
                    channel_push=channel_push_value,
                    channel_sms=channel_sms_value,
                    is_enabled=is_enabled_value,
                    created_at=now,
                    updated_at=now,
                )
                session.add(pref)
                session.commit()
            else:
                pref = existing
                pref.threshold_amount = payload.threshold_amount
                pref.channel_email = channel_email_value
                pref.channel_push = channel_push_value
                pref.channel_sms = channel_sms_value
                pref.is_enabled = is_enabled_value
                pref.updated_at = now
                session.commit()
    model = AlertPreferenceModel(
        id=pref.id,
        account_id=pref.account_id,
        alert_type=pref.alert_type,
        threshold_amount=pref.threshold_amount,
        channel_email=bool(pref.channel_email),
        channel_push=bool(pref.channel_push),
        channel_sms=bool(pref.channel_sms),
        is_enabled=bool(pref.is_enabled),
        created_at=datetime_to_iso(pref.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(pref.updated_at) or now_utc_iso(),
    )
    session.close()
    return AlertPreferenceResponse(alert_preference=model)


@app.patch(
    "/api/alert-preferences/{alert_preference_id}",
    response_model=AlertPreferenceResponse,
    summary="Update an alert preference",
    description="Update threshold and channels for an existing alert_preferences row.",
    tags=["alert_preferences"],
    operation_id="update_alert_preference",
)
async def update_alert_preference(
    alert_preference_id: int = Path(..., description="alert_preferences.id to update", example=1101),
    payload: AlertPreferenceUpdateRequest = Body(...),
) -> AlertPreferenceResponse:
    session = SessionLocal()
    pref = session.query(AlertPreference).filter(AlertPreference.id == alert_preference_id).first()
    now = datetime.utcnow()
    if pref is not None:
        account = session.query(Account).filter(Account.id == pref.account_id).first()
        if account is not None:
            customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
            if customer is not None:
                if payload.threshold_amount is not None:
                    pref.threshold_amount = payload.threshold_amount
                if payload.channel_email is not None:
                    pref.channel_email = payload.channel_email
                if payload.channel_push is not None:
                    pref.channel_push = payload.channel_push
                if payload.channel_sms is not None:
                    pref.channel_sms = payload.channel_sms
                if payload.is_enabled is not None:
                    pref.is_enabled = payload.is_enabled
                pref.updated_at = now
                session.commit()
    if pref is None:
        pref = AlertPreference(
            account_id=0,
            alert_type="low_balance",
            threshold_amount=0.0,
            channel_email=0,
            channel_push=0,
            channel_sms=0,
            is_enabled=1,
            created_at=now,
            updated_at=now,
        )
        session.add(pref)
        session.commit()
    model = AlertPreferenceModel(
        id=pref.id,
        account_id=pref.account_id,
        alert_type=pref.alert_type,
        threshold_amount=pref.threshold_amount,
        channel_email=bool(pref.channel_email),
        channel_push=bool(pref.channel_push),
        channel_sms=bool(pref.channel_sms),
        is_enabled=bool(pref.is_enabled),
        created_at=datetime_to_iso(pref.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(pref.updated_at) or now_utc_iso(),
    )
    session.close()
    return AlertPreferenceResponse(alert_preference=model)


@app.get(
    "/api/alert-preferences/by-account/{account_id}",
    response_model=AlertPreferencesListResponse,
    summary="List alert preferences for an account",
    description="Retrieve all alert_preferences rows for a specific account.",
    tags=["alert_preferences"],
    operation_id="list_alert_preferences_for_account",
)
async def list_alert_preferences_for_account(
    account_id: int = Path(..., description="accounts.id whose alert preferences to list", example=101)
) -> AlertPreferencesListResponse:
    session = SessionLocal()
    account = session.query(Account).filter(Account.id == account_id).first()
    if account is None:
        session.close()
        return AlertPreferencesListResponse(alert_preferences=[])
    customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
    if customer is None:
        session.close()
        return AlertPreferencesListResponse(alert_preferences=[])
    prefs = session.query(AlertPreference).filter(AlertPreference.account_id == account_id).all()
    result: List[AlertPreferenceModel] = []
    for pref in prefs:
        result.append(
            AlertPreferenceModel(
                id=pref.id,
                account_id=pref.account_id,
                alert_type=pref.alert_type,
                threshold_amount=pref.threshold_amount,
                channel_email=bool(pref.channel_email),
                channel_push=bool(pref.channel_push),
                channel_sms=bool(pref.channel_sms),
                is_enabled=bool(pref.is_enabled),
                created_at=datetime_to_iso(pref.created_at) or now_utc_iso(),
                updated_at=datetime_to_iso(pref.updated_at) or now_utc_iso(),
            )
        )
    session.close()
    return AlertPreferencesListResponse(alert_preferences=result)


@app.get(
    "/api/card-holds/by-account/{account_id}",
    response_model=CardHoldsListResponse,
    summary="List active holds for an account",
    description="Retrieve all card_holds with state=authorized for a given account.",
    tags=["card_holds"],
    operation_id="list_authorized_holds_for_account",
)
async def list_authorized_holds_for_account(
    account_id: int = Path(..., description="accounts.id whose authorized holds to list", example=101),
    min_amount: Optional[float] = Query(None, description="Optional minimum hold amount filter", example=200.0),
) -> CardHoldsListResponse:
    session = SessionLocal()
    account = session.query(Account).filter(Account.id == account_id).first()
    if account is None:
        session.close()
        return CardHoldsListResponse(holds=[])
    customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
    if customer is None:
        session.close()
        return CardHoldsListResponse(holds=[])
    query = session.query(CardHold).filter(CardHold.account_id == account_id, CardHold.state == "authorized")
    if min_amount is not None:
        query = query.filter(CardHold.amount >= min_amount)
    holds = query.all()
    result: List[CardHoldModel] = []
    for h in holds:
        result.append(
            CardHoldModel(
                id=h.id,
                card_id=h.card_id,
                account_id=h.account_id,
                amount=h.amount,
                currency=h.currency,
                merchant_metadata=h.merchant_metadata,
                state=h.state,
                authorized_at=datetime_to_iso(h.authorized_at) or now_utc_iso(),
                captured_at=datetime_to_iso(h.captured_at),
                released_at=datetime_to_iso(h.released_at),
                created_at=datetime_to_iso(h.created_at) or now_utc_iso(),
                updated_at=datetime_to_iso(h.updated_at) or now_utc_iso(),
            )
        )
    session.close()
    return CardHoldsListResponse(holds=result)


@app.get(
    "/api/card-holds/summary/by-account/{account_id}",
    response_model=CardHoldsSummaryResponse,
    summary="Summarize large holds for an account",
    description="Return simplified list of holds above min_amount.",
    tags=["card_holds"],
    operation_id="summarize_large_holds_for_account",
)
async def summarize_large_holds_for_account(
    account_id: int = Path(..., description="accounts.id whose holds summary to return", example=101),
    min_amount: float = Query(..., description="Minimum hold amount to include in the summary", example=200.0),
) -> CardHoldsSummaryResponse:
    session = SessionLocal()
    account = session.query(Account).filter(Account.id == account_id).first()
    if account is None:
        session.close()
        return CardHoldsSummaryResponse(holds_summary=[])
    customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
    if customer is None:
        session.close()
        return CardHoldsSummaryResponse(holds_summary=[])
    holds = (
        session.query(CardHold)
        .filter(CardHold.account_id == account_id, CardHold.state == "authorized", CardHold.amount >= min_amount)
        .all()
    )
    result: List[CardHoldSummaryModel] = []
    for h in holds:
        result.append(
            CardHoldSummaryModel(
                card_id=h.card_id,
                amount=h.amount,
                currency=h.currency,
                merchant_metadata=h.merchant_metadata,
                authorized_at=datetime_to_iso(h.authorized_at) or now_utc_iso(),
            )
        )
    session.close()
    return CardHoldsSummaryResponse(holds_summary=result)


@app.post(
    "/api/direct-deposit-configs",
    response_model=DirectDepositConfigResponse,
    summary="Create or upsert direct deposit config",
    description="Create direct_deposit_configs row or update existing metadata.",
    tags=["direct_deposit"],
    operation_id="create_or_update_direct_deposit_config",
)
async def create_or_update_direct_deposit_config(
    payload: DirectDepositConfigCreateRequest = Body(...),
) -> DirectDepositConfigResponse:
    session = SessionLocal()
    now = datetime.utcnow()
    existing = session.query(DirectDepositConfig).filter(
        DirectDepositConfig.user_id == 1, DirectDepositConfig.employer_id == payload.employer_id
    ).first()
    if existing is None:
        cfg = DirectDepositConfig(
            user_id=1,
            employer_id=payload.employer_id,
            employer_name=payload.employer_name,
            allocation_type=payload.allocation_type or "percentage",
            is_active=payload.is_active if payload.is_active is not None else 1,
            created_at=now,
            updated_at=now,
        )
        session.add(cfg)
        session.commit()
    else:
        cfg = existing
        if payload.employer_name is not None:
            cfg.employer_name = payload.employer_name
        if payload.allocation_type is not None:
            cfg.allocation_type = payload.allocation_type
        if payload.is_active is not None:
            cfg.is_active = payload.is_active
        cfg.updated_at = now
        session.commit()
    model = DirectDepositConfigModel(
        id=cfg.id,
        user_id=cfg.user_id,
        employer_id=cfg.employer_id,
        employer_name=cfg.employer_name,
        allocation_type=cfg.allocation_type,
        is_active=bool(cfg.is_active),
        created_at=datetime_to_iso(cfg.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(cfg.updated_at) or now_utc_iso(),
    )
    session.close()
    return DirectDepositConfigResponse(direct_deposit_config=model)


@app.post(
    "/api/direct-deposit-allocations",
    response_model=DirectDepositAllocationResponse,
    summary="Create allocation for a direct deposit config",
    description="Create direct_deposit_allocations row mapping portion of deposits.",
    tags=["direct_deposit"],
    operation_id="create_direct_deposit_allocation",
)
async def create_direct_deposit_allocation(
    payload: DirectDepositAllocationCreateRequest = Body(...),
) -> DirectDepositAllocationResponse:
    session = SessionLocal()
    cfg = session.query(DirectDepositConfig).filter(
        DirectDepositConfig.id == payload.direct_deposit_config_id, DirectDepositConfig.user_id == 1
    ).first()
    account = session.query(Account).filter(Account.id == payload.account_id).first()
    now = datetime.utcnow()
    if cfg is None or account is None:
        alloc = DirectDepositAllocation(
            direct_deposit_config_id=0,
            account_id=0,
            percentage=payload.percentage,
            created_at=now,
            updated_at=now,
        )
        session.add(alloc)
        session.commit()
    else:
        customer = session.query(Customer).filter(Customer.id == account.customer_id, Customer.user_id == 1).first()
        if customer is None:
            alloc = DirectDepositAllocation(
                direct_deposit_config_id=0,
                account_id=0,
                percentage=payload.percentage,
                created_at=now,
                updated_at=now,
            )
            session.add(alloc)
            session.commit()
        else:
            alloc = DirectDepositAllocation(
                direct_deposit_config_id=cfg.id,
                account_id=account.id,
                percentage=payload.percentage,
                created_at=now,
                updated_at=now,
            )
            session.add(alloc)
            session.commit()
    model = DirectDepositAllocationModel(
        id=alloc.id,
        direct_deposit_config_id=alloc.direct_deposit_config_id,
        account_id=alloc.account_id,
        percentage=alloc.percentage,
        created_at=datetime_to_iso(alloc.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(alloc.updated_at) or now_utc_iso(),
    )
    session.close()
    return DirectDepositAllocationResponse(direct_deposit_allocation=model)


@app.get(
    "/api/direct-deposit-allocations/by-config/{direct_deposit_config_id}",
    response_model=DirectDepositAllocationsListResponse,
    summary="List allocations for a direct deposit config",
    description="Retrieve all direct_deposit_allocations for a given config.",
    tags=["direct_deposit"],
    operation_id="list_direct_deposit_allocations_for_config",
)
async def list_direct_deposit_allocations_for_config(
    direct_deposit_config_id: int = Path(..., description="direct_deposit_configs.id whose allocations to list", example=1301)
) -> DirectDepositAllocationsListResponse:
    session = SessionLocal()
    cfg = session.query(DirectDepositConfig).filter(
        DirectDepositConfig.id == direct_deposit_config_id, DirectDepositConfig.user_id == 1
    ).first()
    if cfg is None:
        session.close()
        return DirectDepositAllocationsListResponse(allocations=[])
    allocs = session.query(DirectDepositAllocation).filter(
        DirectDepositAllocation.direct_deposit_config_id == cfg.id
    ).all()
    result: List[DirectDepositAllocationModel] = []
    for alloc in allocs:
        result.append(
            DirectDepositAllocationModel(
                id=alloc.id,
                direct_deposit_config_id=alloc.direct_deposit_config_id,
                account_id=alloc.account_id,
                percentage=alloc.percentage,
                created_at=datetime_to_iso(alloc.created_at) or now_utc_iso(),
                updated_at=datetime_to_iso(alloc.updated_at) or now_utc_iso(),
            )
        )
    session.close()
    return DirectDepositAllocationsListResponse(allocations=result)


@app.get(
    "/api/direct-deposit-configs/by-employer/{employer_id}",
    response_model=DirectDepositSetupResponse,
    summary="Get direct deposit config and allocations by employer",
    description="Retrieve direct_deposit_configs and allocations for an employer_id.",
    tags=["direct_deposit"],
    operation_id="get_direct_deposit_setup_for_employer",
)
async def get_direct_deposit_setup_for_employer(
    employer_id: str = Path(..., description="Employer identifier to filter config", example="ACME-001")
) -> DirectDepositSetupResponse:
    session = SessionLocal()
    cfg = session.query(DirectDepositConfig).filter(
        DirectDepositConfig.user_id == 1, DirectDepositConfig.employer_id == employer_id
    ).first()
    if cfg is None:
        now_str = now_utc_iso()
        empty_cfg = DirectDepositConfigModel(
            id=0,
            user_id=1,
            employer_id=employer_id,
            employer_name=None,
            allocation_type="percentage",
            is_active=False,
            created_at=now_str,
            updated_at=now_str,
        )
        session.close()
        return DirectDepositSetupResponse(direct_deposit_config=empty_cfg, allocations=[])
    allocs = session.query(DirectDepositAllocation).filter(
        DirectDepositAllocation.direct_deposit_config_id == cfg.id
    ).all()
    model_cfg = DirectDepositConfigModel(
        id=cfg.id,
        user_id=cfg.user_id,
        employer_id=cfg.employer_id,
        employer_name=cfg.employer_name,
        allocation_type=cfg.allocation_type,
        is_active=bool(cfg.is_active),
        created_at=datetime_to_iso(cfg.created_at) or now_utc_iso(),
        updated_at=datetime_to_iso(cfg.updated_at) or now_utc_iso(),
    )
    result_allocs: List[DirectDepositAllocationModel] = []
    for alloc in allocs:
        result_allocs.append(
            DirectDepositAllocationModel(
                id=alloc.id,
                direct_deposit_config_id=alloc.direct_deposit_config_id,
                account_id=alloc.account_id,
                percentage=alloc.percentage,
                created_at=datetime_to_iso(alloc.created_at) or now_utc_iso(),
                updated_at=datetime_to_iso(alloc.updated_at) or now_utc_iso(),
            )
        )
    session.close()
    return DirectDepositSetupResponse(direct_deposit_config=model_cfg, allocations=result_allocs)


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)