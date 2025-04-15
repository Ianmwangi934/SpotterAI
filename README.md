# Fuel Route Planner API 🚗⛽
loom video=https://youtu.be/VMiqT4fOPNw


A Django 3.2.23 API that calculates the optimal driving route between two U.S. locations and suggests fuel stops based on a 500-mile fuel range and current fuel prices. It also returns the total fuel cost based on 10 miles per gallon efficiency.

##  Features

-  Takes **start** and **end** location input
-  Returns a route using an external routing API (minimal API calls)
-  Identifies **optimal fuel stops** from provided fuel station data
-  Calculates **total fuel cost** based on distance and fuel prices
-  Efficient logic: Only one external API call is used to fetch the route
-  [Demo video](YOUR_YOUTUBE_LINK_HERE) (Postman + Code Walkthrough)

---

## Tech Stack

- **Backend Framework:** Django 3.2.23
- **External API:** OSRM or similar free routing API
- **Fuel Data Source:** JSON file (e.g., `fuel_stations.json`)

---

## ▶️ How to Run Locally

1. **Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

#Create a virtual environment & activate it
python3 -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows

#Install dependencies
pip install -r requirements.txt

#Run the Django server
python manage.py runserver


#How to Use the API
{
  "start": "New York, NY",
  "end": "Chicago, IL"
}
Sample Response
{
  "total_distance_miles": 790.3,
  "fuel_stops": [
    {
      "name": "Fuel Station 1",
      "location": "Ohio",
      "price_per_gallon": 3.59
    }
  ],
  "total_fuel_cost_usd": 90.3,
  "route_map_url": "https://your-generated-map-link"
}

Author,
Ian Mwangi Murigu
