import json

from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
import user
from iotapp.models import IotDevice


def index(request):
    data = {
        'name': 'zhangsan',
        'age': 18,
    }
    # return HttpResponse(json.dumps(data),content_type="application/json")
    return JsonResponse(data)


@login_required(login_url='/user/requestLogin/')
def add(request):
    if request.method == 'POST':
        msg = json.loads(request.body)
        device_id = msg['device_id']
        device_name = msg['device_name']
        device_type = msg['device_type']
        ownByUser = request.user.username
        try:
            IotDevice.objects.get(device_id=device_id)
            response = {
                'error': -1,
                'msg':'设备已存在'
            }
            return JsonResponse(response)
        except IotDevice.DoesNotExist:
            device = IotDevice()
            device.device_id = device_id
            device.device_name = device_name
            device.device_type = device_type
            device.own_by_user = ownByUser
            device.save()
            print(device)
            response = {
                'error': 0,
                'msg': '设备添加成功'
            }
            return JsonResponse(response)


@login_required(login_url='/user/requestLogin/')
def delete(request):
    try:
        msg = json.loads(request.body)
        device_id = msg['device_id']
        device = IotDevice.objects.get(device_id=device_id, own_by_user=request.user.username)
        device.delete()
    except IotDevice.DoesNotExist:
        print('Device.DoesNotExist')
        pass
    response = {
        'error': 0,
        'msg': '设备已删除'
    }
    return JsonResponse(response)


@login_required(login_url='/user/requestLogin/')
def find(request):
    try:
        msg = json.loads(request.body)
        device_id = msg['device_id']
        device = IotDevice.objects.get(device_id=device_id, own_by_user=request.user.username)
        iotDevice = [{
            'deviceID': device.device_id,
            'deviceName': device.device_name,
            'deviceType': device.device_type
        }]
        deviceJson = {
            'error': 0,
            'device': iotDevice
        }
        return JsonResponse(deviceJson)
    except IotDevice.DoesNotExist:
        response = {
            'error': -1,
            'msg': '设备不存在'
        }
        return JsonResponse(response)


@login_required(login_url='/user/requestLogin/')
def count(request):
    if request.method == 'GET':
        count = IotDevice.objects.filter(own_by_user=request.user.username).count()
        print(count)
        response = {
            'error': 0,
            'count': count
        }
        return JsonResponse(response)

@login_required(login_url='/user/requestLogin/')
def getDevices(request):
    if request.method == 'POST':
        msg = json.loads(request.body)
        startIndex = msg['startIndex']
        endIndex = msg['count'] + startIndex
        devices = IotDevice.objects.filter(own_by_user=request.user.username).order_by('id')[startIndex:endIndex]
        iotDevice = []
        for device in devices:
            iotDevice.append({
                'id': device.id,
                'deviceID': device.device_id,
                'deviceName': device.device_name,
                'deviceType': device.device_type})

        totalCount = IotDevice.objects.filter(own_by_user=request.user.username).count()

        response = {
            'error': 0,
            'totalCount': totalCount,
            'iotDevice': iotDevice
        }
        return JsonResponse(response)
