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
    

# def item_entry(request):
#     csv_path = 'restaurants_small.csv'
#     df = pd.read_csv(csv_path)
#     first_row_item = df['items'].iloc[0]
#     for i, row in df.iterrows():

#         menu_data = json.loads(row['items'])

#         # restaurant = Restaurant.objects.get(id=restaurant_ids[i])
#         for item, price in menu_data.items():
#         # Create a new MenuItem instance
#             menu_item = MenuItem.objects.create(name=item, price=price)

#         # Add the menu_item to the restaurant's items
#             restaurant.items.add(menu_item)   


# views.py
from django.shortcuts import render
from .models import MenuItem, Restaurant
import json
import pandas as pd

def update_database_from_csv(request):
    # Specify the path to your CSV file
    csv_path = 'base/restaurants_small.csv'
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Iterate over the rows in the DataFrame
    for _, row in df.iterrows():
        # Parse the JSON data from the 'items' column
        menu_data = json.loads(row['items'])

        # Create a new Restaurant instance
        restaurant, created = Restaurant.objects.get_or_create(
            id=row['id'],
            name=row['name'],
            location=row['location']
        )

        # Iterate over items in the menu_data and create MenuItem instances
        for item, price in menu_data.items():
            # Create a new MenuItem instance
            menu_item, created = MenuItem.objects.get_or_create(name=item, price=price)

            # Add the menu_item to the restaurant's items
            restaurant.items.add(menu_item)

    # Get all restaurants after the updates
    restaurants = Restaurant.objects.all()

    # Make sure to save the changes to the database
    Restaurant.objects.bulk_update(restaurants, ['items'])

    # You can customize the response based on your needs
    return HttpResponse("Success")
