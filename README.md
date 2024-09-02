# Lexica
Lexica is a language experience app based on recall, context, and learner identity where learners study context-rich content tailored to their interests and levels. This MVP is for English speakers learning Korean and support for other languages is planned for future releases.

In this MVP, users begin by manually entering text and clicking "Start Learning." Users can then click on words to select phrases that they are interested in learning more about. The app will automatically query a dictionary for the definitions of any words in the phrase and an algorithm will recommend the most appropriate definition in the case of words with multiple meanings.

## Deploying Locally
The deploy script `deploy-dev.sh` will automatically export any environment variables in your `.env` file and create a Docker container running MongoDB if one does not exist already. This prepares the backend for running locally.

This MVP uses AWS Cognito for user authentication. However, by default login is disabled and setting up AWS Cognito is not required and any environment variables related to AWS are not required.

### Environment Variables
The following environment variables for configuring the backend can be added to your `.env` file:
| Variable Name | Description | Recommended Value |
| ------------- | ----------- | ----------------- |
| FLASK_APP | The location of the backend Flask app. | run.py
| FLASK_CONFIG | (Optional) The configuration to run the backend Flask app with. | Default
| FLASK_DEBUG | (Optional) Whether to run the Flask app in debug mode. | True
| MONGO_HOST | Where your MongoDB instance is being hosted. | localhost
| MONGO_NAME | The name of your MongoDB Docker container. | l2ai-mongo
| MONGO_PASSWORD | The password for your MongoDB database. |
| MONGO_USERNAME | The username for your MongoDB database. |
| MONGO_PORT | The port your MongoDB instance is exposed on. | 27017
| AWS_DEFAULT_REGION | (Optional) The region where your Cognito instance is deployed. |
| COGNITO_CLIENT_ID | (Optional) The ID of your Cognito user pool's app client. |
| COGNITO_CLIENT_SECRET | (Optional) The secret of your Cognito user pool's app client. |
| COGNITO_USERNAME | (Optional) The username of the user saved in your Cognito user pool. This is used when running the `flask init-user` command.  |
| COGNITO_USERPOOL_ID | (Optional) The ID of your Cognito user pool. |

The following environment variables for configuring the frontend can be added to your `.env` file in the `l2ai/frontend` directory:
| Variable Name | Description | Recommended Value |
| ------------- | ----------- | ----------------- |
| REACT_APP_API_ENDPOINT | The backend Flask app's endpoint. | http://localhost:5000

### Deploying
After creating your `.env` file with the correct environment variables, ensure Docker is running then run the deploy script in a Unix-like terminal and start the backend Flask app:

```bash
source ./deploy-dev.sh
flask run
```

In a separate terminal, insteall the frontend dependencies and start the frontend server:

```bash
cd l2ai/frontend
yarn install
yarn start
```