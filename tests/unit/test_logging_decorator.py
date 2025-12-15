import logging
import pytest

from app.utils.logging_decorator import service_log


def test_logs_entry_and_exit(caplog):
    caplog.set_level(logging.INFO, logger="service_logger")

    @service_log
    def add(a, b=0):
        """Simple add function"""
        return a + b

    # metadata preserved
    assert add.__name__ == "add"
    assert add.__doc__ == "Simple add function"

    res = add(2, b=3)
    assert res == 5

    messages = [r.getMessage() for r in caplog.records]
    # Logger records use the qualified name (e.g. '....<locals>.add'), so assert on tokens
    assert any(("Entering" in m and "add" in m) for m in messages)
    assert any(("Exiting" in m and "result=5" in m) for m in messages)


def test_logs_exception(caplog):
    caplog.set_level(logging.ERROR, logger="service_logger")

    @service_log
    def boom():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        boom()

    messages = [r.getMessage() for r in caplog.records]
    assert any(("Exception in" in m and "boom" in m) for m in messages)
