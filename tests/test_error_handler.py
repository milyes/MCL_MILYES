import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from mcldz.error_handler import ErrorHandler, MCLError, get_handler, handle_error, safe_run

def test_create_error():
    e = MCLError("ERROR", "test", "erreur test")
    assert e.level == "ERROR"
    assert e.module == "test"
    assert e.message == "erreur test"

def test_error_to_dict():
    e = MCLError("WARNING", "gen", "alerte", {"key": "val"})
    d = e.to_dict()
    assert d["level"] == "WARNING"
    assert d["details"]["key"] == "val"
    assert d["timestamp"] is not None

def test_error_with_exception():
    try:
        raise ValueError("boom")
    except Exception as ex:
        e = MCLError("ERROR", "test", "crash", exception=ex)
        assert e.traceback is not None
        assert "ValueError" in e.traceback

def test_handler_handle():
    h = ErrorHandler()
    h.clear()
    err = h.handle("INFO", "test", "ok")
    assert len(h.errors) == 1
    assert h.errors[0].message == "ok"

def test_handler_stats():
    h = ErrorHandler()
    h.clear()
    h.handle("ERROR", "a", "e1")
    h.handle("ERROR", "b", "e2")
    h.handle("WARNING", "c", "w1")
    s = h.get_stats()
    assert s["ERROR"] == 2
    assert s["WARNING"] == 1
    assert s["CRITICAL"] == 0

def test_handler_max_history():
    h = ErrorHandler(max_history=3)
    for i in range(5):
        h.handle("ERROR", "test", str(i))
    assert len(h.errors) == 3
    assert h.errors[-1].message == "4"

def test_handler_clear():
    h = ErrorHandler()
    h.handle("ERROR", "t", "m")
    h.clear()
    assert len(h.errors) == 0

def test_handler_recent():
    h = ErrorHandler()
    h.clear()
    for i in range(5):
        h.handle("ERROR", "mod" + str(i), "msg" + str(i))
    r = h.get_recent(2)
    assert len(r) == 2
    assert r[0]["message"] == "msg3"
    assert r[1]["message"] == "msg4"

def test_safe_run_success():
    result = safe_run("test", lambda: 42)
    assert result == 42

def test_safe_run_error():
    result = safe_run("test", lambda: 1/0)
    assert result is None

def test_safe_run_captures():
    h = get_handler()
    h.clear()
    def boom():
        raise RuntimeError("fail")
    safe_run("boom_mod", boom)
    s = h.get_stats()
    assert s["ERROR"] == 1
    h.clear()

def test_handle_error_quick():
    h = get_handler()
    h.clear()
    err = handle_error("WARNING", "quick", "test rapide")
    assert err.message == "test rapide"
    h.clear()

def test_error_persistence():
    with tempfile.TemporaryDirectory() as d:
        from mcldz.error_handler import ErrorHandler as EH
        from pathlib import Path
        h = EH(max_history=5)
        h._log_file = Path(d) / "errors.json"
        h.handle("ERROR", "persist", "saved")
        assert len(h.errors) == 1
        assert h._log_file.exists()

if __name__ == "__main__":
    test_create_error()
    test_error_to_dict()
    test_error_with_exception()
    test_handler_handle()
    test_handler_stats()
    test_handler_max_history()
    test_handler_clear()
    test_handler_recent()
    test_safe_run_success()
    test_safe_run_error()
    test_safe_run_captures()
    test_handle_error_quick()
    test_error_persistence()
    print("test_error_handler : 15/15 OK")
