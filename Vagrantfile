# vi: set ft=ruby :

#Find Vagrant root directory so you can run vagrant up anywhere
root_dir = Dir.pwd
until Dir.entries(root_dir).include? 'Vagrantfile'
  root_dir = File.expand_path('..', root_dir)
end
Dir.chdir(root_dir)


# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.


  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.provider "virtualbox" do |v, override|
      v.memory = 512
      config.vm.box = "ubuntu-precise-64"
      config.vm.box_url = "http://files.vagrantup.com/precise64.box"  
      config.vm.network :forwarded_port, guest: 8000, host: 8000
      config.vm.network :forwarded_port, guest: 8080, host: 8080
      override.vm.synced_folder ".", "/home/vagrant/Agila", :nfs => true
      override.vm.synced_folder ".", "/var/www/Agila", :nfs => true
      override.vm.network :private_network, ip: "171.71.0.71"
  end
end
