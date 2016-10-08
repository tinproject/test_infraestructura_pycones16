#!/usr/bin/env bash

# This activate a conda env where I have ansible and testinfra
enterconda && source activate ansible

# Destroy the vagran machine to start fresh
vagrant destroy -f
vagrant up --no-provision

# Save ssh config
vagrant ssh-config > .vagrant/ssh-config

# Run tests -> Should fail RED
testinfra --connection=ssh --host=default --ssh-config=.vagrant/ssh-config --tb=no tests/test_sentry_infra.py

# Run provision over our machine
date
time vagrant provision
date

# wait a minute for the services to start
sleep(60)

# Run test again -> Should pass GREE
testinfra --connection=ssh --host=default --ssh-config=.vagrant/ssh-config --tb=no tests/test_sentry_infra.py
