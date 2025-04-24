from reportportal_client.helpers import timestamp
from reportportal_client.core.rp_issues import Issue
from typing import Optional, Dict, Union, Any, Tuple

from .launcher import Launcher


class Test:

    def __init__(self, launcher: Launcher):
        self.launcher = launcher
        self.id = None
        self.__test_url_parts = f"{self.launcher.project_name}/item"

    def get_id(self):
        if not self.id:
            raise RuntimeError("Test item has not been started. Cannot finish the test.")
        return self.id

    def start(
            self, 
            test_name: str,
            item_type: str = "TEST",
            attributes: Optional[Dict[str, Any]] = None, 
            description: Optional[str] = None,
            parameters: Optional[dict] = None,
            parent_item_id: Optional[str] = None,
            has_stats: bool = True,
            code_ref: Optional[str] = None,
            retry: bool = False,
            test_case_id: Optional[str] = None,
            retry_of: Optional[str] = None,
            uuid: Optional[str] = None,
            **kwargs: Any
    ) -> str:
        try:
            test_id = self.launcher.client.start_test_item(
                name=test_name,
                start_time=timestamp(),
                item_type=item_type,
                description=description,
                attributes=attributes,
                parameters=parameters,
                parent_item_id=parent_item_id,
                has_stats=has_stats,
                code_ref=code_ref,
                retry=retry,
                test_case_id=test_case_id,
                retry_of=retry_of,
                uuid=uuid,
                **kwargs  
            )
            self.id = test_id
            return test_id

        except Exception as e:
            raise RuntimeError(f"Failed to start test '{test_name}': {e}")

    def finish(
            self,
            return_code: int,
            test_id: str = None,
            status: Optional[str] = None,
            issue: Optional[Issue] = None,
            attributes: Optional[Union[list, dict]] = None,
            description: Optional[str] = None,
            retry: Optional[bool] = False,
            test_case_id: Optional[str] = None,
            retry_of: Optional[str] = None,
            **kwargs: Any
    ):
        status = status or ("PASSED" if return_code == 0 else "FAILED")
        item_id = test_id or self.id

        if not item_id:
            raise RuntimeError("Test item has not been started. Cannot finish the test.")

        try:
            self.launcher.client.finish_test_item(
                item_id=item_id,
                end_time=timestamp(),
                status=status,
                issue=issue,
                attributes=attributes,
                description=description,
                retry=retry,
                test_case_id=test_case_id,
                retry_of=retry_of,
                **kwargs  
            )

        except Exception as e:
            raise RuntimeError(f"Failed to finish test with item ID '{self.id}' in ReportPortal: {str(e)}")


    def send_log(
        self, 
        message: str, 
        level: Union[int, str] = "INFO", 
        attachment: Optional[dict] = None, 
        test_id: Optional[str] = None,
        **kwargs: Any
        ) -> Optional[Tuple[str, ...]]:

        valid_levels = ["INFO", "DEBUG", "WARN", "ERROR", "TRACE"]
        if isinstance(level, str) and level not in valid_levels:
            raise ValueError(f"Invalid log level: {level}. Must be one of {valid_levels}.")

        item_id = test_id or self.id

        if not item_id:
            raise RuntimeError("Cannot send log: No active test item. Start a test first.")

        try:
            return self.launcher.client.log(
                time=timestamp(), 
                message=message, 
                level=level, 
                attachment=attachment, 
                item_id=item_id, 
                **kwargs
            )

        except Exception as e:
            raise RuntimeError(f"Failed to send log message to ReportPortal: {str(e)}")
