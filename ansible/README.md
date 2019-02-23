# Ansible scripts to manage servers/VMs

Currently, we have one script per server that handles users, ssh keys, sudoers.

# Reminders
Make sure that the security setting allows all traffic between each host.
Make sure that ansible is installed on the default image of the hosts
Make sure you run the ansible scripts in the ansible directory
Make sure you set the IP address correctly in the inventory when make a new image
Fix the issue of rebooting the node or master and it not autostart the node

