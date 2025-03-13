import os
import json
from pathlib import Path
from aws_cdk import aws_iam as iam
from aws_cdk import aws_iot as iot
from constructs import Construct

from config import *


class Provisioning(Construct):

    def __init__(self, scope: Construct, construct_id: str):
        super().__init__(scope, construct_id)
        package_dir = Path(os.path.dirname(__file__))

        production_policy = iot.CfnPolicy(
            self,
            "production_policy",
            policy_document=self._get_document(package_dir / "production_policy.json", {}),
            policy_name=PRODUCTION_POLICY_NAME)

        claim_policy = iot.CfnPolicy(
            self,
            "claim_policy",
            policy_document=self._get_document(package_dir / "claim_policy.json", {"$TEMPLATE_NAME": PROVISIONING_TEMPLATE_NAME}),
            policy_name=CLAIM_POLICY_NAME)

        registration_policy = (
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSIoTThingsRegistration"))

        template_role = iam.Role(
            self,
            "role",
            assumed_by=iam.ServicePrincipal("iot.amazonaws.com"),
            description="Role assumed by provisioning template",
            managed_policies=[registration_policy])

        template_document = self._get_document(package_dir / "provisioning_template.json",
                                               {"$POLICY_NAME": CLAIM_POLICY_NAME})
        iot.CfnProvisioningTemplate(
            self,
            "template",
            provisioning_role_arn=template_role.role_arn,
            description="A template provide production certificates to devices",
            template_body=json.dumps(template_document),
            enabled=True,
            template_name=PROVISIONING_TEMPLATE_NAME)

    @staticmethod
    def _substitute_parameters(document_text: str, parameters: dict):
        for parameter in parameters:
            document_text = document_text.replace(parameter, parameters[parameter])
        return document_text

    def _get_document(self, document_name: str | Path, parameters: dict):
        with open(document_name, "r") as file:
            json_document = json.loads(self._substitute_parameters(file.read(), parameters))
            return json_document
