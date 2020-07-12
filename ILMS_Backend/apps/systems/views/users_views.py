import json

import settings
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler

from utils.list_pages import CusResponse, MySearchFilter, ReadModelViewSetPlus, WriteModelViewSetPlus
from ..models import UsersInfo, BranchesInfo, RolesInfo
from ..serializers import UsersSerializerAnti, UsersSerializer, JwtLogSerializer, AnonymousUser, UpdatePasswordSerial, \
    UserUpdateSerializer
from ..utils import UserFilterSet, CheckUserAccFilter, CheckUserNameFilter


'''
# 用户视图集
class UsersViews(ModelViewSetPlus):
    """用户视图集"""

    queryset = UsersInfo.objects.filter(~Q(pk=1))
    serializer_class = [UsersSerializerAnti, UsersSerializer]
    filter_backends = [DjangoFilterBackend, MySearchFilter]
    filterset_class = UserFilterSet
    pagination_class = CusResponse
    search_fields = ['account', 'username']

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return self.serializer_class[0]
        else:
            return self.serializer_class[1]
'''


# 用户读视图集
class UsersReadViews(ReadModelViewSetPlus):
    """用户读视图集"""

    queryset = UsersInfo.objects.filter(~Q(pk=1))
    serializer_class = UsersSerializer
    filter_backends = [DjangoFilterBackend, MySearchFilter]
    filterset_class = UserFilterSet
    pagination_class = CusResponse
    search_fields = ['account', 'username']


# 用户写视图集
class UsersWriteViews(WriteModelViewSetPlus):
    """用户写视图集"""

    queryset = UsersInfo.objects.filter(~Q(pk=1))
    serializer_class = [UsersSerializerAnti, UserUpdateSerializer]

    def get_serializer_class(self):
        if self.action == 'update':
            return self.serializer_class[1]
        else:
            return self.serializer_class[0]

    def create(self, request, *args, **kwargs):
        if not self.request.data.get('username'):
            return CusResponse.get_response(success=False, message='缺少用戶名', code=settings.FALSE_CODE)
        if not self.request.data.get('account'):
            return CusResponse.get_response(success=False, message='缺少用戶账号', code=settings.FALSE_CODE)
        if not self.request.data.get('password'):
            return CusResponse.get_response(success=False, message='缺少密码', code=settings.FALSE_CODE)
        if not self.request.data.get('bran'):
            return CusResponse.get_response(success=False, message='缺少分部id', code=settings.FALSE_CODE)
        if not self.request.data.get('roles'):
            return CusResponse.get_response(success=False, message='缺少角色id', code=settings.FALSE_CODE)
        return super().create(request, *args, **kwargs)


# jwt登录视图
class UsersLoginView(GenericAPIView):
    """jwt登录视图1"""
    serializer_class = JwtLogSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data.get('account')
        password = serializer.validated_data.get('password')
        try:
            user = UsersInfo.objects.get(account=account)
        except Exception as e:
            return CusResponse.get_response(message='用户名或密码错误', code=settings.FALSE_CODE)
        if user.status == 0:
            return CusResponse.get_response(message='该账号已被冻结，请联系管理员！')
        elif user and user.check_password(password):
            payload = jwt_payload_handler(user=user)
            jwt_token = jwt_encode_handler(payload=payload)

            _menu_list = user.roles.all().values_list('menu_list', flat=True)
            menu_list = []
            [menu_list.extend(i) for i in _menu_list]
            menu_list = list(set(menu_list))

            data = dict()
            data['token'] = jwt_token
            data['id'] = user.id
            data['username'] = user.username
            data['permissions'] = menu_list

            # 增加权限缓存逻辑
            redis_conn = get_redis_connection('default')
            redis_conn.setex(user.id, settings.IMG_CODE_EXPIRE, json.dumps({i: True for i in menu_list}))

            return CusResponse.get_response(data=data)
        else:
            return CusResponse.get_response(message='用户名或密码错误')


# 检查用户账号是否重复
class CheckUserAcc(GenericAPIView):
    """检查用户账号是否重复"""

    queryset = UsersInfo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CheckUserAccFilter

    def get(self, request, *args, **kwargs):
        pk = self.request.query_params.get('pk')
        if pk and pk.isdigit():
            pk = int(pk)
        account = self.request.query_params.get('account')
        try:
            pk_, account_ = self.queryset.values_list('pk', 'account').get(
                account=account)
        except Exception as e:
            return CusResponse.get_response(data=0)
        if pk == pk_:
            return CusResponse.get_response(data=0)
        else:
            return CusResponse.get_response(data=1, message='该用户账号已存在！')


