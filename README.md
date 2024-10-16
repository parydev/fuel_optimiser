# fuel_optimiser
## Fuel Optimization API

## Overview
This is a Django-based API that calculates optimal fuel stops along a driving route. It leverages a CSV dataset for fuel prices and a third-party map/routing API (e.g., Mapbox) to determine the route between two locations within the USA. The API returns a route map, optimal fuel stops based on price, and the total fuel cost for the trip.

---

## Features
- Calculates optimal fuel stops based on price
- Supports multiple stops for long routes with more than 500 miles range
- Returns the total cost of fuel based on vehicle efficiency (10 miles per gallon)
- Uses real fuel price data from a CSV file
- Integrates with Mapbox (or another map API) to retrieve route data

---

## Requirements

- Python 3.8+
- Django 3.2.23
- Django REST Framework
- Pandas
- Requests

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-project-directory>

