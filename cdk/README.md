# SAM to CDK Migration

This is the Python CDK version of the SAM application in the parent directory, providing the same REST API functionality with Lambda backend and DynamoDB storage.

## Architecture

- **API Gateway**: REST API with `/list` (GET) and `/put` (POST) endpoints
- **Lambda Functions**: Two functions handling list and put operations
- **DynamoDB Table**: Simple table with string partition key
- **Deployment**: Conditional canary deployments for production

## Key Features Migrated

- Conditional deployment preferences (canary for prod, all-at-once for dev)
- Lambda aliases and versioning
- Environment variables
- IAM permissions (DynamoDB CRUD)
- API Gateway integration
- Stack name-based table naming

## Setup

1. Navigate to the CDK directory:
```bash
cd cdk
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Bootstrap CDK (if first time):
```bash
cdk bootstrap
```

4. Deploy:
```bash
# Development deployment
cdk deploy

# Production deployment (enables canary deployments)
cdk deploy -c stack_name=sam-app-prod
```

## Project Structure

```
cdk/
├── app.py                    # CDK app entry point
├── requirements.txt          # CDK dependencies
├── cdk.json                 # CDK configuration
├── README.md                # This file
└── sam_cdk_app/
    ├── __init__.py
    └── sam_cdk_stack.py     # Main stack definition
```

The CDK code references the Lambda source code in `../src/` (parent directory).

## Differences from SAM

- Uses CDK constructs instead of SAM transforms
- Explicit CodeDeploy configuration for gradual deployments
- More granular control over resource properties
- Python-based infrastructure as code

## Commands

Run these commands from the `cdk/` directory:

- `cdk ls` - List stacks
- `cdk synth` - Synthesize CloudFormation template
- `cdk deploy` - Deploy stack
- `cdk diff` - Compare deployed stack with current state
- `cdk destroy` - Delete stack