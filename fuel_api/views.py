import math
import pandas as pd
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

# Load fuel prices from CSV
def load_fuel_prices():
    csv_path = f"{settings.BASE_DIR}/fuel_prices/fuel-prices-for-be-assessment.csv"
    fuel_data = pd.read_csv(csv_path)

    # Strip whitespace from column names in case of formatting issues
    fuel_data.columns = fuel_data.columns.str.strip()

    # Standardize column names to avoid mismatches
    if 'Retail Price' in fuel_data.columns:
        fuel_data.rename(columns={'Retail Price': 'price'}, inplace=True)

    # Remove rows with missing or non-numeric price values
    fuel_data = fuel_data[pd.to_numeric(fuel_data['price'], errors='coerce').notnull()]
    return fuel_data


# Fetch route using Mapbox API
MAPBOX_API_KEY = 'your_mapbox_api_key_here'

def get_route(start, end):
    # Call Mapbox API to get the route between start and end points
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{start};{end}?access_token={MAPBOX_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Calculate the fuel stops along the route and total cost
def calculate_fuel_stops(fuel_data):
    # total_distance = route['routes'][0]['distance'] / 1609.34  # Convert meters to miles
    total_distance = 70
    fuel_needed = total_distance / 10  # Assuming 10 miles per gallon
    total_stops = math.ceil(total_distance / 500)

    fuel_stops = []
    stop_distance = 0
    total_cost = 0
    for i in range(total_stops):
        stop_distance += 500 if stop_distance + 500 < total_distance else total_distance - stop_distance
        # Find the closest fuel station from the fuel_data (filter by distance, prices)
        stop = find_optimal_fuel_stop(stop_distance, fuel_data)
        total_cost += stop['price'] * (500 / 10)
        fuel_stops.append(stop)

    return fuel_stops, total_cost

# Helper function to find the optimal fuel stop
def find_optimal_fuel_stop(distance, fuel_data):
    # 'price' is now the standardized column
    price_column = 'price'

    # Since there is no 'distance' column, we will only sort by price for the optimal stop
    print(f"Warning: 'distance' column not found in fuel data. Using {price_column} as the only factor.")
    return fuel_data.sort_values(by=price_column).iloc[0].to_dict()


# API to return route along with optimal fuel stops and total cost
@api_view(['GET'])
def route_with_fuel_stops(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    # if not start or not end:
    #     return Response({'error': 'Start and End locations must be provided'}, status=400)
    #
    # # Get the route from Mapbox
    # route = get_route(start, end)
    # if not route:
    #     return Response({'error': 'Unable to fetch route from Mapbox API'}, status=500)

    # Load fuel prices data
    fuel_data = load_fuel_prices()

    # Calculate fuel stops and cost
    fuel_stops, total_cost = calculate_fuel_stops(fuel_data)

    return Response({
        # 'route': route,
        'fuel_stops': fuel_stops,
        'total_cost': total_cost
    })

