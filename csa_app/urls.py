from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page, name='csa_app_home'),
    path('redirect-form1/', views.form_1, name='csa_app_form_1'),
    path('redirect-form1-parent-only/', views.form1_parent_only, name='csa_app_form_1_parent_only'),
    path('redirect-form1-parent-and-children/', views.form1_parent_and_children, name='csa_app_form_1_parent_and_children'),
    path('redirect-form1-add-children/', views.form1_add_children, name='csa_app_form_1_add_children'),
    path('redirect-home_page/', views.home_page, name='csa_app_redirect_home_page'),
    path('redirect-dummy_page/', views.dummy_page, name='csa_app_redirect_dummy_page'),
    path('redirect-forms_2_5/', views.forms_2_5, name='csa_app_redirect_forms_2_5'),
    path('redirect-form2/', views.form2, name='csa_app_redirect_form2'),
    path('redirect-forms_1_5/', views.forms_1_5, name='csa_app_redirect_forms_1_5'),
    #path('dummy_page/', views.dummy_page, name='csa_app_dummy'),
]
