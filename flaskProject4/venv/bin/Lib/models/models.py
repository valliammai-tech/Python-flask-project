class User(db.Document):
 email = db.EmailField(required=True, unique=True)
 password = db.StringField(required=True, min_length=6)