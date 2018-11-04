from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from webapp.errors import unauthorized


class UserIsAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return unauthorized()


class UserIsAdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return unauthorized()
