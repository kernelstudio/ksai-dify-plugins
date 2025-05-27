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

from ksai.contract.prompts import format_contract_extractor_prompt
from ksai.formater import clean_json_response
from ksai.llm.ollama_client import ollama_execute
from ksai.utils.strings import has_text


def parse_user_prompt(options: dict[str, t.Any]) -> str:
    user_prompt = options.get('user_prompt', None)
    if not has_text(user_prompt):
        user_prompt = '提取以下合同中的关键信息.'

    if user_prompt and '{rules}' in user_prompt:
        rules = options.get('rules', None)
        if not has_text(rules):
            rules = ''
        user_prompt = user_prompt.replace('{rules}', rules)
    return user_prompt


def parse_system_prompt(options: dict[str, t.Any]) -> str | None:
    system_prompt = options.get('system_prompt', None)
    if not has_text(system_prompt):
        system_prompt = None
    return system_prompt


def contract_content_extractor(host: str, model: str, options: dict[str, t.Any]) -> str | None:
    system_prompt = parse_system_prompt(options)
    user_prompt = parse_user_prompt(options)

    text = options.get('text', '')
    if text:
        try:
            text_json = json.loads(clean_json_response(text))
            if text_json and text_json.get('text', None):
                text = text_json['text']
            elif text_json and text_json.get('output', None):
                text = text_json['output']
        except Exception:
            pass

    prompt = format_contract_extractor_prompt(
        user_prompt,
        text,
        system_prompt,
    )
    options.update({
        'prompt': prompt
    })

    result = ollama_execute(host, model, options)
    if result and "</think>" in result:
        result = result.split("</think>")[1]
    result = clean_json_response(result)
    if result:
        try:
            d = json.loads(result)
            if d is not None:
                datas = {}
                for k, v in d.items():
                    if v and k not in datas:
                        datas[k] = v
                return json.dumps(datas, ensure_ascii=False)
        except Exception as e:
            print(e)
            pass
    return result
