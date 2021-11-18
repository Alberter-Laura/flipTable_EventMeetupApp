from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('user_create', views.user_create),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    # path('gameShelf', views.gameShelf),
    path('profile/<int:user_id>', views.user_profile),
    path('update_user/<int:user_id>', views.update_user),
    path('update_user_about/<int:user_id>', views.update_user_about),
    # path('others_profile/<int:user_id>', views.others_profile),
    path('event/<int:event_id>', views.event),
    path('plan_event', views.plan_event),
    path('add_event', views.add_event),
    path('edit_event/<int:event_id>', views.edit_event),
    path('delete_event/<int:event_id>', views.delete_event),
    path('attending/<int:user_id>/<int:event_id>', views.attending),
    path('not_attending/<int:user_id>/<int:event_id>', views.not_attending),
    # path('add-game', views.add_game),
]
