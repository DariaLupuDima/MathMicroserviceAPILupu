from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.request_log import RequestLog, Base
import os
print("Using DB file at:", os.path.abspath("requests.db"))


engine = create_engine('sqlite:///requests.db')
Session = sessionmaker(bind=engine)
session = Session()

logs = session.query(RequestLog).all()

if not logs:
    print("⚠️  No logs found in the database.")
else:
    for log in logs:
        print(f"{log.timestamp} - {log.operation}({log.input_data}) = {log.result}")
