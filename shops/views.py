import logging
from django.views import generic
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Shop
import requests


class Home(generic.ListView):
    model = Shop
    context_object_name = "shops"
    template_name = "shops/index.html"

    def get_user_location_coordinates(self, user_location_str):
        # Default coordinates
        longitude = 105.804817
        latitude = 21.028511

        if user_location_str:
            # Use Nominatim for geocoding
            nominatim_url = f'https://nominatim.openstreetmap.org/search?q={user_location_str}&format=json&limit=1'

            try:
                response = requests.get(nominatim_url)
                response.raise_for_status()  # Check for errors in the response

                data = response.json()
                if data and 'lat' in data[0] and 'lon' in data[0]:
                    # Extract coordinates from the first result
                    latitude = float(data[0]['lat'])
                    longitude = float(data[0]['lon'])
                    logging.info(f"Latitude: {latitude}, Longitude: {longitude}")
            except requests.RequestException as e:
                logging.error(f"Error retrieving coordinates: {e}")

        return Point(longitude, latitude, srid=4326)

    def get_queryset(self):
        # Get user location from the query parameters
        user_location_str = self.request.GET.get("location")

        user_location = self.get_user_location_coordinates(user_location_str)

        # Query for nearby shops
        queryset = Shop.objects.prefetch_related(
            'items'  # Prefetch related items
        ).annotate(
            distance=Distance("location", user_location)
        ).order_by("distance")[:6]

        return queryset


    def post(self, request, *args, **kwargs):
        user_location_str = self.request.POST.get("location")

        # Check if the "Use Default Location" button is clicked
        if 'use_default_location' in self.request.POST:
            user_location_str = ""  # Set user_location_str to an empty string to use the default location

        logging.info(f"User Location in POST method: {user_location_str}")

        # Redirect to the same view with the form data
        return HttpResponseRedirect(request.path_info + f"?location={user_location_str}")



def home(request):
    if request.method == 'POST':
        # If the form is submitted, render the Home view with the updated queryset
        return Home.as_view()(request)
    else:
        # If it's a GET request, render the form
        return render(request, 'shops/index.html')



def shop_detail(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    items = shop.items.all()
    return render(request, 'shops/shop_detail.html', {'shop': shop, 'items': items})
