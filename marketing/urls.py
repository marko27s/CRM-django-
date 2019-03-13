from django.urls import path
from .views import (
    dashboard, contact_lists, contacts_list, contact_list_new, contacts_list_new, contact_list_detail, edit_contact,
    email_template_list, email_template_new, email_template_edit, email_template_delete,
    email_template_detail, campaign_list, campaign_new, campaign_edit, campaign_details, campaign_delete,
    edit_contact_list, delete_contact_list
)

app_name = 'marketing'

urlpatterns = [
    path('', dashboard, name='dashboard'),

    path('cl/all/', contact_lists, name='contact_lists'),
    path('cl/edit_contact/', edit_contact, name='edit_contact'),
    path('cl/lists/', contacts_list, name='contacts_list'),
    path('cl/list/new/', contact_list_new, name='contact_list_new'),
    path('cl/list/edit/<int:pk>/', edit_contact_list, name='edit_contact_list'),
    path('cl/list/delete/<int:pk>/', delete_contact_list, name='delete_contact_list'),
    path('cl/list/cnew/', contacts_list_new, name='contacts_list_new'),
    path('cl/list/detail/', contact_list_detail, name='contact_list_detail'),

    path('et/list/', email_template_list, name='email_template_list'),
    path('et/new/', email_template_new, name='email_template_new'),
    path('et/<int:pk>/edit/', email_template_edit, name='email_template_edit'),
    path('et/<int:pk>/detail/', email_template_detail, name='email_template_detail'),
    path('et/<int:pk>/delete/', email_template_delete, name='email_template_delete'),

    path('cm/list/', campaign_list, name='campaign_list'),
    path('cm/new/', campaign_new, name='campaign_new'),
    path('cm/<int:pk>/edit/', campaign_edit, name='campaign_edit'),
    path('cm/<int:pk>/details/', campaign_details, name='campaign_details'),
    path('cm/<int:pk>/delete/', campaign_delete, name='campaign_delete')
]
