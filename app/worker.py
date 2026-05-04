import time
from app.queue.redis_queue import pop_event
from app.db.session import SessionLocal
from app.models.analytics import Analytics
from app.core.logger import logger

def run_worker():
    db = SessionLocal()

    while True:
        event = pop_event()

        if event:
            record = Analytics(short_code=event["code"])
            db.add(record)
            db.commit()
            logger.info(f"Saved analytics for {event['code']}")

        time.sleep(1)


if __name__ == "__main__":
    run_worker()