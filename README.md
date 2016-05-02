An example of [Google Fusion Tables](https://support.google.com/fusiontables/answer/2571232)
client in form of Django application. This app uses Google Fusion tables as
another backend (altogether with regular db) and one of available geocoders
(Google Geocoder or Nominatim).

* `SERVICE_ACCOUNT_KEY_FILE` an authentication key for fusion tables
* `FUSION_TABLE_ID` fusion table id
* `MAP_CENTER_X`/ `MAP_CENTER_Y` an initial map center
* `GEOCODER` - a name of required geocoder
