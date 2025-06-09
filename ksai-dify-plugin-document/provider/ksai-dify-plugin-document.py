#
# This file is part of the kernelstudio package.
#
# (c) 2014-2025 zlin <admin@kernelstudio.com>
#
# For the full copyright and license information, please view the LICENSE file
# that was distributed with this source code.

from typing import Any

import requests
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class KsaiDifyPluginDocumentProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            endpoint_uri = credentials.get('endpoint_uri', None)
            if not endpoint_uri:
                raise ToolProviderCredentialValidationError('endpoint_uri is required')

            api_key = credentials.get('api_key', "")
            headers = {}
            if api_key:
                headers['Authorization'] = f'Bearer {api_key}'

            res = requests.get(
                f"{endpoint_uri}/api/v1/authorization/verification",
                headers=headers
            ).json()
            if res.get('success') is False:
                raise ToolProviderCredentialValidationError("Invalid credentials")

        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
