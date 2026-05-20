# Deploying a Python App to an Azure Virtual Machine

## Steps Involved in Deployment

### 1. Create the Virtual Machine

- Create a new virtual machine on Azure.
- Choose the preferred region, image, VM size, and authentication method.
- Download the `.pem` private key.

> Keep the `.pem` key outside your project repository, for example in `~/.ssh/`.

Example:

```bash
mv ~/Downloads/my-key.pem ~/.ssh/my-key.pem
```

### 2. Change Permission on the `.pem` File

```bash
chmod 400 ~/.ssh/my-key.pem
```

### 3. SSH into the Virtual Machine

```bash
ssh -i ~/.ssh/my-key.pem azureuser@<virtual-machine-public-ip>
```

### 4. Update and Upgrade Ubuntu Packages

```bash
sudo apt update
sudo apt upgrade -y
```

### 5. Clone the Repository into the Virtual Machine

```bash
git clone <repo-url>
cd <repo-folder>
```

### 6. Install Python Virtual Environment Support

```bash
sudo apt install python3.12-venv -y
```

Or use the generic package:

```bash
sudo apt install python3-venv -y
```

### 7. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 8. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

### 9. Install Project Dependencies

```bash
pip install -r requirements.txt
```

### 10. Run the App

For Django:

```bash
python manage.py runserver 0.0.0.0:8000
```

For FastAPI:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

For Flask:

```bash
flask run --host=0.0.0.0 --port=8000
```

### 11. Open the Application in the Browser

```text
http://<virtual-machine-public-ip>:8000
```

### 12. Allow the Port in Azure

If the app runs on a port that was not opened when creating the VM, add an inbound rule in the VM’s **Network Security Group**.

For example:

```text
Port: 8000
Protocol: TCP
Source: Any or your IP address
Action: Allow
```

## Useful Commands

Check Python version:

```bash
python3 --version
```

Check if the virtual environment is active:

```bash
which python
```

Deactivate the virtual environment:

```bash
deactivate
```

Remove a broken virtual environment:

```bash
rm -rf .venv
```