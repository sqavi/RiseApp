from aws_cdk import core
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_iam as iam
import os

class MyStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        table = dynamodb.Table(
            self, "MyDynamoDBTable",
            partition_key=dynamodb.Attribute(name="user_mobile", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # Lambda Functions
        lambda_functions = {}
        #function_directories = ["reg_lambda", "auth_lambda", "verify_lambda", "askgpt_lambda"]
        function_directories = ["reg_lambda", "auth_lambda", "verify_lambda"]
        
        for func_dir in function_directories:
            function_name = os.path.basename(func_dir)
            lambda_fn = _lambda.Function(
                self, f"{function_name}Function",
                runtime=_lambda.Runtime.PYTHON_3_9,
                handler="lambda_function.lambda_handler",  # Path to the lambda function handler
                code=_lambda.Code.from_asset(func_dir),
                environment={
                    "DYNAMODB_TABLE": table.table_name
                }
            )
            lambda_functions[function_name] = lambda_fn

            # Grant Lambda read/write access to the DynamoDB table
            table.grant_read_write_data(lambda_fn)

        # API Gateway Endpoints
        api = apigw.RestApi(self, "MyAPIGateway", deploy=False)

        # Add resources and methods for each Lambda function
        for function_name, lambda_fn in lambda_functions.items():
            resource = api.root.add_resource(function_name)
            resource.add_method("POST", apigw.LambdaIntegration(lambda_fn))

        # Deploy the API Gateway
        deployment = apigw.Deployment(self, "Deployment", api=api)
        stage = apigw.Stage(self, "Stage", deployment=deployment, stage_name="prod")
        api.deployment_stage = stage

        # Output the API endpoint URLs for each function
        for function_name, lambda_fn in lambda_functions.items():
            core.CfnOutput(
                self, f"{function_name}APIEndpoint",
                value=f"{stage.url}/{function_name}"
            )

app = core.App()
MyStack(app, "MyStack")
app.synth()
