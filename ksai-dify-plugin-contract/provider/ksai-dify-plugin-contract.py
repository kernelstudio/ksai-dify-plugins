from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from ksai.llm.ollama_client import ollama_check_model_exists
from ksai.utils.strings import has_text


class KsaiDifyPluginContractProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            ollama_host = credentials.get('ollama_host', '')
            if not has_text(ollama_host):
                raise ToolProviderCredentialValidationError('Ollama host is required')

            extractor_model = credentials.get('extractor_model', '')
            if not has_text(extractor_model):
                raise ToolProviderCredentialValidationError('Extractor model is required.')

            if not ollama_check_model_exists(ollama_host, extractor_model):
                raise ToolProviderCredentialValidationError(f'Ollama host {extractor_model} does not exist.')

        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
