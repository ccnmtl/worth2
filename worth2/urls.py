import os.path

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import TemplateView
from pagetree.generic.views import PageView, EditView, InstructorView
from rest_framework import routers

from worth2.main import views, apiviews


site_media_root = os.path.join(os.path.dirname(__file__), "../media")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
logout_page = (
    r'^accounts/logout/$',
    'django.contrib.auth.views.logout',
    {'next_page': redirect_after_logout})

rest_router = routers.DefaultRouter()
rest_router.register(r'participants', apiviews.ParticipantViewSet)

urlpatterns = patterns(
    '',
    auth_urls,
    logout_page,
    url(r'^api/', include(rest_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    (r'^registration/', include('registration.backends.default.urls')),
    url(r'^$', views.IndexView.as_view(), name='root'),
    (r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'smoketest/', include('smoketest.urls')),
    (r'infranil/', include('infranil.urls')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^pagetree/', include('pagetree.urls')),
    (r'^quizblock/', include('quizblock.urls')),
    (r'^pages/edit/(?P<path>.*)$', login_required(EditView.as_view(
        hierarchy_name="main",
        hierarchy_base="/pages/")),
     {}, 'edit-page'),
    (r'^pages/instructor/(?P<path>.*)$',
        login_required(InstructorView.as_view(
            hierarchy_name="main",
            hierarchy_base="/pages/"))),
    (r'^pages/(?P<path>.*)$', PageView.as_view(
        hierarchy_name="main",
        hierarchy_base="/pages/")),

    # TODO: change login_required to something that only allows
    # facilitators and superusers
    url(r'^sign-in-participant/$',
        login_required(views.SignInParticipant.as_view()),
        name='sign-in-participant'),
    url(r'^manage-participants/$', login_required(
        views.ManageParticipants.as_view()),
        name='manage-participants'),

    # url(r'^participant/create/$',
    #    login_required(views.ParticipantCreate.as_view(
    #        success_url='/manage-participants/')),
    #    name='participant-create'),
    url(r'^participant/(?P<pk>\d+)/$',
        login_required(views.ParticipantUpdate.as_view(
            success_url='/manage-participants/')),
        name='participant-update'),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
