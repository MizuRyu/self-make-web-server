from typing import Optional, List

from common.http.cookie import Cookie

class HTTPResponse:
    status_code: int
    headers: dict
    cookies: List[Cookie]
    content_type: Optional[str]
    body: bytes

    def __init__(
            self,
            status_code: int = 200,
            headers: dict = None,
            cookies: List[Cookie] = None,
            content_type: Optional[str] = None,
            body: bytes = b""
    ):
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = []
            
        self.status_code = status_code
        self.headers = headers
        self.cookies = cookies
        self.content_type = content_type
        self.body = body