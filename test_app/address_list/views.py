from django.views.generic import TemplateView
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST as BAD_REQUEST

from address_list import utils, models, serializers, exceptions


class IndexView(TemplateView):
    template_name = "address_list/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['map_center_x'] = settings.MAP_CENTER_X
        context['map_center_y'] = settings.MAP_CENTER_Y
        context['table_id'] = settings.FUSION_TABLE_ID
        return context

class AddressView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.AddressSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=BAD_REQUEST)

        try:
            address = utils.get_address(
                serializer.validated_data["latitude"],
                serializer.validated_data["longitude"]
            )

            if not address:
                return Response("Can't find address", status=BAD_REQUEST)
        except exceptions.GeoCodeException as ex:
            return Response(ex.message, status=BAD_REQUEST)

        serializer.validated_data["address"] = address
        serializer.save()

        try:
            utils.save_location(
                serializer.validated_data["latitude"],
                serializer.validated_data["longitude"]
            )
        except exceptions.FusionTablesException as ex:
            return Response(
                "Can't save to fusion tables. Error {}".format(ex.message),
                status=BAD_REQUEST
            )

        return Response(serializer.validated_data)

    def get(self, request, *args, **kwargs):
        address_list = models.Address.objects.all()
        serializer = serializers.AddressSerializer(address_list, many=True)
        return Response(serializer.data)
