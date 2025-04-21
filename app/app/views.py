from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import time

sens_data = []

@csrf_exempt
def data(request):
    global sens_data
    if request.method == 'POST':
        try:
            # Access data from request.POST (for form-encoded data)
            posted_data = request.POST.dict()

            # Alternatively, access JSON data from request.body
            body_data = json.loads(request.body.decode('utf-8'))
            print("Body Data:", body_data)

            if type(body_data) != list:
                body_data = [body_data]
            for item in body_data:
                if type(item) == dict:
                    sens_data.append(item)
            #print (sens_data)
            # Respond with a success message
            return JsonResponse({"message": "Data received successfully", "data": body_data}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
    
def read(request):
    template = "views.html"
    context = {}
    global sens_data
    avg_pwr, peak = avg_peak_power()
    context['data'] = sens_data
    context['avg_power'] = avg_pwr
    context['peak_power'] = peak
    return render(request, template, context)

def avg_peak_power():
    count = pwr = avg_pwr = peak = 0
    power_list = []
    for item in sens_data:
        pwr = int(item['power'])
        power_list.append(pwr)
        count +=1
    if count != 0:
        avg_pwr = sum(power_list)/count
        peak = max(power_list)
    return avg_pwr, peak

def home(request):
    return render(request, 'home.html')

def devices(request):
    # Example data, replace with your actual queryset or data source
    devices = [
        {'deviceid': '0', 'name': 'Main Meter', 'status': 'online', 'last_seen': '{0}'.format(time.strftime('%Y-%m-%d %H:%M:%S'))},
        {'deviceid': '1', 'name': 'AC Unit', 'status': 'offline', 'last_seen': '2025-03-31 19:44:10'},
        {'deviceid': '2', 'name': 'Geysers', 'status': 'offline', 'last_seen': '2025-03-31 19:44:10'},
        {'deviceid': '2', 'name': 'Outdoor', 'status': 'online', 'last_seen': '{0}'.format(time.strftime('%Y-%m-%d %H:%M:%S'))},
        # ... more devices ...
    ]
    return render(request, 'devices.html', {'devices': devices})


def about(request):
    return render(request, 'about.html')