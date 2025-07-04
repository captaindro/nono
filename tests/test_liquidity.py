# tests/test_liquidity.py

import pytest
from utils.liquidity import get_liquidity, POOL_MAP

class DummyClient:
    def __init__(self, lamports):
        self._lamports = lamports
    def get_account_info(self, pool_account, encoding):
        # on renvoie toujours la même structure que Solana RPC
        return {"result": {"value": {"lamports": self._lamports}}}

@pytest.fixture(autouse=True)
def patch_rpc_and_map(monkeypatch):
    # remplace le client RPC par notre DummyClient (2 SOL = 2e9 lamports)
    import utils.liquidity as liqu
    monkeypatch.setattr(liqu, "RPC", DummyClient(2_000_000_000))
    # initialise le mapping pour le test
    liqu.POOL_MAP.clear()
    liqu.POOL_MAP["TestToken"] = "DummyPoolAccount"
    yield

def test_get_liquidity_for_mapped_token():
    liq = get_liquidity("TestToken")
    assert pytest.approx(liq, rel=1e-6) == 2.0

def test_get_liquidity_for_unmapped_token():
    liq = get_liquidity("UnknownToken")
    assert liq == 0.0
