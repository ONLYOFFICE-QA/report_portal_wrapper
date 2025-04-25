from typing import Optional, Tuple, Union

from .launcher import Launcher
from .test_item import TestItem


class Test:

    def __init__(self, launcher: Launcher, name: str):
        self.name = name
        self.launcher = launcher
        self.test_item = TestItem(launcher=self.launcher, item_type="TEST")

    @property
    def uuid(self):
        if not self.test_item.item_uuid:
            raise RuntimeError("Test item has not been started. Cannot finish the test.")
        return self.test_item.item_uuid

    def get_info(self, uuid: str = None):
        return self.test_item.get_info(uuid=uuid)

    def start(self, suite_uuid: str = None, **kwargs) -> str:
        return self.test_item.start(name=self.name, parent_item_id=suite_uuid  ,**kwargs)

    def finish(self, return_code: int, item_id: str = None, **kwargs):
        self.test_item.finish(return_code=return_code, item_id=item_id, **kwargs)

    def send_log(self,
                message: str,
                item_id: Optional[str] = None,
                level: Union[int, str] = "INFO",
                attachment: Optional[dict] = None,
                 **kwargs
        ) -> Optional[Tuple[str, ...]]:
        self.test_item.send_log(
            message=message,
            item_id=item_id,
            level=level,
            attachment=attachment,
            **kwargs
        )
