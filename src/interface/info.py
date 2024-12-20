from typing import TYPE_CHECKING
from typing import Union

from ..interface.template import API
from ..testers import Params

if TYPE_CHECKING:
    from ..config import Parameter


class Info(API):
    def __init__(
            self,
            params: Union["Parameter", Params],
            cookie: str | dict = None,
            proxy: str = None,
            sec_user_id: Union[str, list[str], tuple[str]] = ...,
            *args,
            **kwargs,
    ):
        super().__init__(params, cookie, proxy, *args, **kwargs, )
        self.api = f"{self.domain}aweme/v1/web/im/user/info/"
        self.sec_user_id = sec_user_id
        self.static_params = self.params | {
            "version_code": "170400",
            "version_name": "17.4.0",
        }
        self.text = "账号简略"

    async def run(self, first=True, *args, **kwargs, ) -> dict | list[dict]:
        self.set_referer()
        await self.run_single()
        if first:
            return self.response[0] if self.response else {}
        return self.response

    async def run_single(self, *args, **kwargs, ):
        await super().run_single(
            "",
            params=lambda: self.static_params,
            data=self.__generate_data,
            method="POST",
        )

    def check_response(self, data_dict: dict, *args, **kwargs, ):
        if d := data_dict.get("data"):
            self.append_response(d)
        else:
            self.log.warning(f"获取{self.text}失败")

    def __generate_data(self, ) -> dict:
        if isinstance(self.sec_user_id, str):
            self.sec_user_id = [self.sec_user_id]
        value = f"[{",".join(f'"{i}"' for i in self.sec_user_id)}]"
        return {"sec_user_ids": value, }
