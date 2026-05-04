from django.urls import path
from . import views

urlpatterns = [
    # path('register/', views.registerPage, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("", views.home, name="home"),
    # path('user/', views.userPage, name="user-page" ),
    path("project_list/", views.project_list, name="project_list"),
    path("project_detail/view/<int:pk>/", views.project_detail, name="project_detail"),
    path(
        "project_detail/delete/<int:pk>/", views.delete_project, name="delete_project"
    ),
    path("task/toggle/<int:pk>/", views.toggle_task, name="toggle_task"),
    # path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    # path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    # path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
]
