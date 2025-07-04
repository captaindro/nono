# tests/test_honeypot.py
import pytest
from utils.honeypot import is_honeypot

class DummyResponse:
    def __init__(self, success, out_amount):
        self._success = success
        self._out = out_amount
    def raise_for_status(self): pass
    def json(self):
        return {"success": self._success, "data": {"outAmount": self._out}}

@pytest.fixture(autouse=True)
def dummy_env(monkeypatch):
    monkeypatch.setenv("YOUR_PUBLIC_KEY", "DummyPublicKey")

def test_is_honeypot_allows_sale(monkeypatch):
    monkeypatch.setattr("utils.honeypot.requests.get",
                        lambda *args, **kwargs: DummyResponse(True, 1000))
    assert not is_honeypot("SomeTokenMint", 1000, slippage_bps=50, user_public_key="DummyPublicKey")

def test_is_honeypot_blocks_sale(monkeypatch):
    monkeypatch.setattr("utils.honeypot.requests.get",
                        lambda *args, **kwargs: DummyResponse(False, 0))
    assert is_honeypot("SomeTokenMint", 1000, slippage_bps=50, user_public_key="DummyPublicKey")
