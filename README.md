# Report Portal Launcher

## Overview

`ReportPortalLauncher` is a Python module that provides an interface for managing test launches and test items in [Report Portal](https://reportportal.io/). It allows users to create and manage test runs, send logs, and track test execution statuses.

## Installation

Ensure you have `reportportal-client` installed:

```sh
pip install reportportal-client
```

## Usage

### 1. Initializing ReportPortalLauncher

To start using the Report Portal client, initialize the `ReportPortalLauncher` with the required configuration:

```python
from report_portal_launcher import ReportPortalLauncher

# Configuration for Report Portal client
config = {
    "endpoint": "https://your-report-portal.com",
    "project": "your_project_name",
    "api_key": "your_api_key"
}

launcher = ReportPortalLauncher(config)
```

### 2. Starting a Test Launch

To create a new test launch:

```python
launch_id = launcher.start_launch(name="My Test Launch")
print(f"Launch started with ID: {launch_id}")
```

If you need to connect to an existing launch:

```python
launcher.connect_to_launch(launch_id="existing_launch_id")
```

### 3. Working with Test Cases

Create a `ReportPortalTest` instance to interact with individual test cases:

```python
from report_portal_launcher import ReportPortalTest

test = ReportPortalTest(launcher.get_client())
```

#### Start a Test

```python
test.start_test(test_name="Sample Test")
```

#### Send Logs

```python
test.send_log("Test execution started", level="INFO")
```

#### Finish a Test

```python
test.finish_test(status="PASSED")  # Mark as PASSED
```

### 4. Finishing the Test Launch

Once all test cases are completed, finish the launch:

```python
launcher.finish_launch()
```

## Error Handling

-   If `start_test` is called before `start_launch`, a `RuntimeError` will be raised.
-   Invalid log levels will trigger a `ValueError`.
-   If the client is not initialized, operations will raise `RuntimeError`.

## Example 

```python
from report_portal_launcher import ReportPortalLauncher, ReportPortalTest

# Initialize the launcher
config = {
    "endpoint": "https://your-report-portal.com/api/v1",
    "project": "your_project_name",
    "api_key": "your_api_key"
}
launcher = ReportPortalLauncher(config)

# Start a test launch
launcher.start_launch(name="My Test")

# Initialize a test instance
test = ReportPortalTest(launcher.get_client())

test.start_test(test_name="Sample Test")
test.send_log("Executing test case", level="INFO")
test.finish_test(status="PASSED")

# Finish the test launch
launcher.finish_launch()
```
