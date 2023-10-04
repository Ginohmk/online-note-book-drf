import dataclasses
import datetime
from rest_framework import exceptions
from users import services as user_services
from . import models

# For making html
from django.shortcuts import render
from django.template import Template, Context

# To validate uuid passed in api
from uuid import UUID

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from note.models import Note
    from users.models import User


@dataclasses.dataclass
class NoteDataClass:
    title: str
    due_date: datetime.datetime
    content: str
    priority: int
    id: str = None
    created_at: datetime.datetime = None
    user: user_services.UserDataClass = None
    is_complete: bool = False

    @classmethod
    def from_instance(cls, note: "Note") -> "NoteDataClass":
        return cls(
            id=note.id,
            title=note.title,
            content=note.content,
            due_date=note.due_date,
            is_complete=note.is_complete,
            priority=note.priority,
            created_at=note.created_at,
            user=note.user,
        )


####### Helper Function #######
def check_valid_uuid(id):
    try:
        UUID(id, version=4)

    except:
        raise exceptions.ValidationError("Id is not valid")


###### Api Essentials functions ########


def create_note(user, note_dc: "NoteDataClass") -> "NoteDataClass":
    instance = models.Note(
        title=note_dc.title,
        due_date=note_dc.due_date,
        content=note_dc.content,
        priority=note_dc.priority,
        user=user,
    )

    instance.save()

    return NoteDataClass.from_instance(instance)


def get_user_notes(user: "User") -> list["NoteDataClass"]:
    user_note = models.Note.objects.filter(user=user)

    return [NoteDataClass.from_instance(single_note) for single_note in user_note]


def get_notes() -> list["NoteDataClass"]:
    notes = models.Note.objects.all()

    return [NoteDataClass.from_instance(single_note) for single_note in notes]


def get_user_note(note_id: str) -> "NoteDataClass":
    check_valid_uuid(note_id)

    note = models.Note.objects.filter(id=note_id).first()

    if not note:
        raise exceptions.NotFound("Note Does not exist")

    return NoteDataClass.from_instance(note)


def delete_user_note(user: "User", note_id: str) -> None:
    check_valid_uuid(note_id)

    note = models.Note.objects.filter(id=note_id).first()

    if not note:
        raise exceptions.NotFound("Note Does not exist")

    if note.user.id != user.id:
        raise exceptions.PermissionDenied("Unauthorized")

    note.delete()


def update_user_note(
    user: "User", note_id: str, note_data: "NoteDataClass"
) -> "NoteDataClass":
    check_valid_uuid(note_id)

    note = models.Note.objects.filter(id=note_id).first()

    if not note:
        raise exceptions.NotFound("Note Does not exist")

    if note.user.id != user.id:
        raise exceptions.PermissionDenied("Unauthorized")

    note.title = note_data.title
    note.content = note_data.content
    note.due_date = note_data.due_date
    note.priority = note_data.priority
    note.is_complete = note_data.is_complete

    note.save()

    return NoteDataClass.from_instance(note)


def get_unfinished_note() -> "NoteDataClass":
    notes = models.Note.objects.filter(is_complete=False)

    return [NoteDataClass.from_instance(single_note) for single_note in notes]


def get_finished_note() -> list["NoteDataClass"]:
    notes = models.Note.objects.filter(is_complete=True)

    return [NoteDataClass.from_instance(single_note) for single_note in notes]


def get_overdue_note() -> list["NoteDataClass"]:
    pass

    current_date = datetime.datetime.now()

    notes = models.Note.objects.filter(due_date__lte=current_date)

    return [NoteDataClass.from_instance(single_note) for single_note in notes]


def get_order_by_due_date_note(order_arg: str) -> list["NoteDataClass"]:
    sort_arg_value = "due_date" if order_arg.lower() == "asc" else "-due_date"

    notes = models.Note.objects.all().order_by(sort_arg_value)

    return [NoteDataClass.from_instance(single_note) for single_note in notes]


def get_order_by_priority_note(order_arg: str) -> list["NoteDataClass"]:
    sort_arg_value = "priority" if order_arg.lower() == "asc" else "-priority"

    notes = models.Note.objects.all().order_by(sort_arg_value)

    return [NoteDataClass.from_instance(single_note) for single_note in notes]


def get_order_by_created_at_note(order_arg: str) -> list["NoteDataClass"]:
    sort_arg_value = "created_at" if order_arg.lower() == "asc" else "-created_at"

    notes = models.Note.objects.all().order_by(sort_arg_value)

    return [NoteDataClass.from_instance(single_note) for single_note in notes]


def generate_pdf_html() -> object:
    # Get all notes
    notes = get_notes()

    html_data = {}

    for index, note in enumerate(notes):
        html_data[index] = {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at,
            "due_date": note.due_date,
            "is_complete": note.is_complete,
            "priority": note.priority,
            "user_id": note.user.id,
            "first_name": note.user.first_name,
            "last_name": note.user.last_name,
            "email": note.user.email,
        }

        """
        EXAMPLE DATA

            context = {
            0: {
                    "id": UUID("ebfe6d73-6e7d-40e1-9e94-95d155680ebf"),
                    "title": "New Create",
                    "content": "New",
                    "created_at": datetime.datetime(
                        2023, 9, 25, 13, 26, 22, 240071, tzinfo=datetime.timezone.utc
                    ),
                    "due_date": datetime.datetime(
                        2023, 9, 23, 20, 45, 37, 13440, tzinfo=datetime.timezone.utc
                    ),
                    "is_complete": False,
                    "priority": 3,
                    "user_id": UUID("49b052c8-7677-44be-88b1-6c15ebd03f9f"),
                    "first_name": "Larry",
                    "last_name": "Mall",
                    "email": "michotall95@gmail.com",

                },
            }
        """

    context = {"note_lists": html_data}

    print(context, "Cntext")

    return context
