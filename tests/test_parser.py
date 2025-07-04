# tests/test_parser.py

import json
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
    assert isinstance(result, dict)
    assert result["mint"] == "DummyMintAddress"

def test_parse_msg_with_missing_fields():
    # si le JSON ne contient pas les champs attendus, on doit obtenir mint=None
    msg = json.dumps({"random": "data"})
    result = parse_msg(msg)
    assert result["mint"] is None
