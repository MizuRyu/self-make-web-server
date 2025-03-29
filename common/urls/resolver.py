from typing import Callable, Optional

from common.http.request import HTTPRequest
from common.http.response import HTTPResponse
from common.views.static import static
from common.urls.urls import url_patterns

class URLResolver:
    def resolve(self, request: HTTPRequest) -> Optional[Callable[[HTTPRequest], HTTPResponse]]:
        """
        URL解決を行う。pathにマッチするURLパターンが存在する場合、対応するViewを返却する。
        存在しない場合、Noneを返す
        """
        for url_pattern in url_patterns:
            match = url_pattern.match(request.path)
            if match:
                request.params.update(match.groupdict())
                return url_pattern.view
            
        # pathがstaticの場合、静的ファイルからレスポンスを生成
        return static