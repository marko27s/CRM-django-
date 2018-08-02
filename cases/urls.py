from django.urls import path
from cases.views import (
    CasesListView, CreateCaseView, CaseDetailView, UpdateCaseView, RemoveCaseView,
    CloseCaseView, SelectContactsView, GetCasesView, AddCommentView,
    UpdateCommentView, DeleteCommentView)

app_name = 'cases'

urlpatterns = [
    path('list/', CasesListView.as_view(), name='list'),
    path('create/', CreateCaseView.as_view(), name='add_case'),
    path('<int:pk>/view/', CaseDetailView.as_view(), name="view_case"),
    path('<int:pk>/edit_case/', UpdateCaseView.as_view(), name="edit_case"),
    path('<int:case_id>/remove/', RemoveCaseView.as_view(), name="remove_case"),

    path('close_case/', CloseCaseView.as_view(), name="close_case"),
    path('select_contacts/', SelectContactsView.as_view(), name="select_contacts"),
    path('get/list/', GetCasesView.as_view(), name="get_cases"),

    path('comment/add/', AddCommentView.as_view(), name="add_comment"),
    path('comment/edit/', UpdateCommentView.as_view(), name="edit_comment"),
    path('comment/remove/', DeleteCommentView.as_view(), name="remove_comment"),
]
