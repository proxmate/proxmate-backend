from django.conf.urls import include, url
from django.conf import settings
from website import views
from api import views as ApiViews
from django.contrib import admin
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^pricing/', views.Pricing.as_view(), name='pricing'),
    url(r'^channels/', views.Channels.as_view(), name='channels'),
    url(r'^privacy/', views.Privacy.as_view(), name='privacy'),
    url(r'^terms/', views.Terms.as_view(), name='terms'),
    url(r'^about/', views.About.as_view(), name='about'),
    url(r'^landing/', views.LandingPage.as_view()),
    url(r'^landing_nu/', views.LandingPageNewUser.as_view()),
    url(r'^uninstall/(?P<key>.*)/', views.Uninstall.as_view()),
    url(r'^remove/', views.Removal.as_view()),
    url(r'^unsubscribe/(?P<key>.*)/', views.Unsubscribe.as_view()),
    url(r'^change-card/(?P<key>.*)/', views.ChangeCard.as_view()),
    url(r'^confirm/(?P<key>.*)/$', views.Confirm.as_view()),
    url(r'^api/message/list/(?P<key>.*)/$', ApiViews.MessageApi.as_view()),
    url(r'^api/unsubscribe/(?P<key>.*)/$', ApiViews.UnsubscribeApi.as_view()),
    url(r'^api/user/confirm/(?P<key>.*)/$', ApiViews.UserApi.as_view()),
    url(r'^api/user/activation/require/$', ApiViews.UserApi.as_view()),
    url(r'^api/user/', ApiViews.UserApi.as_view()),
    url(r'^api/feedback/', ApiViews.FeedbackApi.as_view()),
    url(r'^api/proxy/whitelist/', ApiViews.ProxyAPI.as_view()),
    url(r'^api/proxy/whitelist_new/', ApiViews.ProxyAPINew.as_view()),
    url(r'^api/proxy/heartbeat/', ApiViews.ProxyAPI.as_view()),
    url(r'^api/package/update/(?P<key>.*)/', ApiViews.PackageList.as_view()),
    url(r'^api/packages/install/(?P<key>.*)/', ApiViews.PackageAPI.as_view()),
    url(r'^api/package/install/(?P<package_id>.*\w)/(?P<key>.*)/', ApiViews.PackageAPI.as_view()),
    url(r'^api/server/list/(?P<key>.*)/$', ApiViews.ServerList.as_view()),
    url(r'^api/status/(?P<key>.*)/$', ApiViews.StatusApi.as_view()),
    url(r'^api/stripe/card/(?P<key>.*)/$', ApiViews.ChangeCardApi.as_view()),
    url(r'^console/', include(admin.site.urls)),
    url(r'^stripe/', ApiViews.StripeApi.as_view()),
    url(r'^paypal/cancel/$', views.PayPalCancel.as_view()),
    url(r'^paypal/return/$', views.PayPalReturn.as_view()),
    #url(r'^paypal/', ApiViews.PayPalApi.as_view()),
    url(r'^webhook/stripe/', ApiViews.StripeWebhook.as_view()),
    url(r'^webhook/paypal/', ApiViews.PayPalWebhook.as_view()),
    url(r'blog/', include('blog.urls'), name='blog'),
    url(r'^console/reports/$', login_required(views.ReportsView.as_view())),
    url(r'^console/reports/users$', login_required(views.UserReportsView.as_view())),
    url(r'^console/reports/usage', login_required(views.UsageReportsView.as_view())),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
]
