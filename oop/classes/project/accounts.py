from datetime import datetime
from decimal import Decimal

import pytz
from pytz import timezone


class Transaction:
    """Handles Account transactions"""

    TRANSACTION_STATUS = {"deposit": "D", "withdrawal": "W", "interest": "I", "declined": "X"}

    def __init__(self, status: str, amount: Decimal = Decimal(0)):
        self.__status = None

        self.datetime_utc = datetime.now(tz=pytz.utc)
        self.status = status
        self.amount = amount

        self._account_number = None
        self._transaction_id = None
        self._account_timezone = None
        self._local_datetime = None

    def __repr__(self) -> str:
        return self.confirmation_number()

    @classmethod
    def create_transaction_from_confirmation_number(cls, confirmation_number: str):
        status, account_number, datetime_utc, transaction_id = confirmation_number.split("-")
        datetime_utc = datetime.strptime(datetime_utc, "%Y%m%d%H%M%S")
        transaction = Transaction(status=status)
        transaction.datetime_utc = datetime_utc

        transaction._account_number = account_number
        transaction._transaction_id = transaction_id
        return transaction

    @property
    def amount(self) -> Decimal:
        if hasattr(self, "_amount"):
            return self._amount
        return Decimal(0)

    @amount.setter
    def amount(self, value: Decimal):
        if value < 0:
            raise ValueError("Negative transaction values are not allowed.")

        self._amount = Decimal(value)

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value: str):
        if value not in Transaction.TRANSACTION_STATUS.values():
            raise ValueError("Invalid transaction status.")

        self.__status = value

    @property
    def local_datetime(self) -> datetime:
        if self._account_timezone:
            return self.datetime_utc.astimezone(self._account_timezone)
        return self.datetime_utc

    def fill_account_details(self, account: "Account", transaction_id: int = None):
        self._account_number = account.account_number
        self._account_timezone = account.preferred_time_zone
        self._transaction_id = transaction_id

    def confirmation_number(self) -> str:
        return (
            f"{self.status}-{self._account_number}"
            f"-{self.datetime_utc.strftime('%Y%m%d%H%M%S')}-{self._transaction_id}"
        )


class Account:
    """Handles User account information"""
    __existing_accounts: list[int] = list()
    __transactions_count: int = 0
    interest_rate: int = 0.05

    def __init__(
        self,
        account_number: int,
        first_name: str,
        last_name: str,
        preferred_time_zone: timezone = timezone("UTC"),
    ):
        self._account_number = None
        self._transactions: list[Transaction] = list()

        self.account_number = account_number
        self.first_name = first_name
        self.last_name = last_name
        self.preferred_time_zone = preferred_time_zone

    @property
    def account_number(self) -> int:
        return self._account_number

    @account_number.setter
    def account_number(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Account number must be a positive integer.")

        if value in self.__existing_accounts:
            raise ValueError("Account number is already in use.")

        self._account_number = value
        self.__existing_accounts.append(value)

    @property
    def balance(self) -> Decimal:
        final_balance = Decimal(0)
        transactions = (
            transaction for transaction in self._transactions
            if transaction.status not in (Transaction.TRANSACTION_STATUS["declined"],)
        )
        for transaction in transactions:
            if transaction.status == Transaction.TRANSACTION_STATUS["withdrawal"]:
                final_balance -= transaction.amount
            else:
                final_balance += transaction.amount
        return final_balance

    def process_transaction(self, transaction: Transaction) -> str:
        if not transaction.amount or not isinstance(transaction.amount, Decimal):
            raise ValueError("Transaction can not be processed.")

        if transaction.status == Transaction.TRANSACTION_STATUS["withdrawal"] and self.balance < transaction.amount:
            transaction.status = Transaction.TRANSACTION_STATUS["declined"]

        self.__transactions_count += 1
        transaction.fill_account_details(account=self, transaction_id=self.__transactions_count)
        self._transactions.append(transaction)
        return str(transaction)

    def deposit_interest(self) -> str:
        interest_amount: Decimal = Decimal(self.interest_rate) * Decimal(self.balance)
        interest_transaction = Transaction(
            status=Transaction.TRANSACTION_STATUS["interest"],
            amount=interest_amount,
        )
        confirmation_code: str = self.process_transaction(interest_transaction)
        return confirmation_code
