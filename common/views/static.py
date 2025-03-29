import os
import traceback

import settings
from common.http.request import HTTPRequest
from common.http.response import HTTPResponse


def static(request: HTTPRequest) -> HTTPResponse:
    """
    静的ファイルからレスポンスを取得
    """
    try:
        static_root = getattr(settings, "STATIC_ROOT")

        # pathの先頭の/を削除し、相対パスに変換
        relative_path = request.path.lstrip("/")
        static_file_path = os.path.join(static_root, relative_path)

        with open(static_file_path, "rb") as f:
            response_body = f.read()

        content_type = None
        return HTTPResponse(
            status_code=200,
            content_type=content_type,
            body=response_body,
        )
    except FileNotFoundError:
        traceback.print_exc()

        response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
        content_type = "text/html;"
        return HTTPResponse(
            status_code=404,
            content_type=content_type,
            body=response_body,
        )