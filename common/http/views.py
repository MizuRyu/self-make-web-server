import textwrap
import urllib.parse
from datetime import datetime
from pprint import pformat
from typing import Tuple, Optional

from common.http.request import HTTPRequest
from common.http.response import HTTPResponse


def now(
     request: HTTPRequest
    ) -> Tuple[bytes, Optional[str], int]:
    """
    現在時刻を表示するHTMLを生成
    """
    html = f"""\
        <html>
        <body>
            <h1>Now: {datetime.now()}</h1>
        </body>
        </html>
    """
    response_body = textwrap.dedent(html).encode()
    # Content-Typeを指定
    status_code = 200
    content_type = "text/html; charset=utf-8"
    
    return HTTPResponse(
        status_code=status_code,
        content_type=content_type,
        body=response_body
    )

def show_request(
        request: HTTPRequest
    ) -> Tuple[bytes, Optional[str], int]:
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
            <pre>{pformat(request.header)}</pre>
            <h1>Body:</h1>
            <pre>{request.body.decode("utf-8", "ignore")}</pre>
            
        </body>
        </html>
    """
    response_body = textwrap.dedent(html).encode()

    # Content-Typeを指定
    status_code = 200
    content_type = "text/html; charset=utf-8"
    return HTTPResponse(
        status_code=status_code,
        content_type=content_type,
        body=response_body
    )

def parameters(
        request: HTTPRequest
    ) -> Tuple[bytes, Optional[str], int]:
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
        status_code = 200
        response_body = textwrap.dedent(html).encode()
        content_type = "text/html; charset=utf-8"

    return HTTPResponse(
        status_code=status_code,
        content_type=content_type,
        body=response_body
    )