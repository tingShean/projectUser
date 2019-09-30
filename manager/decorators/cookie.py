from django.shortcuts import render


def check_cookie(view_func):

    def _wrapped_view_func(request, *args, **kwargs):
        try:
            if 'admin_uid' not in request.COOKIES:
                return render(request, 'login.index.html', context={})

        except Exception as e:
            print(e)
            return render(request, 'login.index.html', context={})

        # return func
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
