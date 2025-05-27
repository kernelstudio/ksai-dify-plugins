import logging
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ksai.contract.extractor import contract_content_extractor
from ksai.utils.strings import has_text

logger = logging.getLogger(__name__)


class KsaiDifyPluginContractExtractorTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        ollama_host = self.runtime.credentials.get('ollama_host')
        extractor_model = self.runtime.credentials.get('extractor_model')

        rules = tool_parameters.get('rules', '')
        if not has_text(rules):
            rules = self.runtime.credentials.get('extractor_rules', '')
        tool_parameters.update({
            'rules': rules
        })

        response = contract_content_extractor(ollama_host, extractor_model, tool_parameters)
        yield self.create_text_message(response)
