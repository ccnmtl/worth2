import os.path

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.urls import path
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
    url(r'^accounts/',
        include('django_registration.backends.activation.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    path('cas/login', cas_views.LoginView.as_view(),
         name='cas_ng_login'),
    path('cas/logout', cas_views.LogoutView.as_view(),
         name='cas_ng_logout'),
    url(r'^api/', include(rest_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^$', views.DashboardView.as_view(), name='root'),
    url(r'^admin/', admin.site.urls),
    url(r'^_impersonate/', include('impersonate.urls')),
    url(r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'^uploads/(?P<path>.*)$',
        django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^pagetree/', include('pagetree.urls')),
    url(r'^quizblock/', include('quizblock.urls')),
    url(r'^pages/edit/(?P<path>.*)$',
        user_passes_test(lambda u: u.is_superuser)(
            EditView.as_view(
                hierarchy_name="main",
                hierarchy_base="/pages/")),
        {}, 'edit-page'),
    url(r'^pages/(?P<path>.*)$', views.ParticipantSessionPageView.as_view(
        hierarchy_name="main",
        hierarchy_base="/pages/")),

    url(r'^journal/(?P<session_num>\d+)/$',
        views.JournalView.as_view(), name='journal'),

    # Social Support Network Map activity
    url(r'^ssnm/api/', include(ssnm_rest_router.urls)),

    url('^epub/$', user_passes_test(lambda u: u.is_superuser)(
        EpubExporterView.as_view()), name='epub-export'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
