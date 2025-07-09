from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.utils import extend_schema
from .serializers import ExportConfigSerializer, ExportResponseSerializer
from .export_engine import export_project

class ExportProjectView(APIView):
    @extend_schema(
        summary="Exportar contenido del proyecto",
        description="Exporta el contenido del proyecto en el formato especificado. con filtros de estado y transformaciones personalizadas",
        request=ExportConfigSerializer,
        responses={200: ExportConfigSerializer}
    )

    def post(self, request):
        export_config = request.data
        output_path = export_project(export_config)
        return Response({
            "success": True,
            "message": "Exportación completada",
            "output_path": output_path
        })

