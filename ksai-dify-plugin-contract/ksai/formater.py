# coding=utf-8
# -*- coding: UTF-8 -*-
#
# This file is part of the kernelstudio package.
#
# (c) 2014-2025 zlin <admin@kernelstudio.com>
#
# For the full copyright and license information, please view the LICENSE file
# that was distributed with this source code.
import re


def clean_json_response(text: str) -> str | None:
    if text:
        # 使用正则表达式匹配被```包裹的内容，可能包含可选的json标记
        pattern = r'^\s*```(?:json)?\s*([\s\S]*?)\s*```\s*$'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            return text.strip()
    return text


def json_to_markdown_table(json_data) -> str | None:
    if isinstance(json_data, list) and len(json_data) > 0:
        headers = json_data[0].keys()
        md = "| " + " | ".join(headers) + " |\n"
        md += "| " + " | ".join(["---"] * len(headers)) + " |\n"
        for row in json_data:
            md += "| " + " | ".join(str(row.get(h, "")) for h in headers) + " |\n"
        return md
    return None
