import httplib2

from django.conf import settings

from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from apiclient import errors

from address_list import exceptions

def save_location(latitude, longitude):
    scopes = [settings.FUSION_TABLES_SCOPE]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        settings.SERVICE_ACCOUNT_KEY_FILE, scopes)

    http = credentials.authorize(httplib2.Http())
    service = build("fusiontables", "v1", http=http)

    try:
        service.query().sql(sql=
            "INSERT INTO {table_id}(Latitude, Longitude ) VALUES({lat}, {lng})"
            .format(
                table_id=settings.FUSION_TABLE_ID,
                lat=latitude,
                lng=longitude
            )).execute()
    except errors.Error as ex:
        raise exceptions.FusionTablesException(ex)


def get_address(latitude, longitude):
    return {
        "Google": get_google_geocoder,
        "Nominatim": get_nominatim_geocoder,
    }[settings.GEOCODER](latitude, longitude)


def get_google_geocoder(latitude, longitude):
    import geocoder
    data = geocoder.google([latitude, longitude], method='reverse')
    return data.address


def get_nominatim_geocoder(latitude, longitude):
    from geopy.geocoders import Nominatim
    from geopy.exc import GeopyError
    geolocator = Nominatim()

    try:
        location = geolocator.reverse("{}, {}".format(latitude, longitude))
    except GeopyError as ex:
        raise exceptions.GeoCodeException(ex)

    if location.raw["address"].get("house_number"):
        return location.address
