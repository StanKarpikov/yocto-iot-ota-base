import os
import json
from pathlib import Path
from aws_cdk import aws_iam as iam
from aws_cdk import aws_iot as iot
from aws_cdk import Duration, aws_lambda as _lambda
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
                                               {"$POLICY_NAME": PRODUCTION_POLICY_NAME})

        pre_provisioning_lambda = _lambda.Function(
            self, LAMBDA_REQUESTS,
            code=_lambda.Code.from_asset(os.path.join(str(package_dir), "pre_prov_lambda_code")),
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            environment={},
            timeout=Duration.seconds(20))
        pre_provisioning_lambda.grant_invoke(iam.ServicePrincipal("iot.amazonaws.com"))

        iot.CfnProvisioningTemplate(
            self,
            "template",
            pre_provisioning_hook=iot.CfnProvisioningTemplate.ProvisioningHookProperty(
                target_arn=pre_provisioning_lambda.function_arn,
            ),
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
