#api/urls.py
from django.urls import path
from ansible_api.views import ListToolsView, InstallToolsView

urlpatterns = [
    path('list-tools/', ListToolsView.as_view(), name='list_tools'),
    path('install-tools/', InstallToolsView.as_view(), name='install_tools'),
]
