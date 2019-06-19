import os.path
import django.views.static

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.views.generic import TemplateView

from pagetree.generic.views import EditView, InstructorView
from pagetreeepub.views import EpubExporterView

from rest_framework import routers

from worth2.main import apiviews, auth, views
from worth2.ssnm import apiviews as ssnm_apiviews


site_media_root = os.path.join(os.path.dirname(__file__), "../media")

auth_urls = url(r'^accounts/', include('django.contrib.auth.urls'))
if hasattr(settings, 'CAS_BASE'):
    auth_urls = url(r'^accounts/', include('djangowind.urls'))


rest_router = routers.DefaultRouter()
rest_router.register(r'participants', apiviews.ParticipantViewSet)
rest_router.register(r'watched_videos', apiviews.WatchedVideoViewSet,
                     base_name='watched_video')

ssnm_rest_router = routers.DefaultRouter(trailing_slash=False)
ssnm_rest_router.register(r'supporters', ssnm_apiviews.SupporterViewSet,
                          base_name='supporter')

urlpatterns = [
    auth_urls,
    url(r'^api/', include(rest_router.urls)),
    url(r'^api/login_check/', apiviews.LoginCheck.as_view(),
        name='api-login-check'),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^registration/', include('registration.backends.default.urls')),
    url(r'^$', views.DashboardView.as_view(), name='root'),
    url(r'^admin/', admin.site.urls),
    url(r'^_impersonate/', include('impersonate.urls')),
    url(r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'infranil/', include('infranil.urls')),
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
    url(r'^pages/instructor/(?P<path>.*)$',
        user_passes_test(lambda u: auth.user_is_facilitator(u))(
            InstructorView.as_view(
                hierarchy_name="main",
                hierarchy_base="/pages/"))),
    url(r'^pages/(?P<path>.*)$', views.ParticipantSessionPageView.as_view(
        hierarchy_name="main",
        hierarchy_base="/pages/")),

    url(r'^sign-in-participant/$',
        user_passes_test(lambda u: auth.user_is_facilitator(u))(
            views.SignInParticipant.as_view()),
        name='sign-in-participant'),
    url(r'^manage-participants/$',
        user_passes_test(lambda u: auth.user_is_facilitator(u))(
            views.ManageParticipants.as_view()),
        name='manage-participants'),

    url(r'^participant/(?P<pk>\d+)/archive/$',
        user_passes_test(lambda u: auth.user_is_facilitator(u))(
            views.ParticipantArchiveView.as_view()),
        name='archive-participant'),

    url(r'^journal/(?P<session_num>\d+)/$',
        views.JournalView.as_view(), name='journal'),
    url(r'^participant-report/$',
        user_passes_test(lambda u: auth.user_is_facilitator(u))(
            views.ParticipantReportView.as_view()),
        name='participant-report'),

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
