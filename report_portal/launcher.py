# -*- coding: utf-8 -*-
from .client import Client
from reportportal_client.helpers import timestamp
from typing import  Any, Optional, Union


class Launcher:

    def __init__(self, project_name: str, config_path: str = None):
        self.project_name = project_name
        self.config_path = config_path
        self._client = None
        self.id = None

    @property
    def client(self):
        if not self._client:
            raise RuntimeError("Client is not initialized.")

        return self._client

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

        self._client = Client(config_path=self.config_path).create(project_name=self.project_name)

        try:
            self.id = self._client.start_launch(
                name=name,
                start_time=start_time,
                description=description,
                attributes=attributes,
                rerun=rerun,
                rerun_of=rerun_of,
                **kwargs
            )
            return self.id

        except Exception as e:
            raise RuntimeError(f"Failed to start launch '{name}': {e}")


    def finish(
        self,
        end_time: Optional[str] = None,
        status: Optional[str] = "PASSED",
        attributes: Optional[Union[list, dict]] = None,
        **kwargs: Any
    ):
        if not self.id:
            raise RuntimeError("No active launch to finish.")

        end_time = end_time or timestamp() 
        attributes = attributes or {}

        try:
            self._client.finish_launch(
                end_time=end_time,
                status=status,
                attributes=attributes,
                **kwargs  
            )
            self._client.terminate()
            self.id = None
        except Exception as e:
            raise RuntimeError(f"Failed to finish launch '{self.id}': {e}")

        self._client.terminate()

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

        if not self.id:
            raise RuntimeError("Cannot send log: No active launch. Please start a launch or connect to an existing one.")

        time = time or timestamp()  

        try:
            self._client.log(
                time=time,
                message=message,
                level=level,
                attachment=attachment,
                item_id=item_id,
                **kwargs  
            )
        except Exception as e:
            raise RuntimeError(f"Failed to send log to ReportPortal: {e}")

