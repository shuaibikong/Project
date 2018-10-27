import xadmin
from .models import UserOperation, Comments


class UserOperationAdmin:
    pass


class CommentsAdmin:
    pass


xadmin.site.register(UserOperation, UserOperationAdmin)
xadmin.site.register(Comments, CommentsAdmin)