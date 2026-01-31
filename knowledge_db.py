from pymongo import MongoClient

def connect_db():
    """Connect to the MongoDB knowledge base."""
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ai_knowledge_base"]
    return db

def load_rules_from_db():
    db = connect_db()
    rules = list(db.rules.find({}, {"_id": 0}))
    return rules

def load_percepts_from_db():
    db = connect_db()
    percepts = list(db.percepts.find({}, {"_id": 0}))
    return percepts
