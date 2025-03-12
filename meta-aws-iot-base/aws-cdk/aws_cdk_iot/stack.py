from aws_cdk import core as cdk

from control import control
from provisioning import provisioning


class IoTStack(cdk.Stack):
    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 description: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, description=description, **kwargs)

        control.Control(self, "control")
        provisioning.Provisioning(self, "provisioning")
