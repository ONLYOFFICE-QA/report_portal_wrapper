from typing import Optional, Tuple, Union

from .launcher import Launcher
from .test_item import TestItem


class Test:

    def __init__(self, launcher: Launcher):
        self.launcher = launcher
        self.test_item = TestItem(launcher=self.launcher, item_type="TEST")

    @property
    def id(self):
        if not self.test_item.item_id:
            raise RuntimeError("Test item has not been started. Cannot finish the test.")
        return self.test_item.item_id

    def start(self, test_name: str, suite_id: str = None, **kwargs) -> str:
        return self.test_item.start(name=test_name, parent_item_id=suite_id  ,**kwargs)

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
