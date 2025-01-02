
# Azure DevOps Agent Configuration on Ubuntu

Below is a detailed guide on how to configure the Azure DevOps agent on an Ubuntu machine.

## Prerequisites

- An Ubuntu machine(on Amazon Ubuntu it would not work now)
- Azure DevOps agent installed (instructions can be found in Microsoft's documentation)
- Personal Access Token (PAT) for authentication

## Configuration Steps

### 1. Download the Agent
If you haven't done so already, download the Azure DevOps agent by running the following command:
For ubuntu you need to choose x64 version of agent.
```bash
wget https://vstsagentpackage.azureedge.net/agent/3.248.0/vsts-agent-linux-x64-3.248.0.tar.gz
tar zxvf vsts-agent-linux-x64-3.248.0.tar.gz
```

### 2. Run the Agent Configuration Script
In the directory where the agent is installed, run the configuration script:

```bash
./config.sh
```

### 3. Accept the License Agreement
During the configuration, the agent will ask you to accept the license agreement. Type `y` and press Enter to continue:

```
Enter (Y/N) Accept the Team Explorer Everywhere license agreement now? (press enter for N) > y
```

### 4. Enter the Server URL
When prompted for the server URL, enter the following:

```
https://dev.azure.com/YourDomain/
```

Press Enter to continue.

### 5. Choose Authentication Method
The script will ask you which authentication method to choose. Press Enter to select the default method `PAT` (Personal Access Token):

```
Enter authentication type (press enter for PAT) > 
```

### 6. Enter the PAT Token
Next, enter your **Personal Access Token (PAT)**. You can find this token in your Azure DevOps account settings. Paste it and press Enter:

```
Enter personal access token > (paste your PAT here)
```

### 7. Choose the Agent Pool
The script will ask for the agent pool. Press Enter to select the default pool `default`:

```
Enter agent pool (press enter for default) > 
```

### 8. Enter the Agent Name
The script will ask for the agent name. You can press Enter to use the default agent name (e.g., `AgentSelfHosted`), or you can type your own custom name:

```
Enter agent name (press enter for ip-10-0-2-205) > AgentSelfHosted
```

### 9. Enter the Work Folder
The script will prompt for the work folder. Press Enter to use the default folder `_work`:

```
Enter work folder (press enter for _work) > 
```

After this, the agent will be configured and connected to Azure DevOps.

### 10. Install the Agent as a Service
To ensure the agent runs automatically after a system restart, install it as a service:

```bash
sudo ./svc.sh install
```

### 11. Start the Agent
Start the agent so it begins running:

```bash
sudo ./svc.sh start
```

After completing these steps, the Azure DevOps agent will be running on your Ubuntu machine.

### 12. Check the Agent Status
To check the agent's status, use the following command:

```bash
sudo ./svc.sh status
```

If the agent is running, you should see something like this:

```
● vsts.agent.malwinafila.Default.AgentSelfHosted.service - Azure Pipelines Agent (malwinafila.Default.AgentSelfHosted)
     Loaded: loaded (/etc/systemd/system/vsts.agent.malwinafila.Default.AgentSelfHosted.service; enabled; preset: enabled)
     Active: active (running) since Wed 2025-01-01 10:11:19 UTC; 14ms ago
```

## Notes

- If you encounter any issues during installation or configuration, check the system logs or refer to the Azure DevOps agent documentation for troubleshooting.
- To stop the agent, you can use the command:
  ```bash
  sudo ./svc.sh stop
  ```

---

This README should help you configure the Azure DevOps agent on your Ubuntu system. If you have any questions or run into problems, feel free to ask!
