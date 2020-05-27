# Test Executor

Test Executor is a python UI library for the execution, monitoring and control of python based tests on a device.

The device can be identified by multiple key values, like serial number and MAC address, which are configured by the user of this library.

## Framework
The UI is a Pyside2/QML based UI and has a listener api via which the test framework (not part of this library) should control it.

## Configuration
There is a default configuration for the layout of the test suites which can be replaced using a json string with all layout configuration items. 

## Example
The TestExecutorSample.py provides a demonstration of tetost execution and user configuration.