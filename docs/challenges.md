# Deploying a Python App to an Azure Virtual Machine

Deploying a python app to microsoft azure virtual machine for the software industrilization course

## Challenges

- Finding a region on azure
- Setting up and installing Pythin properly on the virtual machine
- Creating and activating a Python virtual environment
- Opening the correct inbound port for the running application

## Steps Involved In Deploying the app to the virtual machine

- Create the virtual machine in azure and download the `.pem` key
- Move the `.pem` key to the `~/.ssh/`
- Change the permission on the `.pem` file using the command `chmod 400 ./path/to/key.pem`
- SSH into the virtual machine using the following command `ssh -i ./path/to/key.pem {virtual-machine-username}@{virtual-machine-public-ip}`
- Run the following ubuntu commands to update and upgrade
  - `sudo apt update`
  - `sudo apt upgrade -y`
- Clone the repo into the virtual machine using `git clone /path/to/repo.git`
- Set up the requirements and install the pre-requisite to have the repo running
  - `sudo apt install python3.12-venv`
  - `python3 -m venv .venv`
  - `pip install -r requirements.txt`
- After setting it up and running the app, visit:
  - If the app is running on a different port asides from the ones created when setting up the virtual machine, add new inbound ports in the security group section under the resource tab
  - `http://${virtual-machine-public-ip}:8000`