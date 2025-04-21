from reportportal_client import RPClient
from reportportal_client.helpers import timestamp
from typing import  Any, Optional, Union


class Launch:

    def __init__(self, client: RPClient):
        self.client = client
        self.launch_id = None

    def start(
        self, 
        name: str, 
        start_time: Optional[str] = None,
        description: Optional[str] = None, 
        attributes: Optional[list | dict] = None,
        rerun: bool = False,
        rerun_of: Optional[str] = None,
        **kwargs
    ) -> str:
        start_time = start_time or timestamp()  
        attributes = attributes or {}
        try:
            self.launch_id = self.client.start_launch(
                name=name,
                start_time=start_time,
                description=description,
                attributes=attributes,
                rerun=rerun,
                rerun_of=rerun_of,
                **kwargs
            )
            return self.launch_id

        except Exception as e:
            raise RuntimeError(f"Failed to start launch '{name}': {e}")


    def finish(
        self,
        end_time: Optional[str] = None,
        status: Optional[str] = "PASSED",
        attributes: Optional[Union[list, dict]] = None,
        **kwargs: Any
    ):
        if not self.launch_id:
            raise RuntimeError("No active launch to finish.")

        end_time = end_time or timestamp() 
        attributes = attributes or {}

        try:
            self.client.finish_launch(
                end_time=end_time,
                status=status,
                attributes=attributes,
                **kwargs  
            )
            self.client.terminate()
            self.launch_id = None
        except Exception as e:
            raise RuntimeError(f"Failed to finish launch '{self.launch_id}': {e}")

        self.client.terminate()

    def send_log(
            self, 
            message: str, 
            level: Optional[Union[int, str]] = "INFO", 
            attachment: Optional[dict] = None, 
            item_id: Optional[str] = None,
            time: Optional[str] = None,
            print_output: bool = True,
            **kwargs: Any
        ):
        valid_levels = ["INFO", "DEBUG", "WARN", "ERROR", "TRACE"]
        if isinstance(level, str) and level not in valid_levels:
            raise ValueError(f"Invalid log level: {level}. Must be one of {valid_levels}.")

        if print_output:
            print(f"[{level}] {message}")

        if not self.launch_id:
            raise RuntimeError("Cannot send log: No active launch. Please start a launch or connect to an existing one.")

        time = time or timestamp()  

        try:
            self.client.log(
                time=time,
                message=message,
                level=level,
                attachment=attachment,
                item_id=item_id,
                **kwargs  
            )
        except Exception as e:
            raise RuntimeError(f"Failed to send log to ReportPortal: {e}")

