# Test lambda function locally
docker network create sam-demo
docker run -p 8000:8000 --network sam-demo --name dynamodb amazon/dynamodb-local
export AWS_ENDPOINT_URL=http://localhost:8000
./create-table.sh
sam local start-api --env-vars ./testenv.json --docker-network sam-demo
# Test locally
curl http://127.0.0.1:3000/list
curl -X POST http://127.0.0.1:3000/put
curl http://127.0.0.1:3000/list

# Deploy an app
sam build -u
sam deploy --guided

# Test deployment
curl https://REST-API-ID.execute-api.REGION.amazonaws.com/Prod/list                                                                                                        
curl -X POST https://REST-API-ID.execute-api.REGION.amazonaws.com/Pr
od/put