"""Views for 'info' endpoints of 'Api' application v1."""

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.v1.info.serializers import IndustrySerializer
from companies.models import Industry


@api_view()
@authentication_classes(())
@permission_classes((AllowAny,))
def industries(request):
    """URL request handler for the industries/ endpoint."""
    serializer = IndustrySerializer(Industry.objects.all(), many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
