#!/usr/bin/env python3
import aws_cdk

import aws_cdk_iot.stack as stack

app = aws_cdk.App()
stack.IoTStack(app, "IoTMainStack", "IoT Stack")

app.synth()
