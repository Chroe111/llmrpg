from app.models import Session
from app import db

print(db.message_history(Session("G0foUeUm")))
