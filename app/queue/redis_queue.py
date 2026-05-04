import json
from app.cache.redis_client import r

QUEUE_NAME = "click_events"

def push_event(code: str):
    event = {"code": code}
    r.lpush(QUEUE_NAME, json.dumps(event))


def pop_event():
    event = r.rpop(QUEUE_NAME)
    if event:
        return json.loads(event)
    return None