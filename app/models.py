from app import db
from app import login_manager
from flask_login import UserMixin

# Определение модели User
class User(db.Model, UserMixin):  # db.Model с заглавной буквы
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    clicks = db.Column(db.Integer, default=0)  # default вместо defaults

    def __repr__(self):
        return f"User {self.username} - clicks: {self.clicks}"  # Убрана лишняя кавычка

# Загрузка пользователя по id для flask_login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
