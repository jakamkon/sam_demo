# Build your deployment package and put into S3
sam build
# Create a "stack" with all of the necessary resources
# Print the API endpoint we can use for testing
sam deploy --guided
