# Test Executor

Test Executor is a python UI library for the execution, monitoring and control of python based tests on a device.

The device can be identified by multiple key values, like serial number and MAC address, which are configured by the user of this library.

## Framework
The UI is a Pyside2/QML based UI and has a listener api which the test framework (not part of this library) should control.

## Configuration
There is a default configuration for the layout of the test suites which can be replaced using a json string defining each layout configuration items. 
