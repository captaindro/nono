import json

def parse_msg(raw_msg: str):
    msg = json.loads(raw_msg)
    if "result" in msg:
        return None, None
    mint = msg["params"]["result"]["value"]["data"]["parsed"]["info"]["mint"]
    timestamp = msg["params"]["result"]["context"]["slot"]
    return mint, timestamp