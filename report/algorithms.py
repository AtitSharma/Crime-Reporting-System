from math import radians, cos, sin, asin, sqrt
from decimal import Decimal

from report.models import PoliceStation

# Haversine formula to calculate distance between two lat/lon points in kilometers

## d = 2 * r * arcsin( sqrt( sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2) ) )

def haversine(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    r = 6371  # Radius of Earth in kilometers
    return c * r




def nearest_police_station(user_lat,user_lon):
    stations = PoliceStation.objects.all()

    try :
        nearest_station = min(
            stations,
            key=lambda station: haversine(Decimal(user_lat), Decimal(user_lon), station.latitude, station.longitude)
        )

        return nearest_station
    except Exception:
        return None


