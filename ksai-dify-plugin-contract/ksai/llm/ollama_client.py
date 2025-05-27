# coding=utf-8
# -*- coding: UTF-8 -*-
#
# This file is part of the kernelstudio package.
#
# (c) 2014-2025 zlin <admin@kernelstudio.com>
#
# For the full copyright and license information, please view the LICENSE file
# that was distributed with this source code.

import json
import typing as t

import requests


def ollama_check_model_exists(ollama_host="http://localhost:11434", model_name=None):
    """
    检查指定的模型是否存在于Ollama的本地模型列表中。

    参数:
        model_name (str): 需要检查的模型名称（可包含标签，如"llama2:latest"）。
        ollama_host (str): Ollama服务的主机地址，默认为http://localhost:11434。

    返回:
        bool: 如果模型存在返回True，否则返回False。
    """
    try:
        # 发送GET请求到Ollama的API端点
        response = requests.get(f"{ollama_host}/api/tags")
        response.raise_for_status()  # 如果请求失败则抛出HTTPError异常

        # 解析JSON响应并提取模型名称列表
        models = response.json().get("models", [])
        existing_models = [model["name"] for model in models]

        # 检查目标模型是否存在
        return model_name in existing_models
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False
    except ValueError as e:
        print(f"Parse response error: {e}")
        return False


def ollama_execute(host: str, model: str, options: dict[str, t.Any]) -> str | None:
    url = f"{host}/api/generate"
    headers = {
        "Content-Type": "application/json"
    }

    final_options = {}
    for k in ['seed', 'num_predict', 'top_k', 'num_ctx', 'repeat_last_n']:
        if k in options and options.get(k) is not None:
            final_options[k] = int(options[k])

    for k in ['top_p', 'temperature', 'repeat_penalty']:
        if k in options and options.get(k) is not None:
            final_options[k] = float(options[k])

    stream = True
    if 'stream' in options and options.get('stream') is not None:
        stream = bool(options['stream'])

    prompt = ''
    if 'prompt' in options and options.get('prompt') is not None:
        prompt = str(options['prompt'])

    connection_timeout = 120
    read_timeout = 120
    if 'read_timeout' in options and options.get('read_timeout', None) is not None:
        read_timeout = int(options['read_timeout'])
    if 'connection_timeout' in options and options.get('connection_timeout', None) is not None:
        connection_timeout = int(options['connection_timeout'])

    data = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
        "options": final_options
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
            timeout=(connection_timeout, read_timeout),
            stream=stream
        )
        chunks = []
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode("utf-8"))
                chunks.append(chunk["response"])
                if stream:
                    print(chunk["response"], end="", flush=True)
        return "".join(chunks)
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
