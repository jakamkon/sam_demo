#!/usr/bin/env python3
import aws_cdk as cdk
from sam_cdk_app.sam_cdk_stack import SamCdkStack

app = cdk.App()

# Get stack name from context or use default
stack_name = app.node.try_get_context("stack_name") or "sam-cdk-app"

SamCdkStack(app, "SamCdkStack", 
    stack_name=stack_name,
    env=cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region")
    )
)

app.synth()