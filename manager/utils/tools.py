from login.models import UserManagers


def get_admin_uid_cookie(request):
    if 'admin_uid' in request.COOKIES:
        return request.COOKIES['admin_uid']

    return False


# get user account by uid
def get_user_account(uid):
    try:
        usr = UserManagers.objects.get(uid=uid)

        if not usr:
            raise

    except Exception as e:
        raise e

    return usr.account
