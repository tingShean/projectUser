def get_admin_uid_cookie(request):
    if 'admin_uid' in request.COOKIES:
        return request.COOKIES['admin_uid']

    return False
