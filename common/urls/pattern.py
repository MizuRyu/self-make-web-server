import re
from re import Match
from typing import Callable, Optional

from common.http.request import HTTPRequest
from common.http.response import HTTPResponse

class URLPattern:
    pattern: str
    view: Callable[[HTTPRequest], HTTPResponse]

    def __init__(
            self,
            pattern: str,
            view: Callable[[HTTPRequest], HTTPResponse]
    ):
        self.pattern = pattern
        self.view = view
    

    def match(self, path: str) -> Optional[Match]:
        """
        pathがURLパターンにマッチするかを判定
        マッチした場合、Matchオブジェクトを返却し、マッチしない場合、Noneを返却
        """
        # '/user/<user_id>/profile' -> '/user/(?P<user_id>[^/]+)/profile'
        re_pattern = re.sub(r"<(.+?)>", r"(?P<\1>[^/]+)", self.pattern)
        return re.match(re_pattern, path)