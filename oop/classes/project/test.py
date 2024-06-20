from decimal import Decimal

import freezegun
import pytest

from oop.classes.project.accounts import Account, Transaction


class BaseTestCase:
    def setup_method(*args, **kwargs):
        Account._Account__existing_accounts = []
        Account._Account__transactions_count = 0


@freezegun.freeze_time("2024-06-01", tick=False)
class TestTransaction(BaseTestCase):
    @freezegun.freeze_time("2024-06-01", tick=False)
    def test_empty_transaction_creation(self):
        t1 = Transaction(
            status=Transaction.TRANSACTION_STATUS["deposit"],
            amount=Decimal(10),
        )

        assert t1.datetime_utc is not None
        assert t1.datetime_utc.year == 2024
        assert t1.datetime_utc.month == 6
        assert t1.datetime_utc.day == 1
        assert t1.datetime_utc.hour == 0
        assert t1.datetime_utc.minute == 0
        assert t1.datetime_utc.second == 0

        assert t1._account_number is None
        assert t1._transaction_id is None
        assert t1._account_timezone is None

    def test_negative_transactions_not_allowed(self):
        with pytest.raises(ValueError) as e:
            Transaction(
                status=Transaction.TRANSACTION_STATUS["deposit"],
                amount=Decimal(-10),
            )
        assert e.value.args[0] == "Negative transaction values are not allowed."

    def test_invalid_transaction_status_not_allowed(self):
        with pytest.raises(ValueError) as e:
            Transaction(
                status="status_not_supported",
                amount=Decimal(10),
            )
        assert e.value.args[0] == "Invalid transaction status."

    def test_create_transaction_from_confirmation_number(self):
        confirmation_number: str = "D-2214123-20230923173045-231"
        transaction = Transaction.create_transaction_from_confirmation_number(confirmation_number)
        assert str(transaction) == confirmation_number


@freezegun.freeze_time("2024-06-01T12:30:45", tick=False)
class TestAccount(BaseTestCase):

    def test_account_init(self):
        account = Account(
            account_number=12345, first_name="John", last_name="Doe",
        )

        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.account_number == 12345
        assert account.balance == Decimal(0)
        assert account._transactions == []
        assert Account._Account__existing_accounts == [12345]

    def test_account_init__duplicated_account_numbers_raises_an_exception(self):
        Account(
            account_number=12345, first_name="John", last_name="Doe",
        )

        with pytest.raises(ValueError):
            Account(
                account_number=12345, first_name="Bob", last_name="Smith",
            )

    @pytest.mark.parametrize(
        "invalid_input", ["abc", -1, 0, 5.25, None]
    )
    def test_invalid_account_number(self, invalid_input):
        with pytest.raises(ValueError):
            Account(
                account_number=invalid_input, first_name="John", last_name="Doe",
            )

    def test_balance_is_read_only(self):
        account = Account(
            account_number=12345, first_name="John", last_name="Doe",
        )
        assert account.balance == Decimal(0)

        with pytest.raises(AttributeError):
            account.balance = Decimal(100)

    def test_process_deposit(self):
        account = Account(
            account_number=12345, first_name="John", last_name="Doe",
        )
        t1 = Transaction(amount=Decimal(100), status=Transaction.TRANSACTION_STATUS["deposit"])
        confirmation_number: str = account.process_transaction(t1)
        assert confirmation_number == 'D-12345-20240601123045-1'

        assert account.balance == Decimal(100)
        assert t1 in account._transactions

        assert t1._account_number == account.account_number
        assert t1._transaction_id == 1
        assert t1._account_timezone == account.preferred_time_zone

    def test_process_withdrawal(self):
        account = Account(
            account_number=12345, first_name="John", last_name="Doe",
        )
        t1 = Transaction(amount=Decimal(100), status=Transaction.TRANSACTION_STATUS["deposit"])
        t2 = Transaction(amount=Decimal(45), status=Transaction.TRANSACTION_STATUS["withdrawal"])
        account.process_transaction(t1)
        confirmation_number: str = account.process_transaction(t2)
        assert confirmation_number == "W-12345-20240601123045-2"

        assert account.balance == Decimal(55)
        assert t1 in account._transactions
        assert t2 in account._transactions

        assert t1._account_number == account.account_number
        assert t1._transaction_id == 1
        assert t1._account_timezone == account.preferred_time_zone

        assert t2._account_number == account.account_number
        assert t2._transaction_id == 2
        assert t2._account_timezone == account.preferred_time_zone

    def test_process_declined_transaction(self):
        account = Account(
            account_number=12345, first_name="John", last_name="Doe",
        )
        t1 = Transaction(amount=Decimal(100), status=Transaction.TRANSACTION_STATUS["deposit"])
        t2 = Transaction(amount=Decimal(150), status=Transaction.TRANSACTION_STATUS["withdrawal"])
        account.process_transaction(t1)
        confirmation_number: str = account.process_transaction(t2)
        assert confirmation_number == "X-12345-20240601123045-2"

        assert account.balance == Decimal(100)
        assert t1 in account._transactions
        assert t2 in account._transactions

        assert t1._account_number == account.account_number
        assert t1._transaction_id == 1
        assert t1._account_timezone == account.preferred_time_zone

        assert t2._account_number == account.account_number
        assert t2._transaction_id == 2
        assert t2._account_timezone == account.preferred_time_zone
        assert t2.status == Transaction.TRANSACTION_STATUS["declined"]

    def test_account_have_separate_transactions(self):
        a1 = Account(
            account_number=12345, first_name="John", last_name="Doe",
        )
        t1 = Transaction(amount=Decimal(100), status=Transaction.TRANSACTION_STATUS["deposit"])
        t2 = Transaction(amount=Decimal(150), status=Transaction.TRANSACTION_STATUS["deposit"])
        a1.process_transaction(t1)
        a1.process_transaction(t2)

        a2 = Account(
            account_number=67890, first_name="Bob", last_name="Smith",
        )
        t1 = Transaction(amount=Decimal(1000), status=Transaction.TRANSACTION_STATUS["deposit"])
        t2 = Transaction(amount=Decimal(1500), status=Transaction.TRANSACTION_STATUS["deposit"])
        a2.process_transaction(t1)
        a2.process_transaction(t2)

        assert a1.balance == Decimal(250)
        assert a2.balance == Decimal(2500)

    def test_account_deposit_interest(self):
        a1 = Account(
            account_number=1122334455, first_name="John", last_name="Doe",
        )
        t1 = Transaction(amount=Decimal(10000), status=Transaction.TRANSACTION_STATUS["deposit"])
        t2 = Transaction(amount=Decimal(15000), status=Transaction.TRANSACTION_STATUS["deposit"])
        a1.process_transaction(t1)
        a1.process_transaction(t2)

        assert a1.balance == Decimal(25000)

        confirmation_code: str = a1.deposit_interest()
        assert confirmation_code == "I-1122334455-20240601123045-3"
        assert round(a1.balance, 4) == Decimal(26250.0000)
