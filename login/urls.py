from django.conf.urls import patterns, url
from login import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^group/(?P<group_id>\d+)$', views.sample_add_member, name='group'),
   	url(r'^category/(?P<category_name_slug>\w+)$', views.category, name='category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^add_page/$', views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_slug>\w+)/add_page/$', views.add_page, name='add_page'),
    url(r'^register/$', views.register, name='register'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^add_staffManager/$', views.siteManager, name='add_staff'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^groups/$', views.groups, name='groups'),
    url(r'^mygroups/$', views.mygroups, name='mygroups'),
    url(r'^manage/$', views.manage, name='manage'),
    url(r'^delete_users/$', views.deleteUser, name='delete'),
    url(r'^activate/$', views.activate, name='activate'),
    url(r'^deactivate/$', views.deactivate, name='deactivate'),
    url(r'^group/(?P<group_id>\w+)/add_member/$', views.add_user, name="adduser"),
    url(r'^group/(?P<group_id>\w+)/delete_member/$', views.delete_user, name="deleteuser"),
    url(r'^login_page/$', views.user_login, name='login_page'),  # New!
	)
