# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    config.vm.box = "debian/jessie64"
    config.vm.hostname = "sentry.local"

    # Outside port for our sentry
    config.vm.network "forwarded_port", guest: 80, host: 8080

    config.vm.provider "virtualbox" do |vb|
        vb.memory = "1024"
        vb.name = "sentry.tinproject.es"
    end

    config.vm.provision "ansible" do |ansible|
        ansible.verbose = ""
        ansible.playbook = "playbooks/install.yml"
    end
end
