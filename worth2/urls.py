import os.path

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.views.generic import TemplateView
from pagetree.generic.views import EditView, InstructorView
from rest_framework import routers

from worth2.main import apiviews, auth, views
from worth2.ssnm import views as ssnm_views
from worth2.ssnm import apiviews as ssnm_apiviews


site_media_root = os.path.join(os.path.dirname(__file__), "../media")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
logout_page = (
    r'^accounts/logout/$',
    'django.contrib.auth.views.logout',
    {'next_page': redirect_after_logout})
if hasattr(settings, 'CAS_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (
        r'^accounts/logout/$',
        'djangowind.views.logout',
        {'next_page': redirect_after_logout})

rest_router = routers.DefaultRouter()
rest_router.register(r'participants', apiviews.ParticipantViewSet)

ssnm_rest_router = routers.DefaultRouter(trailing_slash=False)
ssnm_rest_router.register(r'supporters', ssnm_apiviews.SupporterViewSet,
                          base_name='supporter')

urlpatterns = patterns(
    '',
    auth_urls,
    logout_page,
    url(r'^api/', include(rest_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    (r'^registration/', include('registration.backends.default.urls')),
    url(r'^$',
        user_passes_test(lambda u: u.is_authenticated())(
            views.IndexView.as_view()),
        name='root'),
    (r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'infranil/', include('infranil.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    (r'^pagetree/', include('pagetree.urls')),
    (r'^quizblock/', include('quizblock.urls')),
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

    url(r'^avatar-selector/$',
        user_passes_test(lambda u: auth.user_is_participant(u))(
            views.AvatarSelector.as_view()),
        name='avatar-selector'),

    # Social Support Network Map activity
    url(r'^ssnm/api/', include(ssnm_rest_router.urls)),
    url(r'^ssnm/$',
        user_passes_test(lambda u: auth.user_is_participant(u))(
            ssnm_views.SSNM.as_view()),
        name='ssnm'),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
