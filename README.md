# Report Portal Launcher

## Overview

`ReportPortalLauncher` is a Python module that provides an interface for managing test launches and test items in [Report Portal](https://reportportal.io/). It allows users to create and manage test runs, send logs, and track test execution statuses.

## Installation

Ensure you have `reportportal-client` installed:

```sh
uv sync
```

# Configuration for Report Portal client

Create a configuration file at the path `~\.report_portal\config.json` with the following parameters:

```
{
    "endpoint": "https://your-report-portal.com",
    "api_key": "your_api_key"
}
```

## Usage


### 1. Initializing ReportPortal

To start using the Report Portal client, initialize the `ReportPortal` with the required configuration:

```python
from report_portal import ReportPortal

rp = ReportPortal(project_name="your_project_name")
```

### 2. Starting a Test Launch

To create a new test launch:

```python
launch_uuid = rp.launch.start(name="launch_name")
print(f"Launch started with UUID: {launch_uuid}")
```

If you need to connect to an existing launch:

```python
rp.launch.connect(launch_uuid="existing_launch_uuid")
```

### 3. Working with Test Step

After launch start you can create a test case

```python
step = rp.get_launch_step()
```

#### Start a Test

```python
step.start(name="Sample Test")
```

#### Send Logs

```python
step.send_log("Test execution started", level="INFO")
```

#### Finish a Test

```python
step.finish(return_code=0, status="PASSED")  # Mark as PASSED
```

### 4. Finishing the Test Launch

Once all test cases are completed, finish the launch:

```python
rp.launch.finish()
```

## Example 

```python
from report_portal import ReportPortal

# Initialize the report portal
rp = ReportPortal(project_name="your_project_name")

# Start a test launch
rp.launch.start(name="9.0.0.58")

# Initialize a test step instance
step = rp.get_launch_step()
step.start(name="Sample Test")
step.send_log("Executing test case", level="INFO")
step.finish(return_code=0)

# Finish the test launch
rp.launch.finish()
```
