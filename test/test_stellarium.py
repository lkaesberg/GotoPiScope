import requests
import json

def get_stellarium_coordinates(object_name = None):
    url = f'http://localhost:8090/api/objects/info'
    params = {
        'format': 'json',
        'name': object_name
    }
    response = requests.get(url, params=params)
    response_json = response.json()
    print(response_json)
    az = response_json['azimuth']
    alt = response_json['altitude']
    print(response_json["localized-name"])
    return az, alt

if __name__ == '__main__':
    # Test
    az, alt = get_stellarium_coordinates()
    print(f'Azimuth: {az}, Altitude: {alt}')
