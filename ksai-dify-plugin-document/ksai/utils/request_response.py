#
# This file is part of the kernelstudio package.
#
# (c) 2014-2025 zlin <admin@kernelstudio.com>
#
# For the full copyright and license information, please view the LICENSE file
# that was distributed with this source code.

import json

import requests
from dify_plugin.file.file import File


def has_results(res) -> bool:
    if res and res.get('success') is True and res.get('result') is not None:
        return True
    return False


def handle_request(endpoint_uri, runtime, tool_parameters) -> str:
    files: list[File] = tool_parameters['files']
    if not files:
        raise ValueError('No files to process')

    submit_files = []
    for file in files:
        submit_files.append({
            'url': file.url,
            'mime': file.mime_type,
            'name': file.filename,
            'suffix': file.extension.split('.')[-1],
            'size': file.size,
        })

    api_key = runtime.credentials.get('api_key', "")
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'

    res = requests.post(
        endpoint_uri,
        headers=headers,
        data={
            "files": json.dumps(submit_files, ensure_ascii=False),
        },
    ).json()

    if has_results(res) and isinstance(res.get('result'), list):
        result = res.get('result', [])
        contents = []
        for r in result:
            if 'content' in r:
                contents.append(r['content'])
        if len(contents) > 0:
            return "\n\n\n".join(contents)
        else:
            raise ValueError("无法解析.")
    else:
        raise ValueError("解析出现错误.")
