from __future__ import annotations

from ..base_error	import BaseError

from typing		import TYPE_CHECKING

if TYPE_CHECKING:
	
	from ...models	import BaseResponse


class RequestRefuseError(BaseError):
	
	"""PI 拒绝了请求 (响应的 success=False), 字段从 response 现取"""
	
	def __init__(self, response: BaseResponse) -> None:
		
		self.response: BaseResponse = response
		
		super().__init__(self.response.error or "")