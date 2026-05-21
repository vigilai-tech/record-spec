"""
record-py — Python SDK for the RECORD open standard.

    from record_py import RecordEmitter, RecordValidator
    from record_py.openinference_adapter import adapt_span
"""

from .emitter import RecordEmitter
from .validator import RecordValidator

__all__ = ["RecordEmitter", "RecordValidator"]
__version__ = "0.1.0"
