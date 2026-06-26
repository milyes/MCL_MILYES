import sys, os, json, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from mcldz.logger import load_logs, save_log, load_project_leads, save_lead

def test_load_empty():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("[]")
        tmp = f.name
    import mcldz.config as cfg
    orig = cfg.DATA_FILE
    cfg.DATA_FILE = tmp
    assert load_logs() == []
    cfg.DATA_FILE = orig
    os.unlink(tmp)

def test_save_and_load():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("[]")
        tmp = f.name
    import mcldz.config as cfg
    orig = cfg.DATA_FILE
    cfg.DATA_FILE = tmp
    save_log({"test": True})
    logs = load_logs()
    assert len(logs) == 1
    assert logs[0]["test"] == True
    cfg.DATA_FILE = orig
    os.unlink(tmp)

def test_load_leads_empty():
    with tempfile.TemporaryDirectory() as d:
        import mcldz.logger as lg
        assert lg.load_project_leads(d) == []

def test_save_and_load_lead():
    with tempfile.TemporaryDirectory() as d:
        import mcldz.logger as lg
        assert lg.save_lead(d, {"name": "Ali", "phone": "0555123456"}) == True
        leads = lg.load_project_leads(d)
        assert len(leads) == 1
        assert leads[0]["name"] == "Ali"

def test_malformed_json():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "leads.json")
        with open(p, "w") as f:
            f.write("NOT JSON")
        import mcldz.logger as lg
        assert lg.load_project_leads(d) == []

if __name__ == "__main__":
    test_load_empty()
    test_save_and_load()
    test_load_leads_empty()
    test_save_and_load_lead()
    test_malformed_json()
    print("test_logger : 5/5 OK")
