import requests


def get_ip_location(ip):
    """
    Get approximate location information
    from public IP address.
    """

    try:
        url = f"https://ipapi.co/{ip}/json/"

        response = requests.get(
            url,
            timeout=5
        )

        data = response.json()

        return {
            "country": data.get("country_name", "Unknown"),
            "city": data.get("city", "Unknown"),
            "region": data.get("region", "Unknown"),
            "latitude": data.get("latitude", None),
            "longitude": data.get("longitude", None)
        }

    except Exception:

        return {
            "country": "Unknown",
            "city": "Unknown",
            "region": "Unknown",
            "latitude": None,
            "longitude": None
        }



def add_geo_information(df):

    locations = []

    for ip in df["source_ip"]:
        locations.append(
            get_ip_location(ip)
        )

    geo_df = df.copy()

    geo_df["country"] = [
        x["country"] for x in locations
    ]

    geo_df["city"] = [
        x["city"] for x in locations
    ]

    geo_df["latitude"] = [
        x["latitude"] for x in locations
    ]

    geo_df["longitude"] = [
        x["longitude"] for x in locations
    ]

    return geo_df
