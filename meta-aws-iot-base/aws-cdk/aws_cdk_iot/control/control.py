import os
from aws_cdk import Stack, Duration, aws_iam as _iam, aws_dynamodb as _dynamodb, aws_lambda as _lambda, aws_iot_alpha as _iot_alpha, aws_secretsmanager as _secretsmanager, aws_iot_actions_alpha as _aws_iot_actions_alpha
from constructs import Construct
from config import *


class Control(Stack):

    def __init__(self, scope: Construct, construct_id: str) -> None:
        super().__init__(scope, construct_id)
        self.dir_name = os.path.dirname(os.path.realpath(__file__))
        self._define_statements()
        ids_table = _dynamodb.Table(self,
                                    id=DEVICES_TABLE_NAME_ID,
                                    table_name=DEVICES_TABLE_NAME,
                                    partition_key=_dynamodb.Attribute(
                                        name=DevicesTableFields.ID,
                                        type=_dynamodb.AttributeType.STRING)
                                    )
        self._create_lambda_user()
        self._define_requests_lambda()
        ids_table.grant_read_write_data(self._requests_lambda)

    def _define_statements(self):
        self._statements = dict()
        self._statements['iot_publish'] = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            actions=["iot:Publish"],
            resources=[
                Stack.of(self).format_arn(
                    service="iot",
                    resource="*",
                ),
            ]
        )
        self._statements['dynamodb_get_put'] = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            actions=[
                "dynamodb:GetItem",
                "dynamodb:PutItem"
            ],
            resources=[
                Stack.of(self).format_arn(
                    service="dynamodb",
                    resource="table",
                    resource_name=DEVICES_TABLE_NAME,
                ),
            ],
        )
        self._statements['get_secret'] = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            actions=["secretsmanager:GetSecretValue"],
            resources=["*"]
        )

    def _create_lambda_user(self):
        self.lambda_user = _iam.User(self, LAMBDA_USER)
        self.lambda_access_key = _iam.CfnAccessKey(self, LAMBDA_ACCESS_KEY,
                                                   user_name=self.lambda_user.user_name)
        self.lambda_access_key_secret = _secretsmanager.Secret(
            self,
            LAMBDA_ACCESS_KEY_SECRET)

        cfnSecret = self.lambda_access_key_secret.node.default_child
        cfnSecret.generate_secret_string = None
        cfnSecret.secret_string = self.lambda_access_key.attr_secret_access_key

    def _define_requests_lambda(self):
        self._requests_lambda = _lambda.Function(
            self, LAMBDA_REQUESTS,
            code=_lambda.Code.from_asset(os.path.join(self.dir_name, "lambda_code")),
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_code.lambda_function.lambda_handler",
            environment={PERMANENT_ACCESS_KEY_ID_ENV: self.lambda_access_key.ref,
                         PERMANENT_ACCESS_KEY_SECRET_NAME_ENV: self.lambda_access_key_secret.secret_name,
                         DEVICES_TABLE_NAME_ENV: DEVICES_TABLE_NAME},
            timeout=Duration.seconds(20))

        self._requests_lambda.add_to_role_policy(self._statements['iot_publish'])
        self._requests_lambda.add_to_role_policy(self._statements['get_secret'])
        self._requests_lambda.add_to_role_policy(self._statements['dynamodb_get_put'])

        _iot_alpha.TopicRule(self, "TopicRuleRequests",
                             sql=_iot_alpha.IotSql.from_string_as_ver20160323(
                                 f"SELECT * FROM '{REQUESTS_TOPIC}'"),
                             actions=[_aws_iot_actions_alpha.LambdaFunctionAction(self._requests_lambda)])
