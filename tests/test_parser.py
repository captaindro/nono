import json
import pytest
from utils.parser import parse_msg


def test_parse_msg_with_valid_notification():
    msg = json.dumps({
        "method": "accountNotification",
        "params": {
            "result": {
                "value": {
                    "pubkey": "DummyMintAddress"
                }
            }
        }
    })
    mint, timestamp = parse_msg(msg)
    assert mint == "DummyMintAddress"
    assert timestamp is None  # ✅ attend None car pas de slot fourni


def test_parse_msg_with_valid_data():
    msg = json.dumps({
        "method": "accountNotification",
        "params": {
            "result": {
                "value": {
                    "data": {
                        "parsed": {
                            "info": {
                                "mint": "ValidMintAddress"
                            }
                        }
                    }
                },
                "context": {
                    "slot": 123456
                }
            }
        }
    })
    mint, timestamp = parse_msg(msg)
    assert mint == "ValidMintAddress"
    assert isinstance(timestamp, int)


def test_parse_msg_with_missing_fields():
    msg = json.dumps({"random": "data"})
    mint, timestamp = parse_msg(msg)
    assert mint is None
    assert timestamp is None


def test_parse_msg_with_none_result():
    msg = json.dumps({"result": None})
    mint, timestamp = parse_msg(msg)
    assert mint is None
    assert timestamp is None
