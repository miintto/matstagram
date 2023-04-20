from logging import Filter, LogRecord

from .transaction import ctx_manager


class TransactionFilter(Filter):

    def filter(self, record: LogRecord):
        record.transaction = ctx_manager.get_transaction()
        return True
