from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer


class SnippetList(viewsets.ModelViewSet):
    """
    @swg_begin
    path: /snippets
    method: get
    summary: This endpoint lists the snippets
    description: The `highlight` field presents a hyperlink to the highlighted HTML
      representation of the code snippet.
      The **owner** of the code snippet may update or delete instances
      of the code snippet.
      Try it yourself by logging in as one of these four users **amy**, **max**,
      **jose** or **aziz**.  The passwords are the same as the usernames.
    responses:
      default:
        description: A list is returned
        schema:
          $ref: '#/definitions/Snippet'
    @swg_end
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get(self, request, format=None):
        queryset = Snippet.objects.all()
        return SnippetSerializer(queryset, read_only=True, many=True)


class SnippetCreate(viewsets.ModelViewSet):

    def post(self, request, format=None):
        """
        @swg_begin
        path: /snippets
        method: post
        summary: This endpoint creates the snippets
        description: Create a snippet
        parameters:
          - name: created
            in: formData
            type: string
            format: date-time
          - name: title
            type: string
            format: char[100]
            in: formData
          - name: code
            type: string
            in: formData
          - name: linenos
            type: boolean
            in: formData
          - name: language
            type: string
            format: char[100]
            in: formData
          - name: style
            type: string
            format: char[100]
            in: formData
        responses:
          default:
            description: A list is returned
            schema:
              $ref: '#/definitions/Snippet'
        @swg_end
        """
