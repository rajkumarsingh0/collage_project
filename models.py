class VideoSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    session_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)