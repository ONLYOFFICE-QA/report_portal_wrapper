from reportportal_client.helpers import timestamp
from reportportal_client import RPClient
from reportportal_client.core.rp_issues import Issue
from typing import List, Optional, Dict, Union, Any, Tuple

class ReportPortalTest:
    """
    A class to interact with individual tests in Report Portal.
    It allows starting a test, finishing a test, and sending logs for the test.
    """

    def __init__(
            self, 
            client: RPClient, 
            ):
        """
        Initializes the ReportPortalTest instance.
        
        :param client: The ReportPortal client used to interact with the API.
        """
        self.client = client
        self.item_id = None

    def get_item_id(self):
        """
        Retrieves the item ID of the current test.
        
        :return: The test item's unique identifier.
        :raises RuntimeError: If the test item has not been started.
        """
        if not self.item_id:
            raise RuntimeError("Test item has not been started. Cannot finish the test.")
        return self.item_id
    

    def start_test(
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
        """
        Starts a new test item in Report Portal.

        :param test_name: The name of the test.
        :param attributes: Optional dictionary of attributes for the test.
        :param description: Description of the test (optional).
        :param parameters: Parameters associated with the test (optional).
        :param parent_item_id: ID of the parent item (optional).
        :param has_stats: Whether to collect statistics for the test (default is True).
        :param code_ref: Optional code reference for the test.
        :param retry: Whether this is a retry of a previous test.
        :param test_case_id: Optional test case ID.
        :param retry_of: ID of the test being retried (if applicable).
        :param uuid: Optional UUID for the test.
        :param kwargs: Additional parameters for the test creation.
        :raises RuntimeError: If starting the test fails.
        """
        try:
            self.item_id = self.client.start_test_item(
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
            return self.item_id

        except Exception as e:
            raise RuntimeError(f"Failed to start test '{test_name}': {e}")

    def finish_test(
            self, 
            return_code: int, 
            status: Optional[str] = None,
            issue: Optional[Issue] = None,
            attributes: Optional[Union[list, dict]] = None,
            description: Optional[str] = None,
            retry: Optional[bool] = False,
            test_case_id: Optional[str] = None,
            retry_of: Optional[str] = None,
            **kwargs: Any
    ):
        """
        Finishes the test item in Report Portal.

        :param return_code: The return code from the test (0 for success, non-zero for failure).
        :param status: Optional status to override based on the return code ("PASSED" or "FAILED").
        :param issue: Associated issue (if any).
        :param attributes: Optional additional attributes for the test item.
        :param description: Optional description for the test item.
        :param retry: Whether this test is a retry.
        :param test_case_id: Optional test case ID.
        :param retry_of: Optional ID of the test being retried.
        :param kwargs: Additional parameters for the test item finish request.
        :raises RuntimeError: If finishing the test fails.
        """
        status = status or ("PASSED" if return_code == 0 else "FAILED")

        if not self.item_id:
            raise RuntimeError("Test item has not been started. Cannot finish the test.")

        try:
            self.client.finish_test_item(
                item_id=self.item_id,
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
            raise RuntimeError(f"Failed to finish test with item ID '{self.item_id}' in ReportPortal: {str(e)}")


    def send_log(
        self, 
        message: str, 
        level: Union[int, str] = "INFO", 
        attachment: Optional[dict] = None, 
        item_id: Optional[str] = None,
        **kwargs: Any
        ) -> Optional[Tuple[str, ...]]:
        """
        Sends a log message related to the test item in Report Portal.

        :param message: The log message.
        :param level: The log level (INFO, DEBUG, WARN, ERROR, TRACE).
        :param attachment: Optional attachment for the log.
        :param item_id: The test item ID to associate the log with (default is the current test item).
        :param kwargs: Additional parameters for the log request.
        :raises ValueError: If the log level is invalid.
        :raises RuntimeError: If sending the log fails.
        :return: Optional tuple of log entry identifiers.
        """
        valid_levels = ["INFO", "DEBUG", "WARN", "ERROR", "TRACE"]
        if isinstance(level, str) and level not in valid_levels:
            raise ValueError(f"Invalid log level: {level}. Must be one of {valid_levels}.")

        item_id = item_id or self.item_id 

        if not item_id:
            raise RuntimeError("Cannot send log: No active test item. Start a test first.")

        try:
            return self.client.log(
                time=timestamp(), 
                message=message, 
                level=level, 
                attachment=attachment, 
                item_id=item_id, 
                **kwargs  
            )
        except Exception as e:
            raise RuntimeError(f"Failed to send log message to ReportPortal: {str(e)}")
