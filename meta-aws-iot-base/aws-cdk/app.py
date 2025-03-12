#!/usr/bin/env python3
from aws_cdk import core as cdk

import aws_cdk_iot.aws_cdk_iot_stack as stack

app = cdk.App()
stack.IoTStack(app, "IoTStack", "IoT Stack")

app.synth()
