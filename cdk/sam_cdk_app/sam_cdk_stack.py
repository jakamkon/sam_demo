from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_codedeploy as codedeploy,
    CfnOutput,
    Duration,
    RemovalPolicy
)
from constructs import Construct

class SamCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, stack_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Determine if this is production based on stack name
        is_production = stack_name == "sam-app-prod"
        
        # Create DynamoDB table
        table = dynamodb.Table(
            self, "Table",
            table_name=f"SAMTest-{stack_name}",
            partition_key=dynamodb.Attribute(
                name="mykey",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PROVISIONED,
            read_capacity=2,
            write_capacity=2,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # Create Lambda functions with shared configuration
        lambda_props = {
            "runtime": _lambda.Runtime.PYTHON_3_9,
            "code": _lambda.Code.from_asset("../src"),  # Reference src folder from parent directory
            "timeout": Duration.seconds(60),
            "memory_size": 128,
            "environment": {
                "TABLE_NAME": table.table_name,
                "ENDPOINT": "default"
            }
        }
        
        # List Lambda function
        list_lambda = _lambda.Function(
            self, "ListLambda",
            handler="lambda_function.list_handler",
            description="List all items in table.",
            **lambda_props
        )
        
        # Put Lambda function  
        put_lambda = _lambda.Function(
            self, "PutLambda",
            handler="lambda_function.put_handler", 
            description="Put a random item into a table.",
            **lambda_props
        )
        
        # Grant DynamoDB permissions to Lambda functions
        table.grant_read_write_data(list_lambda)
        table.grant_read_write_data(put_lambda)
        
        # Create Lambda aliases for deployment
        list_alias = _lambda.Alias(
            self, "ListLambdaAlias",
            alias_name="live",
            version=list_lambda.current_version
        )
        
        put_alias = _lambda.Alias(
            self, "PutLambdaAlias", 
            alias_name="live",
            version=put_lambda.current_version
        )
        
        # Create CodeDeploy applications and deployment groups for gradual deployments
        if is_production:
            # Production uses canary deployment
            list_app = codedeploy.LambdaApplication(self, "ListLambdaApp")
            codedeploy.LambdaDeploymentGroup(
                self, "ListLambdaDeploymentGroup",
                application=list_app,
                alias=list_alias,
                deployment_config=codedeploy.LambdaDeploymentConfig.CANARY_10_PERCENT_5_MINUTES
            )
            
            put_app = codedeploy.LambdaApplication(self, "PutLambdaApp") 
            codedeploy.LambdaDeploymentGroup(
                self, "PutLambdaDeploymentGroup",
                application=put_app,
                alias=put_alias,
                deployment_config=codedeploy.LambdaDeploymentConfig.CANARY_10_PERCENT_5_MINUTES
            )
        
        # Create API Gateway
        api = apigateway.RestApi(
            self, "ApiGatewayApi",
            rest_api_name="SAM CDK API",
            description="REST API with Lambda backend converted from SAM"
        )
        
        # Create API Gateway integrations
        list_integration = apigateway.LambdaIntegration(
            list_alias if is_production else list_lambda
        )
        put_integration = apigateway.LambdaIntegration(
            put_alias if is_production else put_lambda  
        )
        
        # Add API routes
        api.root.add_resource("list").add_method("GET", list_integration)
        api.root.add_resource("put").add_method("POST", put_integration)
        
        # Output the API URL
        CfnOutput(
            self, "APIGatewayDeploymentURL",
            value=f"https://{api.rest_api_id}.execute-api.{self.region}.amazonaws.com/prod/",
            description="API Gateway deployment URL"
        )