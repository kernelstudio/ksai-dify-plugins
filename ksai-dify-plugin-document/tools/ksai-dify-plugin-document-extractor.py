#
# This file is part of the kernelstudio package.
#
# (c) 2014-2025 zlin <admin@kernelstudio.com>
#
# For the full copyright and license information, please view the LICENSE file
# that was distributed with this source code.

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ksai.utils.request_response import handle_request


class KsaiDifyPluginDocumentExtractorTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        endpoint_uri = self.runtime.credentials.get('endpoint_uri', "")
        endpoint_uri = f"{endpoint_uri}/api/v1/app/document/extract/batch"
        content = handle_request(endpoint_uri, self.runtime, tool_parameters)
        yield self.create_text_message(content)
