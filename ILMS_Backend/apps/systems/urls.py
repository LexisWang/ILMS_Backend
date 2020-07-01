from django.conf.urls import url

from .views import UsersLoginView, BranchesReadViews, BranchesWriteViews, CheckBranName, RolesWriteViews, \
    RolesReadViews, CheckRoleName, UsersWriteViews, UsersReadViews, CheckUserAcc, CheckUserName, ResetPassword, \
    UpdatePassword, GetBranchRole, FilesWriteViews, TypesWriteViews, TypesReadViews, CountiesWriteViews, \
    CountiesReadViews, ValuesWriteViews, ValuesReadViews, CitiesWriteViews, CitiesReadViews, CheckType, CheckValue, \
    CheckCounty, CheckCity, PricesReadViews, PricesWriteViews

urlpatterns = [
    url(r'^users/login$', UsersLoginView.as_view()),
    # url(r'^users/login$', UsersLoginCookieView.as_view()),

    # 分部模块
    url(r'^branches-create$', BranchesWriteViews.as_view({'post': 'create'})),
    url(r'^branches-update/(?P<pk>\d+)$', BranchesWriteViews.as_view({'put': 'update'})),
    url(r'^branches-delete/(?P<pk>\d+)$', BranchesWriteViews.as_view({'delete': 'destroy'})),
    url(r'^branches-detail/(?P<pk>\d+)$', BranchesReadViews.as_view({'get': 'retrieve'})),
    url(r'^branches-list$', BranchesReadViews.as_view({'get': 'list'})),
    url(r'^branches/check-name$', CheckBranName.as_view()),

    # 角色模块
    url(r'^roles-create$', RolesWriteViews.as_view({'post': 'create'})),
    url(r'^roles-update/(?P<pk>\d+)$', RolesWriteViews.as_view({'put': 'update'})),
    url(r'^roles-delete/(?P<pk>\d+)$', RolesWriteViews.as_view({'delete': 'destroy'})),
    url(r'^roles-detail/(?P<pk>\d+)$', RolesReadViews.as_view({'get': 'retrieve'})),
    url(r'^roles-list$', RolesReadViews.as_view({'get': 'list'})),
    url(r'^roles/check-name$', CheckRoleName.as_view()),

    # 用户模块
    url(r'^users-create$', UsersWriteViews.as_view({'post': 'create'})),
    url(r'^users-update/(?P<pk>\d+)$', UsersWriteViews.as_view({'put': 'update'})),
    url(r'^users-delete/(?P<pk>\d+)$', UsersWriteViews.as_view({'delete': 'destroy'})),
    url(r'^users-detail/(?P<pk>\d+)$', UsersReadViews.as_view({'get': 'retrieve'})),
    url(r'^users-list$', UsersReadViews.as_view({'get': 'list'})),

    # 检查
    url(r'^users/check-account$', CheckUserAcc.as_view()),
    url(r'^users/check-username$', CheckUserName.as_view()),
    # 密码
    url(r'^users/reset-password$', ResetPassword.as_view()),
    url(r'^users/update-password$', UpdatePassword.as_view()),

    # 新增用户时获取 分部和角色
    url(r'^users/branches-roles$', GetBranchRole.as_view()),

    # 文件模块
    url(r'^files$', FilesWriteViews.as_view({'post': 'create'})),

    # 字典类型
    url(r'^types-create$', TypesWriteViews.as_view({'post': 'create'})),
    url(r'^types-update/(?P<pk>\d+)$', TypesWriteViews.as_view({'put': 'update'})),
    url(r'^types-delete/(?P<pk>\d+)$', TypesWriteViews.as_view({'delete': 'destroy'})),
    url(r'^types-detail/(?P<pk>\d+)$', TypesReadViews.as_view({'get': 'retrieve'})),
    url(r'^types-list$', TypesReadViews.as_view({'get': 'list'})),

    # 国家
    url(r'^counties-create$', CountiesWriteViews.as_view({'post': 'create'})),
    url(r'^counties-update/(?P<pk>\d+)$', CountiesWriteViews.as_view({'put': 'update'})),
    url(r'^counties-delete/(?P<pk>\d+)$', CountiesWriteViews.as_view({'delete': 'destroy'})),
    url(r'^counties-detail/(?P<pk>\d+)$', CountiesReadViews.as_view({'get': 'retrieve'})),
    url(r'^counties-list$', CountiesReadViews.as_view({'get': 'list'})),

    # 字典值
    url(r'^values-create$', ValuesWriteViews.as_view({'post': 'create'})),
    url(r'^values-update/(?P<pk>\d+)$', ValuesWriteViews.as_view({'put': 'update'})),
    url(r'^values-delete/(?P<pk>\d+)$', ValuesWriteViews.as_view({'delete': 'destroy'})),
    url(r'^values-detail/(?P<pk>\d+)$', ValuesReadViews.as_view({'get': 'retrieve'})),
    url(r'^values-list$', ValuesReadViews.as_view({'get': 'list'})),

    # 城市
    url(r'^cities-create$', CitiesWriteViews.as_view({'post': 'create'})),
    url(r'^cities-update/(?P<pk>\d+)$', CitiesWriteViews.as_view({'put': 'update'})),
    url(r'^cities-delete/(?P<pk>\d+)$', CitiesWriteViews.as_view({'delete': 'destroy'})),
    url(r'^cities-detail/(?P<pk>\d+)$', CitiesReadViews.as_view({'get': 'retrieve'})),
    url(r'^cities-list$', CitiesReadViews.as_view({'get': 'list'})),

    # 检查字典(类型，国家，城市)
    url(r'^check-type$', CheckType.as_view()),
    url(r'^check-value$', CheckValue.as_view()),
    url(r'^check-county$', CheckCounty.as_view()),
    url(r'^check-city$', CheckCity.as_view()),

    # 价格配置模块
    url(r'^prices$', PricesReadViews.as_view({'get': 'list'})),
    url(r'^prices/(?P<pk>\d+)$', PricesWriteViews.as_view({'put': 'update'})),
]
