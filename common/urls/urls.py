import common.http.views as views
from common.urls.pattern import URLPattern

URL_VIEW = {
    "/now": views.now,
    "/show_request": views.show_request,
    "/parameters": views.parameters,
    "/user/<user_id>/profile": views.user_profile,
}

url_patterns = [
    URLPattern("/now", views.now),
    URLPattern("/show_request", views.show_request),
    URLPattern("/parameters", views.parameters),
    URLPattern("/user/<user_id>/profile", views.user_profile),
    URLPattern("/set_cookie", views.set_cookie),
    URLPattern("/login", views.login),
    URLPattern("/welcome", views.welcome)
]