# 检查用户名称是否重复
class CheckUserName(GenericAPIView):
    """检查用户名称是否重复"""

    queryset = UsersInfo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CheckUserNameFilter

    def get(self, request, *args, **kwargs):
        pk = self.request.query_params.get('pk')
        if pk and pk.isdigit():
            pk = int(pk)
        username = self.request.query_params.get('username')
        try:
            pk_, username = self.queryset.values_list('pk', 'username').get(
                username=username)
        except Exception as e:
            return CusResponse.get_response(data=0)
        if pk == pk_:
            return CusResponse.get_response(data=0)
        else:
            return CusResponse.get_response(data=1, message='该用户名称已存在！')


# 重置密码接口
class ResetPassword(GenericAPIView):
    """重置密码接口"""

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        request_user = request.user
        if isinstance(request_user, AnonymousUser):
            request_user = None
        modifier = request_user
        _kwargs = {
            'password': make_password('e10adc3949ba59abbe56e057f20f883e'),
            'modifier': modifier
        }
        UsersInfo.objects.filter(pk=pk).update(**_kwargs)
        return CusResponse.get_response(success=True, message='重置密码成功')


# 修改密码接口
class UpdatePassword(GenericAPIView):
    """修改密码接口"""

    serializer_class = UpdatePasswordSerial

    def post(self, request, *args, **kwargs):
        request_user = self.request.user
        if isinstance(request_user, AnonymousUser):
            request_user = None
        modifier = request_user

        pk = kwargs.get('pk')
        old_password = self.request.data.get('old_password')
        new_password = self.request.data.get('new_password')
        ensure_password = self.request.data.get('ensure_password')
        _kwargs = {
            'password': make_password(new_password),
            'modifier': modifier
        }
        instance = UsersInfo.objects.get(pk=pk)
        if not all([old_password, new_password, ensure_password]):
            return CusResponse.get_response(success=False, message='缺少毕传参数！')
        elif new_password != ensure_password:
            return CusResponse.get_response(success=False, message='确认密码与新密码不一致！')
        elif instance.check_password(old_password):
            UsersInfo.objects.filter(pk=pk).update(**_kwargs)
            return CusResponse.get_response(message='修改密码成功！')
        else:
            return CusResponse.get_response(success=False, message='原密码不正确')


# 获取分部和角色列表
class GetBranchRole(GenericAPIView):
    """获取分部和角色列表"""

    def get(self, request):
        return CusResponse.get_response(data={
            'branches': BranchesInfo.objects.values('id', 'name').filter(~Q(id=1) & Q(status=1)),
            'roles': RolesInfo.objects.values('id', 'name').filter(~Q(id=1) & Q(status=1))
        })


"""----------------------------------------------------------- cookie 登陆--------------------------------------------"""


# Cookie 登录视图
class UsersLoginCookieView(GenericAPIView):
    """Cookie 登录视图"""
    serializer_class = JwtLogSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data.get('account')
        password = serializer.validated_data.get('password')
        try:
            user = UsersInfo.objects.get(account=account)
        except Exception as e:
            return CusResponse.get_response(message='用户名或密码错误', code=settings.FALSE_CODE)
        if user.status == 0:
            return CusResponse.get_response(message='该账号已被冻结，请联系管理员！', code=settings.FALSE_CODE)
        elif user and user.check_password(password):
            _menu_list = user.roles.all().values_list('menu_list', flat=True)
            menu_list = []
            [menu_list.extend(i) for i in _menu_list]
            menu_list = list(set(menu_list))

            data = dict()
            data['id'] = user.id
            data['username'] = user.username
            data['permissions'] = menu_list

            # 保持登陆状态
            login(request, user)

            # 增加权限缓存逻辑
            redis_conn = get_redis_connection('default')
            redis_conn.setex(user.id, settings.IMG_CODE_EXPIRE, json.dumps({i: True for i in menu_list}))

            return CusResponse.get_response(data=data)
        else:
            return CusResponse.get_response(message='用户名或密码错误')


if __name__ == '__main__':
    pass
