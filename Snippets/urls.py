from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='snippets_add'),
    path('snippets/list', views.snippets_page, name='snippets_list'),
    # path('snippets/create', views.create_snippet, name='create_snippet'),
    path('snippet/<int:snippet_id>', views.snippet_detail, name='snippet_detail'),
    path('snippet/<int:snippet_id>/delete', views.snippet_delete, name='snippet_delete'),
    path('snippet/<int:snippet_id>/edit', views.snippet_edit, name='snippet_edit'),
    path('snippet/my', views.my_snippets, name='my_snippets'),
    path('auth/register', views.create_user, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
