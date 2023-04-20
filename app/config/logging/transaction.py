from contextvars import ContextVar
from uuid import uuid4


class TransactionContextManager:
    transaction_contextvars = ContextVar("matstagram_transaction")

    def set_transaction(self):
        self.transaction_contextvars.set({"id": uuid4().hex})

    def get_transaction(self) -> dict:
        return self.transaction_contextvars.get()


ctx_manager = TransactionContextManager()
