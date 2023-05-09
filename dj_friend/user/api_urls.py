from user.views import UserApi
from django.urls import path

urlpatterns = [
    # path("admin/", admin.site.urls),
    path(
        "reg", UserApi.as_view({"post": "post_registration"}), name="registration_user"
    ),
    path(
        "add/<int:user_from_id>/<int:user_to_id>",
        UserApi.as_view({"get": "get_add_friend"}),
        name="add_friend",
    ),
    path(
        "accept/<int:user_from_id>/<int:user_to_id>",
        UserApi.as_view({"get": "get_accept_friendship"}),
        name="accept_friend",
    ),
    path(
        "reject/<int:user_from_id>/<int:user_to_id>",
        UserApi.as_view({"get": "get_reject_friendship"}),
        name="reject_friend",
    ),
    path(
        "delete/<int:user_from_id>/<int:user_to_id>",
        UserApi.as_view({"delete": "delete_friendship"}),
        name="delete_friend",
    ),
    path(
        "status/<int:user_from_id>/<int:user_to_id>",
        UserApi.as_view({"get": "get_status"}),
        name="status_friend",
    ),
    path(
        "friend_list/<int:user_from_id>",
        UserApi.as_view({"get": "get_friend_list"}),
        name="friend_list",
    ),
    path(
        "in_out_friend_request/<int:user_from_id>",
        UserApi.as_view({"get": "get_in_out_friend_request"}),
        name="request_lists_friend",
    ),
]
