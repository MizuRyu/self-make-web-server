# self-make-web-server

フレームワークやライブラリをなるべく使わず、Python の標準ライブラリだけで Web サーバーと Web アプリケーションを作ってみた学習用のリポジトリです。

## 現状

2025-03-31 の commit のまま、更新していません。

## できること

- ソケットで HTTP を受け、接続ごとにスレッドを立てて処理する
- `static/` の静的ファイルを、拡張子に合った Content-Type で返す
- URL のパターン（`/user/<user_id>/profile` など）で処理を振り分ける
- クエリと POST のパラメータ、クッキーを扱う
- 簡単なテンプレートで HTML を作る（`common/templates/`）

| URL | 内容 |
| --- | --- |
| `/index.html`、`/form.html` | 静的ファイル |
| `/now` | 今の時刻 |
| `/show_request` | 受け取ったリクエストの中身 |
| `/parameters` | クエリと POST のパラメータ |
| `/user/<user_id>/profile` | URL の一部を受け取る例 |
| `/set_cookie` | クッキーを設定する |
| `/login`、`/welcome` | クッキーを使った簡単なログイン |

## 動かし方

```bash
python common/start.py   # リポジトリ直下で実行する。localhost:8080 で待ち受ける
```

ブラウザで `http://localhost:8080/index.html` を開きます。

## 構成

| 場所 | 内容 |
| --- | --- |
| `common/server/` | ソケットで待ち受けるサーバーと、リクエストごとのスレッド |
| `common/http/` | リクエスト・レスポンス・クッキーと、各 URL の処理 |
| `common/urls/` | URL のパターンと振り分け |
| `common/templates/` | テンプレートと描画 |
| `singlethreadwebserver.py`、`multithreadwebserver.py`、`workerthread.py`、`tcpclient.py` | 作っていく途中の段階のサーバーとクライアント |
| `*_recv.txt`、`*_send.txt` | 試したときに送受信した HTTP の記録 |

## できないこと

- `http://localhost:8080/` のように末尾が `/` の URL では、応答を返さずに接続が切れます。ディレクトリを静的ファイルとして開こうとして失敗するためです。
- HTTPS と keep-alive には対応していません。接続はリクエストごとに閉じます。

## ライセンス

[MIT](LICENSE)
