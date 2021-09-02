# create an s3 bucket
aws s3 mb s3://sam-deploy-serverless-app-kuba

# package cloudformation
aws cloudformation package  --s3-bucket sam-deploy-serverless-app-kuba --template-file template.yaml --output-template-file gen/template-generated.yaml

# deploy 
aws cloudformation deploy --template-file gen/template-generated.yaml --stack-name sam-deploy-serverless-app-kuba-stack --capabilities CAPABILITY_IAM

# invoke lambda
aws lambda invoke --function-name sam-deploy-serverless-app-kuba-s-helloworldpython3-GP8VMMD9BZO2 out.json

