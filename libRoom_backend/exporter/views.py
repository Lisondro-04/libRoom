from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializers import ExportConfigSerializer, ExportResponseSerializer
from .export_engine import export_project

class ExportProjectView(APIView):
    @extend_schema(
        summary="Exportar contenido del proyecto",
        description="""
Exporta el contenido completo del proyecto (novela o cuento) en el formato especificado.

### Estructura compatible:

- **Novela**: capítulos con escenas anidadas.
- **Cuento**: solo escenas, sin capítulos (`include_chapters: false`).

### Parámetros principales:

- `include_chapters`: si es `false`, se asume un cuento sin capítulos.
- `status_filter`: lista de estados válidos para exportar (por ejemplo, `[2, 3]`).
- `text_transformations`: reemplazos personalizados, comillas, guiones, etc.
- `include_toc`: genera tabla de contenidos basada en la estructura jerárquica.

        """,
        request=ExportConfigSerializer,
        responses={200: ExportResponseSerializer}
    )
    def post(self, request):
        config = request.data
        try:
            output_path = export_project(config)
            return Response({
                "success": True,
                "message": "Exportación completada.",
                "output_path": output_path
            })
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Error durante la exportación: {str(e)}",
                "output_path": None
            }, status=500)
