from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from django.template import loader
from .serializers import UserManagersSerializer

import json


# Create your views here.
@csrf_exempt
def index(request):
    """
    Login index page
    :param request:
        - GET show login page
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.index.html', context={})

    if request.method == 'POST':
        return render(request, 'dashboard.index.html', context={})


@csrf_exempt
def add_user(request):
    """
    Add new user manager
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'dashboard.adduser.html', context={})

    elif request.method == 'POST':
        try:
            import hashlib
            data = json.loads(request.body.decode('utf-8'))
            # print(data)

            data['password'] = hashlib.sha1(data['password'].encode('utf-8')).hexdigest()
            # print(data)
            context = {
                'status': 0,
                'msg': 'user added',
            }

            serializer = UserManagersSerializer(data=data)
            if serializer.is_valid():
                # print(serializer.data)
                serializer.save()

                return JSONRenderer(context)

            print(serializer.errors)

        except Exception as e:
            print(e)
            context = {
                'status': 1,
                'error_code': '999',
                'msg': 'Add user got error',
            }

        return render(request, 'dashboard.adduser.html', context=context)
