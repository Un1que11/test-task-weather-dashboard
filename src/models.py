from src import db

class SearchHistory(db.Model):
    __tablename__ = "search_history"
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50), nullable=False)
    search_count = db.Column(db.Integer, default=1)
    session_id = db.Column(db.String(100), nullable=False)
