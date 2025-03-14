# AWS CDK Configuration for IoT

This project follows a standard Python setup with a virtual environment (.venv). If the virtual environment isn't created automatically, you can set it up manually.

## Set Up Virtual Environment

On MacOS and Linux, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```bash
python -m venv .venv
.venv\Scripts\Activate
```

## Install Dependencies

Once the virtual environment is activated, install dependencies:

```bash
pip install -r requirements.txt
```

## Bootstrap

```bash
cdk bootstrap
```

## Generate CloudFormation Template

```bash
cdk synth
```

## Deploy a Stack

Replace IoTMainStack with your desired stack name (shown after running cdk synth):

```bash
cdk deploy IoTMainStack
```

## Add Dependencies

To install additional CDK libraries, add them to setup.py and rerun:

```bash
pip install -r requirements.txt
```

To update or install the Node framework use

```bash
sudo apt update && sudo apt install npm

# Check your current Node version: 
node -v 
# Install n package using the following command:
sudo npm cache clean -f
sudo npm install -g n
sudo n stable

# This command will install a tool called "n" which you can use to update Node easily.
# To update Node, run the following command in your terminal:           
n latest

# This command will install the latest version of Node on your system.
# Now you can verify that your update is complete by rechecking your Node version:  
node -v
```

AWS CLI:

```bash
npm install -g aws-cdk
```

### Deploy

```bash
nano ~/.aws/credentials

# Add IAM credentials under [profile]

export AWS_PROFILE=profile
```

The account needs the following policies attached:

```
AmazonDynamoDBFullAccess
AmazonSSMFullAccess
AWSCloudFormationFullAccess
AWSLambda_FullAccess
IAMFullAccess
AmazonS3FullAccess

Elastic-Container-Registry
```

