Here's an example of how to use boto3 in Python to invoke a Lambda function and wait for the response:

```python
python
import boto3
import json

session = boto3.Session()
lambda_client = session.client('lambda')

function_name = 'your-function-name'
invocation_type = 'RequestResponse'

payload = {'key1': 'value1', 'key2': 'value2'}

try:
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType=invocation_type,
        Payload=json.dumps(payload)
    )

    if 'Payload' in response:
        payload = response['Payload'].read().decode('utf-8')
        result = json.loads(payload)
        print("Lambda function response:", json.dumps(result, indent=2))
    else:
        print("No payload in the response.")

except Exception as e:
    print(f"An error occurred: {e}")
```

#### Explanation:
* boto3 Session: This creates a session which you can use to interact with AWS services. Normally, AWS credentials are picked up from the environment or from a credentials file.
* Lambda Client: We use this client to interact with AWS Lambda.
* Function Name: Replace your-function-name with the actual name of your Lambda function.
* Invocation Type: 'RequestResponse' tells Lambda to execute the function synchronously and return the response.
* Payload: This is the data you want to pass to your Lambda function. Here, it's just a dictionary converted to JSON.
* Invoke: This method sends the request to invoke the Lambda function.
* Response Handling: We check for the presence of a Payload in the response, decode it from bytes to string, then parse the JSON back into a Python dictionary for readability when printing.

Remember, you'll need to have the appropriate AWS permissions set up for your IAM user or role to invoke Lambda functions. Also, ensure your AWS credentials are correctly configured either through environment variables, AWS CLI, or boto3 configuration.
