# coding=utf-8
# -*- coding: UTF-8 -*-
#
# This file is part of the kernelstudio package.
#
# (c) 2014-2025 zlin <admin@kernelstudio.com>
#
# For the full copyright and license information, please view the LICENSE file
# that was distributed with this source code.

default_system_prompt = "你是一个专业的合同解析助手,能够准确识别合同中的关键信息并严格按照JSON格式返回."


def format_contract_extractor_prompt(user_prompt: str, text: str, system_prompt: str = None) -> str:
    if not system_prompt:
        system_prompt = default_system_prompt

    prompts = f"""<|im_start|>system
{system_prompt}<|im_end|>
<|im_start|>user
{user_prompt}
合同文本: {text}<|im_end|>
<|im_start|>assistant
"""
    return prompts
