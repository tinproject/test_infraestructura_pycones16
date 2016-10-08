#!/usr/bin/env bash

# This script is used to run vagrant provision from pycharm

set -e

# Activate ansible virtual environment
source ~/.bashrc
enterconda
source activate ansible

# Send cows to the farm..
export ANSIBLE_NOCOWS=1

# Launch provisioning with Vagrant -> Ansible
vagrant provision
