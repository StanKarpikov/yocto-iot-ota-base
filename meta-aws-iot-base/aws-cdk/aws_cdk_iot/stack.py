import aws_cdk
from control import control
from constructs import Construct
from provisioning import provisioning


class IoTStack(aws_cdk.Stack):
    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 description: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, description=description, **kwargs)

        control.Control(self, "control")
        provisioning.Provisioning(self, "provisioning")
