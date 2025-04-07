from reportportal_client import RPClient
from reportportal_client.helpers import timestamp
from typing import  Dict, Any, Optional, Union
import json, os

class ReportPortalLauncher:
    """
    Class for managing launches in Report Portal.
    Allows creating a new launch, connecting to an existing launch,
    finishing it, and sending logs.
    """
    def __init__(self, project_name: str = None, config_path: str = "./config.json"):
        """
        Initializes ReportPortalLauncher with the provided configuration for RPClient.

        :param rp_client_config: Dictionary with all parameters for RPClient initialization.
        """
        self.project_name = project_name
        if not os.path.isabs(config_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, config_path)
        self.config_path = config_path
        self.rp_client_config = self._load_config()
        self.client = None
        self.launch_id = None

    def _create_client(self):
        """
        Creates an instance of RPClient with merged configuration.
        """
        config = {**self.rp_client_config, "project": self.project_name}
        return RPClient(**config)
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Loads the configuration from the JSON file.

        :return: Dictionary with configuration parameters.
        """
        try:
            with open(self.config_path, "r") as config_file:
                return json.load(config_file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load config from {self.config_path}: {e}")
    
    def get_client(self):
        """
        Retrieves the initialized ReportPortal client.

        :raises RuntimeError: If the client is not initialized.
        :return: The initialized RPClient instance.
        """
        if not self.client:
            raise RuntimeError("Client is not initialized.")
        return self.client

    def connect_to_launch(self, launch_id: str, **kwargs):
        """
        Connects to an existing launch in Report Portal.
        
        :param launch_id: Identifier of the existing launch.
        :param kwargs: Additional parameters to override the launch config.
        """
        self.launch_id = launch_id
        self.client = self._create_client(launch_uuid=self.launch_id, **kwargs)
        try:
            self.client.start_launch(name=self.launch_name, start_time=timestamp())
            launch_info = self.client.get_launch_info()
            if not launch_info:
                raise RuntimeError(f"Launch with ID {self.launch_id} does not exist.")
        except Exception as e:
            raise RuntimeError(f"Failed to connect to existing launch with ID {self.launch_id}: {e}")

    def start_launch(
        self, 
        name: str, 
        start_time: Optional[str] = None,
        description: Optional[str] = None, 
        attributes: Optional[list | dict] = None,
        rerun: bool = False,
        rerun_of: Optional[str] = None,
        **kwargs
) -> str:
        """
        Starts a new launch or connects to an existing one.
        
        :param name: Name of the launch.
        :param start_time: Start time of the launch (optional, defaults to current timestamp).
        :param description: Description of the launch (optional).
        :param attributes: Attributes for the launch (optional).
        :param rerun: Whether this is a rerun of a previous launch.
        :param rerun_of: ID of the launch being rerun.
        :param kwargs: Additional parameters for the client configuration.
        :return: Identifier of the created or connected launch.
        """
        start_time = start_time or timestamp()  
        attributes = attributes or {}

        self.client = self._create_client(**kwargs)
        
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


    def finish_launch(
        self,
        end_time: Optional[str] = None,
        status: Optional[str] = "PASSED",
        attributes: Optional[Union[list, dict]] = None,
        **kwargs: Any
    ):
        """
        Finishes the current launch.
        
        :param end_time: End time of the launch (defaults to current timestamp).
        :param status: Completion status (e.g., "PASSED" or "FAILED").
        :param attributes: Attributes for the launch (optional).
        :param kwargs: Additional parameters for the finish request.
        """
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

    from typing import Optional, Union, Any

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
        """
        Sends a log message to Report Portal.

        :param message: Log message.
        :param level: Log level (INFO, DEBUG, WARN, ERROR, TRACE).
        :param attachment: Attachment (if available).
        :param item_id: ID of the test item this log belongs to (optional).
        :param time: Log timestamp (optional, defaults to current time).
        :param print_output: Flag to print the message to the console.
        :param kwargs: Additional parameters for the log request.
        """
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

