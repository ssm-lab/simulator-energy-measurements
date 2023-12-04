import sys
from concurrent.futures import ALL_COMPLETED as ALL_COMPLETED
from concurrent.futures import FIRST_COMPLETED as FIRST_COMPLETED
from concurrent.futures import FIRST_EXCEPTION as FIRST_EXCEPTION
from concurrent.futures import CancelledError as CancelledError
from concurrent.futures import Executor as Executor
from concurrent.futures import Future as Future
from concurrent.futures import TimeoutError as TimeoutError
from concurrent.futures import as_completed as as_completed
from concurrent.futures import wait as wait

if sys.version_info >= (3, 7):
    from concurrent.futures import BrokenExecutor as BrokenExecutor
else:
    class BrokenExecutor(RuntimeError): ...

if sys.version_info >= (3, 8):
    from concurrent.futures import InvalidStateError as InvalidStateError
else:
    from concurrent.futures._base import Error
    class InvalidStateError(Error): ...
