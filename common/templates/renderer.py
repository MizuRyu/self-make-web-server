import os

import settings

def render(
        template_name: str,
        context: dict
):
    # NOTE: テンプレートファイルの置き場は、設定値で変更できるようにしておく
    template_path = os.path.join(settings.TEMPLATES_DIR, template_name)
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    
    return template.format(**context)