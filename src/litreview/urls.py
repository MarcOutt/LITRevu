from blog.views import LoginPageView, SignupPageView, TicketCreateView, PostsView, TicketUpdateView, \
    TicketDeleteView, ReviewCreateView, FollowUsersView, FluxView, TicketResponseView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', LoginPageView.as_view(), name='login'),
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('flux/', FluxView.as_view(), name='flux'),
    path('ticket/create/', TicketCreateView.as_view(), name='ticket-create'),
    path('ticket/<int:ticket_id>/response/', TicketResponseView.as_view(), name='ticket-response'),
    path('review/create/', ReviewCreateView.as_view(), name='review-create'),

    path('posts/', PostsView.as_view(), name='posts'),
    path('ticket/<int:ticket_id>/edit/', TicketUpdateView.as_view(), name='ticket-edit'),
    path('ticket/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
    path('review/<int:pk>/delete/', TicketDeleteView.as_view(), name='review-delete'),

    path('follow-users/', FollowUsersView.as_view(), name='follow-users'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)