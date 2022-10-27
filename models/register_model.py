from sqlalchemydb import db



class RegisterModel(db.Model):
    __tablename__ = 'register'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(120))
    images = db.relationship('Img', backref='user', lazy=True)


    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email          

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def json(self):
        return {'username': self.username, 'email':self.email}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def __repr__(self) -> str:
        return '{}, {}'.format(self.username, self.email)



    
        