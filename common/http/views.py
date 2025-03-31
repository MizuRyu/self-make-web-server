import textwrap
import urllib.parse
from datetime import datetime
from pprint import pformat
from typing import Tuple, Optional

from common.http.cookie import Cookie
from common.http.request import HTTPRequest
from common.http.response import HTTPResponse
from common.templates.renderer import render


def now(
     request: HTTPRequest
    ) -> HTTPResponse:
    """
    現在時刻を表示するHTMLを生成
    """
    context = {"now": datetime.now()}
    html = render("now.html", context)
    response_body = textwrap.dedent(html)
    
    return HTTPResponse(
        body=response_body
    )

def show_request(
        request: HTTPRequest
    ) -> HTTPResponse:
    """
    HTTPリクエストを表示するHTMLを生成
    """
    html = f"""\
        <html>
        <body>
            <h1>Request Line:</h1>
            <p>
                {request.method} {request.path} {request.http_version}
            </p>
            <h1>Headers:</h1>
            <pre>{pformat(request.headers)}</pre>
            <h1>Body:</h1>
            <pre>{request.body.decode("utf-8", "ignore")}</pre>
            
        </body>
        </html>
    """
    response_body = textwrap.dedent(html)

    # Content-Typeを指定
    return HTTPResponse(
        body=response_body
    )

def parameters(
        request: HTTPRequest
    ) -> HTTPResponse:
    """
    POSTパラメータを表示するHTMLを生成
    """
    if request.method == "GET":
        status_code = 405
        response_body = b"<html><body><h1>405 Method Not Allowed</h1></body></html>"
        content_type = "html"
    if request.method == "POST":
        post_params = urllib.parse.parse_qs(request.body.decode())
        html = f"""\
            <html>
            <body>
                <h1>Parameters:</h1>
                <pre>{pformat(post_params)}</pre>                        
            </body>
            </html>
        """
        response_body = textwrap.dedent(html)

    return HTTPResponse(
        body=response_body
    )

def user_profile(
        request: HTTPRequest
    ) -> HTTPResponse:
    user_id = request.params.get("user_id")
    html = f"""\
        <html>
        <body>
            <h1>User Profile</h1>
            <p>User ID: {user_id}</p>
        </body>
        </html>
    """
    response_body = textwrap.dedent(html).encode()
    return HTTPResponse(
        body=response_body
    )

def set_cookie(
        request: HTTPRequest
    ) -> HTTPResponse:
    """
    Cookieを設定する
    """
    return HTTPResponse(
        headers={"Set-Cookie": "username=TARO"}
    )

def login(
        request: HTTPRequest
) -> HTTPResponse:
    """
    ログイン画面を表示する
    """
    if request.method == "GET":
        response_body = render("login.html", {})
        return HTTPResponse(
            body=response_body
        )
    if request.method == "POST":
        post_params = urllib.parse.parse_qs(request.body.decode())
        username = post_params.get("username", [""])[0]
        email = post_params.get("email", [""])[0]

        headers = {"Location": "/welcome"}
        cookies = [
            Cookie(name="username", value=username, max_age=30),
            Cookie(name="email", value=email, max_age=30)
        ]
        return HTTPResponse(
            status_code=302,
            headers=headers,
            cookies=cookies
        )
    
def welcome(
    request: HTTPRequest
) -> HTTPResponse:
    """
    ログイン後、ようこそ画面表示
    """
    # Cookieが存在しない場合、ログイン画面にリダイレクト
    if "username" not in request.cookies:
        return HTTPResponse(
            status_code=302,
            headers={"Location": "/login"}
        )
    
    username = request.cookies.get("username", "")
    email = request.cookies.get("email", "")
    body = render("welcome.html", context={"username": username, "email": email})
    return HTTPResponse(
        body=body
    )
