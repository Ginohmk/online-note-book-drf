from django.shortcuts import render
from rest_framework import response, status, exceptions, views, status as rest_status
from users import permission, authentication as user_auth
from . import serializers as note_serializer

from . import services

# For Http response Typing
from django.http import HttpResponse
import csv

#  covert html to pdf
from django.template.loader import get_template
import os

from drf_spectacular.utils import extend_schema, OpenApiParameter


# Create and Get user notes
class NoteApi(views.APIView):
    authentication_classes = (user_auth.CustomUserAuthentication,)
    permission_classes = (permission.CustomPermision,)

    @extend_schema(request=note_serializer.NoteSeralizer())
    def post(self, request):
        serializer = note_serializer.NoteSeralizer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        # create note
        serializer.instance = services.create_note(request.user, data)

        return response.Response(data=serializer.data)

    def get(self, request):
        user_note_collection = services.get_user_notes(request.user)

        serializer = note_serializer.NoteSeralizer(user_note_collection, many=True)

        return response.Response(data=serializer.data)


# Get all notes
class NotesApi(views.APIView):
    authentication_classes = (user_auth.CustomUserAuthentication,)
    permission_classes = (permission.CustomPermision,)

    def get(self, request):
        note_collection = services.get_notes()

        serializer = note_serializer.NoteSeralizer(note_collection, many=True)

        return response.Response(data=serializer.data)


class NoteRetreiveUpdateDelete(views.APIView):
    authentication_classes = (user_auth.CustomUserAuthentication,)
    permission_classes = (permission.CustomPermision,)

    def get(self, request, note_id):
        note = services.get_user_note(note_id)

        serializer = note_serializer.NoteSeralizer(note)

        return response.Response(data=serializer.data)

    def delete(self, request, note_id):
        services.delete_user_note(request.user, note_id)

        return response.Response(status=rest_status.HTTP_204_NO_CONTENT)

    @extend_schema(request=note_serializer.NoteSeralizer())
    def put(self, request, note_id):
        serializer = note_serializer.NoteSeralizer(data=request.data)
        serializer.is_valid(raise_exception=True)

        note_data = serializer.validated_data

        serializer.instance = services.update_user_note(
            request.user, note_id, note_data
        )

        return response.Response(data=serializer.data)


class UnfinishedNoteApi(views.APIView):
    authentication_classes = (user_auth.CustomUserAuthentication,)
    permission_classes = (permission.CustomPermision,)

    def get(self, request):
        notes = services.get_unfinished_note()

        serializer = note_serializer.NoteSeralizer(notes, many=True)

        return response.Response(data=serializer.data, status=status.HTTP_200_OK)


class FinishedNoteApi(views.APIView):
    authentication_classes = (user_auth.CustomUserAuthentication,)
    permission_classes = (permission.CustomPermision,)

    def get(self, request):
        notes = services.get_finished_note()

        serializer = note_serializer.NoteSeralizer(notes, many=True)

        return response.Response(data=serializer.data, status=status.HTTP_200_OK)


class OverDueNoteApi(views.APIView):
    authentication_classes = (user_auth.CustomUserAuthentication,)
    permission_classes = (permission.CustomPermision,)

    def get(self, request):
        notes = services.get_overdue_note()

        serializer = note_serializer.NoteSeralizer(notes, many=True)

        return response.Response(data=serializer.data, status=status.HTTP_200_OK)


class OrderNoteDueDateApi(views.APIView):
    authentication_classes = (user_auth.CustomUserAuthentication,)
    permission_classes = (permission.CustomPermision,)

    def get(self, request, order_arg):
        notes = services.get_order_by_due_date_note(order_arg)

        serializer = note_serializer.NoteSeralizer(notes, many=True)

        return response.Response(data=serializer.data, status=status.HTTP_200_OK)


class OrderNotePriorityApi(views.APIView):
    authentication_classes = (user_auth.CustomUserAuthentication,)
    permission_classes = (permission.CustomPermision,)

    def get(self, request, order_arg):
        notes = services.get_order_by_priority_note(order_arg)

        serializer = note_serializer.NoteSeralizer(notes, many=True)

        return response.Response(data=serializer.data, status=status.HTTP_200_OK)


class OrderNoteCreatedAtApi(views.APIView):
    authentication_classes = (user_auth.CustomUserAuthentication,)
    permission_classes = (permission.CustomPermision,)

    def get(self, request, order_arg):
        notes = services.get_order_by_created_at_note(order_arg)

        serializer = note_serializer.NoteSeralizer(notes, many=True)

        return response.Response(data=serializer.data, status=status.HTTP_200_OK)


class GenerateCSVApi(views.APIView):
    authentication_classes = (user_auth.CustomUserAuthentication,)
    permission_classes = (permission.CustomPermision,)

    @extend_schema(responses=note_serializer.NoteSeralizer)
    def get(self, request):
        notes = services.get_notes()

        serializer = note_serializer.NoteSeralizer(notes, many=True)

        response = HttpResponse(
            content="text/csv",
        )

        response["Content-Disposition"] = 'attachment; filename="notes.csv"'

        writer = csv.writer(response)

        writer.writerow(
            [
                "id",
                "title",
                "content",
                "created_at",
                "due_date",
                "priority",
                "is_complete",
                "user_id",
                "user_first_name",
                "user_last_name",
                "user_email",
            ]
        )

        for note in serializer.data:
            print(note.get("user").get("first_name"), "Data")
            writer.writerow(
                [
                    note.get("id"),
                    note.get("title"),
                    note.get("content"),
                    note.get("created_at"),
                    note.get("due_date"),
                    note.get("priority"),
                    note.get("is_complete"),
                    note.get("user").get("user_id"),
                    note.get("user").get("first_name"),
                    note.get("user").get("last_name"),
                    note.get("user").get("email"),
                ]
            )

        return response


class GeneratePDFApi(views.APIView):
    authentication_classes = (user_auth.CustomUserAuthentication,)
    permission_classes = (permission.CustomPermision,)

    def post(self, request):
        data = services.generate_pdf_html()

        # print(f"{os.getcwd()}/templates/notes.html")

        # path = os.getcwd()

        template = get_template("notes.html")

        html = template.render(data)

        print(html, "HTML")

        # pdf = pdfkit.from_string("Hello world", False)

        # response = HttpResponse(pdf, content="application/pdf")

        # response["Content-Disposition"] = 'attachment; filename="notes.pdf"'

        return response.Response(data="Hello Here")
