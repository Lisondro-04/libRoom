from django.shortcuts import render
from pathlib import Path
from django.http import Http404
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from .serializers import (
    CharacterMetaSerializer,
    CharacterCreateSerializer,
    SectionPatchSerializer,
)
from . import utils

class CharacterViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    File-backed Characters.

    All operations touch files inside `<project>/characters`.
    """
    lookup_field = "id"
    serializer_class = CharacterMetaSerializer

    # --------------------------------------------------------------------- #
    # ───────── Index helpers ───────────────────────────────────────────── #
    # --------------------------------------------------------------------- #
    def _index(self):
        return utils._load_index()

    def _save_index(self, data):
        utils._save_index(data)

    def _find(self, cid):
        for entry in self._index():
            if entry["id"] == cid:
                return entry
        raise Http404

    # --------------------------------------------------------------------- #
    # ───────── List / Detail ───────────────────────────────────────────── #
    # --------------------------------------------------------------------- #
    def list(self, request, *args, **kwargs):
        return Response(self._index())

    def retrieve(self, request, *args, **kwargs):
        return Response(self._find(kwargs["id"]))

    # --------------------------------------------------------------------- #
    # ───────── Create ─────────────────────────────────────────────────── #
    # --------------------------------------------------------------------- #
    @extend_schema(
        request=CharacterCreateSerializer,
        responses={201: CharacterMetaSerializer},
        examples=[
            OpenApiExample(
                "Create main character",
                value={"name": "Mark", "type": "main"},
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        ser = CharacterCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.validated_data
        cid = utils._generate_id()
        md_path = utils._characters_dir() / f"{data['name']}.md"

        utils.write_markdown_skeleton(md_path, data["name"], data["type"])

        new_meta = {
            "id": cid,
            "name": data["name"],
            "type": data["type"],
            "path": str(Path("characters") / md_path.name),
        }
        idx = self._index()
        idx.append(new_meta)
        self._save_index(idx)

        return Response(new_meta, status=status.HTTP_201_CREATED)

    # --------------------------------------------------------------------- #
    # ───────── Patch a single section ──────────────────────────────────── #
    # --------------------------------------------------------------------- #
    @action(
        detail=True,
        methods=["patch"],
        url_path="section",
        serializer_class=SectionPatchSerializer,
    )
    @extend_schema(
        request=SectionPatchSerializer,
        responses={200: CharacterMetaSerializer},
        description="Overwrite the given markdown section of this character.",
    )
    def patch_section(self, request, id=None):
        char_meta = self._find(id)
        ser = SectionPatchSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        section = ser.validated_data["section"]
        content = ser.validated_data["content"]

        md_abs = utils._characters_dir() / Path(char_meta["path"]).name
        md_text = md_abs.read_text(encoding="utf-8")
        md_text = utils.replace_section(md_text, section, content)
        md_abs.write_text(md_text, encoding="utf-8")

        return Response(char_meta)

