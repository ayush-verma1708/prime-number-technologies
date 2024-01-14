from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import Restaurant , MenuItem

import json
import pandas as pd


def home(request):
    restaurants = Restaurant.objects.all()
    restaurants_items = MenuItem.objects.all()

    context = {'restaurants': restaurants,
               'restaurants_items':restaurants_items,
    }
    return render(request, 'restaurant_list.html', context)
    
def update_database_from_csv(request):
    csv_path = 'base/restaurants_small.csv'
    
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        menu_data = json.loads(row['items'])

        restaurant, created = Restaurant.objects.get_or_create(
            id=row['id'],
            name=row['name'],
            location=row['location']
        )

        for item, price in menu_data.items():
            menu_item, created = MenuItem.objects.get_or_create(name=item, price=price)

            restaurant.items.add(menu_item)

    restaurants = Restaurant.objects.all()

    Restaurant.objects.bulk_update(restaurants, ['items'])

    return HttpResponse("Success")

def search_results(request):
    query = request.GET.get('query', '')

    # Perform case-insensitive partial match search on the 'name' field of the MenuItem model
    matching_items = MenuItem.objects.filter(name__icontains=query)

    # Retrieve the restaurants associated with the matching items
    restaurants_with_matching_items = Restaurant.objects.filter(items__in=matching_items)

    context = {
        'query': query,
        'restaurants': restaurants_with_matching_items,
        'matching_items': matching_items,
    }

    return render(request, 'search_results.html', context)