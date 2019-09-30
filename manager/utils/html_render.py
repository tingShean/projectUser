from django.shortcuts import render
from login.serializers import UserAuthorizeGetSerializer, PageNameGetSerializer


def web_render(request, tmpl, context, user=None, c_key=None, c_val=None):
    """set cookie"""

    resp = render(request, tmpl, context)
    if c_key and c_val:
        resp.set_cookie(c_key, c_val)
    elif user:
        bar_serializer = UserAuthorizeGetSerializer(data=user)

        if not bar_serializer.is_valid():
            print(bar_serializer.errors)
            return render(request, 'login.index.html', context={})

        # print(bar_serializer.validated_data['bar_list'])
        bar_list = bar_serializer.validated_data['bar_list']

        page = {}
        page_list = []
        page_title = ''
        bar_context = ''
        # get bar list by authorize
        for bar in bar_list:
            page['id'] = bar['page']

            page_serializer = PageNameGetSerializer(data=page)
            if not page_serializer.is_valid():
                print(page_serializer.errors)
                return render(request, 'login.index.html', context={})

            if not page_title:
                page_title = page_serializer.validated_data['title']
                bar_context += '<tr><td>' \
                               '<h3>{}</h3>' \
                               '</td></tr>'.format(page_title)

            elif page_serializer.validated_data['title'] != page_title:
                page_title = page_serializer.validated_data['title']
                bar_context += '<tr><td>' \
                               '<h3>{}</h3>' \
                               '</td></tr>'.format(page_title)

            bar_context += '<tr><td>' \
                           '<a href="./{}/">{}</a></br>' \
                           '</td></tr>'.format(page_serializer.validated_data['id'],
                                               page_serializer.validated_data['name'])

        # print(bar_context)
        context['bar_context'] = bar_context

        resp.set_cookie('admin_uid', user['uid'])

    return resp
