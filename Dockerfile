FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY . /var/task
# Install dependencies
RUN pip install -r requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD ["lambdaFunc.lambda_handler"]
