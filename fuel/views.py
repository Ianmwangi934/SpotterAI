from django.shortcuts import render
import pandas as pd
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie



@method_decorator(csrf_exempt, name='dispatch')
class RouteAPIView(APIView):
    def post(self, request):
        start = request.data.get("start")
        end = request.data.get("end")

        if not start or not end:
            return Response({"error": "Please provide both start and end location"}, status=status.HTTP_400_BAD_REQUEST)

        # Get route and distance using ORS
        try:
            route_data = self.get_route(start, end)
            total_distance = route_data['features'][0]['properties']['segments'][0]['distance'] / 1609.34  # meters to miles
        except Exception as e:
            return Response({"error": f"Failed to retrieve route: {str(e)}"}, status=500)

        # Load fuel price data
        try:
            df = pd.read_csv("spotter.csv")
        except Exception as e:
            return Response({"error": f"Failed to load fuel prices: {str(e)}"}, status=500)

        # Calculate fuel stops
        stops, total_cost = self.calculate_fuel_stops(df, total_distance)

        # Final response
        return Response({
            "route_distance_miles": round(total_distance, 2),
            "fuel_stops": stops,
            "total_fuel_cost": round(total_cost, 2),
            "note": "Fuel stops calculated assuming 500-mile range and 10 mpg efficiency."
        })

    def get_route(self, start, end):
        api_key = settings.ORS_API_KEY
        headers = {'Authorization': api_key}
        geocode_url = "https://api.openrouteservice.org/geocode/search"
        directions_url = "https://api.openrouteservice.org/v2/directions/driving-car"

        # Geocode start and end
        start_coords = requests.get(geocode_url, params={"text": start},headers=headers).json()['features'][0]['geometry']['coordinates']
        end_coords = requests.get(geocode_url, params={"text": end},headers=headers).json()['features'][0]['geometry']['coordinates']

        # Get route
        route_url = f"{directions_url}?start={start_coords[0]},{start_coords[1]}&end={end_coords[0]},{end_coords[1]}"
        response = requests.get(route_url, headers=headers)
        return response.json()

    def calculate_fuel_stops(self, df, total_distance):
        stops = []
        cost = 0
        miles_remaining = total_distance
        index = 0

        while miles_remaining > 0:
            fuel_range = min(miles_remaining, 500)

            if index >= len(df):
                break

            row = df.iloc[index]
            try:
                price = float(row.get('Retail Price', 3.50))
            except:
                price = 3.50

            # Match case-sensitive column name
            location = row.get('City') or "Unknown"

            gallons_needed = fuel_range / 10
            stop_cost = gallons_needed * price

            stops.append({
                "location": location,
                "price_per_gallon": round(price, 2),
                "miles_from_start": round(total_distance - miles_remaining, 2),
                "fuel_cost": round(stop_cost, 2)
            })

            cost += stop_cost
            miles_remaining -= 500
            index += 1

        return stops, cost
@method_decorator(ensure_csrf_cookie, name='dispatch')
class FuelMapView(View):
    def get(self, request):
        return render(request, "fuel/map.html")

class RouteInputeView(View):
    def get(self, request):
        return render(request, "fuel/route_input.html")

    def post(self, request):
        start = request.POST.get("start")
        end = request.POST.get("end")

        #Redirecting to map with query params
        return render(request, "fuel/map.html",{"start":start, "end":end})

