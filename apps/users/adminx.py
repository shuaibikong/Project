import xadmin
from xadmin import views
from .models import EmailVerifyRecord


class BaseSetting:
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    site_title = "蓝鸭后台"
    site_footer = "blue"


class EmailVerifyRecordAdmin:
    list_display = ['code', 'email', "send_time"]


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)