# -*- mode: ruby -*-
# vi: set ft=ruby :

# This script is to be run by saying 'vagrant up' in this folder. This script
# should be run only when creating a local development environment.

# Pre-provisioner shell script installs Ansible into the guest and continues
# to provision rest of the system in the guest. Works also on Windows.
$script = <<SCRIPT
if [ ! -f /vagrant_bootstrap_done.info ]; then
  sudo yum update
  sudo yum -y install epel-release
  sudo yum -y upgrade ca-certificates --disablerepo=epel
  sudo yum -y install python-devel python-pip gcc libffi-devel openssl-devel
  sudo pip install pip --upgrade
  sudo pip install setuptools --upgrade
  sudo pip install markupsafe ansible paramiko
  sudo pip install urllib3
  sudo pip install pyopenssl
  sudo pip install ndg-httpsclient
  sudo pip install pyasn1
  sudo touch /vagrant_bootstrap_done.info
fi
cd /metax/ansible
ansible-playbook site.yml
SCRIPT

#exec "vagrant plugin install vagrant-vbguest;vagrant #{ARGV.join(" ")}" unless Vagrant.has_plugin? vagrant-vbguest || ARGV[0] == 'plugin'

required_plugins = %w( vagrant-vbguest )
required_plugins.each do |plugin|
   exec "vagrant plugin install #{plugin};vagrant #{ARGV.join(" ")}" unless Vagrant.has_plugin? plugin || ARGV[0] == 'plugin'
end

Vagrant.configure("2") do |config|
  config.vm.define "metax_local_dev_env" do |server|
    server.vm.box = "centos/7"
    server.vm.network :private_network, ip: "20.20.20.20"

    case RUBY_PLATFORM
    when /mswin|msys|mingw|cygwin|bccwin|wince|emc/
        # Fix Windows file rights, otherwise Ansible tries to execute files
        server.vm.synced_folder "./", "/metax", :mount_options => ["dmode=755","fmode=644"]
    else
        # Basic VM synced folder mount
        server.vm.synced_folder "", "/metax"
    end

    server.vm.provision "shell", inline: $script

    server.vm.provider "virtualbox" do |vbox|
        vbox.name = "metax_local_development"
        vbox.gui = false
        vbox.memory = 2048
        vbox.customize ["modifyvm", :id, "--nictype1", "virtio"]
    end
  end
end
