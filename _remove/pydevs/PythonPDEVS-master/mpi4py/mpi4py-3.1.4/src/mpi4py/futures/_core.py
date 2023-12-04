# Author:  Lisandro Dalcin
# Contact: dalcinl@gmail.com

# pylint: disable=unused-import
# pylint: disable=redefined-builtin
# pylint: disable=missing-module-docstring

try:

    from concurrent.futures import (ALL_COMPLETED, FIRST_COMPLETED,
                                    FIRST_EXCEPTION, CancelledError, Executor,
                                    Future, TimeoutError, as_completed, wait)

    try:  # Python 3.7
        from concurrent.futures import BrokenExecutor
    except ImportError:  # pragma: no cover
        class BrokenExecutor(RuntimeError):
            """The executor has become non-functional."""

    try:  # Python 3.8
        from concurrent.futures import InvalidStateError
    except ImportError:  # pragma: no cover
        # pylint: disable=too-few-public-methods
        # pylint: disable=useless-object-inheritance
        class InvalidStateError(CancelledError.__base__):
            """The operation is not allowed in this state."""

except ImportError:  # pragma: no cover

    from ._base import (ALL_COMPLETED, FIRST_COMPLETED, FIRST_EXCEPTION,
                        BrokenExecutor, CancelledError, Executor, Future,
                        InvalidStateError, TimeoutError, as_completed, wait)
