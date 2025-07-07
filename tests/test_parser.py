import json
import pytest
from utils.parser import parse_msg

def test_parse_msg_with_valid_notification():
    msg = json.dumps({
        "method": "accountNotification",
        "params": {
            "result": {
                "value": {
                    "pubkey": "DummyMintAddress",
                    "account": {}
                }
            }
        }
    })
    result = parse_msg(msg)
    assert isinstance(result, tuple)
    assert result[0] == "DummyMintAddress"
    assert isinstance(result[1], float)

def test_parse_msg_with_missing_fields():
    msg = json.dumps({"random": "data"})
    with pytest.raises(ValueError, match="Impossible de trouver 'pubkey'"):
        parse_msg(msg)
