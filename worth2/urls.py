import os.path

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.urls import include, path, re_path
from django.views.generic import TemplateView
import django.views.static
from django_cas_ng import views as cas_views
from pagetree.generic.views import EditView
from pagetreeepub.views import EpubExporterView
from rest_framework import routers
from worth2.main import apiviews, views
from worth2.ssnm import apiviews as ssnm_apiviews


site_media_root = os.path.join(os.path.dirname(__file__), "../media")

rest_router = routers.DefaultRouter()
rest_router.register(r'watched_videos', apiviews.WatchedVideoViewSet,
                     basename='watched_video')

ssnm_rest_router = routers.DefaultRouter(trailing_slash=False)
ssnm_rest_router.register(r'supporters', ssnm_apiviews.SupporterViewSet,
                          basename='supporter')

urlpatterns = [
    path('accounts/',
         include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cas/login', cas_views.LoginView.as_view(),
         name='cas_ng_login'),
    path('cas/logout', cas_views.LogoutView.as_view(),
         name='cas_ng_logout'),
    path('api/', include(rest_router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('', views.DashboardView.as_view(), name='root'),
    path('admin/', admin.site.urls),
    path('_impersonate/', include('impersonate.urls')),
    path('stats/$', TemplateView.as_view(template_name="stats.html")),
    path('smoketest/', include('smoketest.urls')),
    re_path(r'^uploads/(?P<path>.*)$',
            django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),

    path('pagetree/', include('pagetree.urls')),
    path('quizblock/', include('quizblock.urls')),
    re_path(r'^pages/edit/(?P<path>.*)$',
            user_passes_test(lambda u: u.is_superuser)(
                EditView.as_view(
                    hierarchy_name="main",
                    hierarchy_base="/pages/")),
            {}, 'edit-page'),
    re_path(r'^pages/(?P<path>.*)$', views.ParticipantSessionPageView.as_view(
        hierarchy_name="main",
        hierarchy_base="/pages/")),

    re_path(r'^journal/(?P<session_num>\d+)/$',
            views.JournalView.as_view(), name='journal'),

    # Social Support Network Map activity
    path('ssnm/api/', include(ssnm_rest_router.urls)),

    path('epub/', user_passes_test(lambda u: u.is_superuser)(
        EpubExporterView.as_view()), name='epub-export'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
