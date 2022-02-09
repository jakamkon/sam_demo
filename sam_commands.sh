# Test lambda function locally
docker network create sam-demo
docker run -p 8000:8000 --network sam-demo --name dynamodb amazon/dynamodb-local
./create-table.sh
sam local start-api --env-vars ./testenv.json --docker-network sam-demo
# Test locally
curl http://127.0.0.1:3000/list
curl -X POST http://127.0.0.1:3000/put
curl http://127.0.0.1:3000/list

# Deploy an app
sam build
sam deploy --guided
