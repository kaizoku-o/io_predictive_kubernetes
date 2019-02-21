#!/bin/bash

cat<<EOF>/etc/netplan/99-netcfg-vmware.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens160:
      dhcp4: no
      dhcp6: no
      addresses:
        [$1/24]
      gateway4: $2
      nameservers:
          addresses: [$3]
EOF

netplan --debug apply
