from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import path,include
from assets_management.models import Asset
from customer.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from customadmin.decorators import allowed_users, admin_only, unauthenticated_user

from .forms import AssetForm, updatedata
from django.conf import settings
from django.conf.urls.static import static

import matplotlib.pyplot as plt
import io
import base64


@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def add_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Asset was Added successfully!')
            return redirect('assets')
    else:
        form = AssetForm()
    return render(request, 'add_asset.html', {'form': form})


@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def list_assets(request):
    query = request.GET.get('q')
    assets = Asset.objects.all().order_by('id').values()
    if query:
        assets = assets.filter(serial_number__icontains=query) 
    
    # Retrieve the assets once after the filtering
    assets_list = Asset.objects.all().order_by('purchase_date')
    if query:
        assets_list = assets_list.filter(serial_number__icontains=query)
    dates = [asset.purchase_date.strftime('%Y-%m-%d') for asset in assets_list]
    prices = [asset.purchase_price for asset in assets_list]

    # Create the line chart
    plt.plot(dates, prices)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Asset Purchase Prices Over Time')

    # Save the chart to a file-like object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the chart image to a base64-encoded string
    line_chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Close the plot
    plt.close()

    return render(request, 'asset_list.html', {'assets': assets, 'query': query, 'line_chart_image': line_chart_image})


@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def update_data(request, pk):
    data = Asset.objects.get(id=pk)
    if request.method == 'POST':
        form = updatedata(request.POST, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, f'Asset with ID "{data.id}" was updated successfully!')
            return redirect('assets')
    else:
        form = updatedata(instance=data)
    return render(request, 'update_asset.html', {'form': form})


@login_required(login_url="loginview")
@allowed_users(allowed_roles=['admin'])
def delete_data(request, id):
    data = Asset.objects.get(id=id)
    data.delete()
    messages.success(request,'Asset was Deleted successfully!')
    return redirect('assets')

