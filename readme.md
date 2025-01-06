# Azure DevOps Agent Configuration with Terraform and AWS

## Prerequisites

- AWS CLI installed and configured with proper credentials
- Terraform installed (v1.0+ recommended)
- Azure DevOps agent installed (instructions below)
- Personal Access Token (PAT) for Azure DevOps authentication

## Steps


## Structure in order :
```bash
ci-cd/                                                                                       
├── terraform/                                                                               
│   └── main.tf                                                                              
├── pipelines/                                                                              
│   ├── azure_pipelines_run_on_VM_Agent.yaml                                                 
│   └── azure_pipelines_on_Azure_Agent.yaml                                                  
├── code/                                                                                    
│   ├── deploy.sh                                                                            
│   ├── log.txt                                                                              
│   ├── main.py                                                                              
│   └── test_main.py                                                                         
├── .gitignore                                                                               
└── README.md                                                                                
```
   
### 1. Configure AWS Credentials

Before starting, ensure you have valid AWS credentials configured. Use the following command to set up your credentials:

```bash
aws configure
```

Provide:
- AWS Access Key ID
- AWS Secret Access Key
- Default region name
- Default output format (e.g., `json`)

### 2. Deploy Infrastructure with Terraform

Navigate to the Terraform directory and initialize the environment:

```bash
cd terraform
terraform init
```

Then, apply the Terraform configuration to deploy the required infrastructure:

```bash
terraform apply
```

Review the proposed changes and type `yes` to confirm. Terraform will create the necessary resources, including an EC2 instance.

Once complete, Terraform will output the public IP address of the EC2 instance. Note this IP address for later steps.

### 3. Connect to the EC2 Instance via SSH

Use the public IP address of the EC2 instance to connect via SSH. Replace `<public-ip>` with the actual IP address and ensure you have the private key file (`.pem`) for authentication:

```bash
ssh -i path/to/your-key.pem ubuntu@<public-ip>
```

### 4. Configure the Azure DevOps Agent

#### a. Download the Agent

Choose the x64 version of the agent and download it:

```bash
wget https://vstsagentpackage.azureedge.net/agent/3.248.0/vsts-agent-linux-x64-3.248.0.tar.gz
tar zxvf vsts-agent-linux-x64-3.248.0.tar.gz
```

#### b. Run the Configuration Script

Navigate to the agent's directory and run the configuration script:

```bash
./config.sh
```

#### c. Provide Configuration Details

1. Accept the license agreement by typing `y`.
2. Enter the server URL for Azure DevOps:
   ```
   https://dev.azure.com/YourDomain/
   ```
3. Use `PAT` (Personal Access Token) as the authentication method and paste your PAT when prompted.
4. Choose the agent pool (default: `default`).
5. Enter the agent name or press Enter to use the default.
6. Use the default work folder (`_work`) or specify a custom one.

#### d. Install the Agent as a Service

To ensure the agent runs automatically after a restart:

```bash
sudo ./svc.sh install
```
#### e. Start the Agent

Start the agent:
```bash
sudo ./svc.sh start
```
Check the agent status:
```bash
sudo ./svc.sh status
```
You should see a status indicating the agent is running.

### 5. Configure SSH Connection in Azure DevOps

In Azure DevOps, set up the SSH connection for deployment:

1. Navigate to your project settings and select "Service Connections."
2. Add a new service connection of type "SSH."
3. Provide the following details:
   - **Host**: The public IP address of your EC2 instance
   - **Port**: `22`
   - **User Name**: `ubuntu` (or the default user for your EC2 AMI)
   - **Private Key**: Paste the contents of your private key file (e.g., `key.pem`)

Save the connection.

### 6. Add Reporting and Backup Steps

To enhance reliability and visibility, the pipeline includes steps to:

1. **Publish Reports**: Ensure test results and logs are uploaded to Azure DevOps.
2. **Perform Backup**: Configure automated backups of critical data before executing critical operations.


