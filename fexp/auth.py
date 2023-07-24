from fexp import login_manager
from fexp.models import User


@login_manager.user_loader
def load_user(user):
    return User.query.get(user)


