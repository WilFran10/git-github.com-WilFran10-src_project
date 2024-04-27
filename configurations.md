# NETWORK CONFIGURATIONS 

## PCS CONFIGURATIONS

PC1\
ip 10.2.2.100/24 10.2.2.10\
save 

PC2\
ip 200.2.2.100/24 200.2.2.10\
save

PC3 or LB\
ip 192.1.1.100/24 192.1.1.1\
save

## ROUTERS CONFIGURATIONS

Router - Internal Network \
configure \
int f0/1 \
no shut \
ip add 10.2.2.10 255.255.255.0\
do wr \
int f0/0\
no shut\
ip add 10.1.1.10 255.255.255.0\
do wr \
ip route 0.0.0.0 0.0.0.0 10.1.1.1\
ip route 0.0.0.0 0.0.0.0 10.1.1.2

Router - Outside\
configure\
int f0/0\
ip add 200.1.1.10 255.255.255.0\
no shut\
do wr\
int f0/1\
ip add 200.2.2.10 255.255.255.0\
no shut \
do wr\
ip route 192.2.0.0 255.255.255.0 200.1.1.1\
ip route 192.2.0.0 255.255.255.0 200.1.1.2\
ip route 192.1.1.0 255.255.255.0 200.1.1.1\
ip route 192.1.1.0 255.255.255.0 200.1.1.2

Router - DMZ\
configure\
int f0/0\
ip add 192.1.1.1 255.255.255.0\
no shut\
do wr\
int f0/1\
ip add 10.7.0.10 255.255.255.0\
no shut\
do wr\
ip route 10.2.2.0 255.255.255.0 10.7.0.1\
ip route 10.2.2.0 255.255.255.0 10.7.0.2\
ip route 0.0.0.0 0.0.0.0 10.7.0.1\
ip route 0.0.0.0 0.0.0.0 10.7.0.2

## FIREWALLS CONFIGURATIONS

**FW1** \
configure\
set system host-name FW1\
set interface ethernet eth0 address 10.3.0.10/24\
set interface ethernet eth1 address 10.0.2.12/24\
set interface ethernet eth2 address 10.0.3.20/24\
set interface ethernet eth3 address 10.2.0.11/24\
set interface ethernet eth5 address 10.7.0.1/24\
set protocols static route 0.0.0.0/0 next-hop 10.2.0.12\
set protocols static route 0.0.0.0/0 next-hop 10.0.3.21\
set protocols static route 10.2.2.0/24 next-hop 10.3.0.1\
set protocols static route 10.2.2.0/24 next-hop 10.0.2.11\
set protocols static route 192.1.1.0/24 next-hop 10.7.0.10\
commit

set nat source rule 1 outbound-interface eth2\
set nat source rule 1 source address 10.0.0.0/8\
set nat source rule 1 translation address 192.2.0.1-192.2.0.10\
commit

set nat source rule 2 outbound-interface eth3\
set nat source rule 2 source address 10.0.0.0/8\
set nat source rule 2 translation address 192.2.0.11-192.2.0.20\
commit\
save

**FW2**\
configure\
set system host-name FW2\
set interface ethernet eth0 address 10.0.4.2/24\
set interface ethernet eth1 address 10.1.0.110/24\
set interface ethernet eth2 address 10.4.0.10/24\
set interface ethernet eth3 address 10.0.5.11/24\
set interface ethernet eth5 address 10.7.0.1/24\
set protocols static route 0.0.0.0/0 next-hop 10.0.5.12\
set protocols static route 0.0.0.0/0 next-hop 10.4.0.11\
set protocols static route 10.2.2.0/24 next-hop 10.0.4.1\
set protocols static route 10.2.2.0/24 next-hop 10.1.0.100\
set protocols static route 192.1.1.0/24 next-hop 10.7.0.10\
commit

set nat source rule 1 outbound-interface eth2\
set nat source rule 1 source address 10.0.0.0/8\
set nat source rule 1 translation address 192.2.0.21-192.2.0.30\
commit

set nat source rule 2 outbound-interface eth3\
set nat source rule 2 source address 10.0.0.0/8\
set nat source rule 2 translation address 192.2.0.31-192.2.0.40\
commit\
save

## LBS CONFIGURATIONS

**LB1A**\
set system host-name LB1A\
set interfaces ethernet eth0 address 10.1.1.1/24\
set interfaces ethernet eth3 address 10.0.1.1/24\
set interfaces ethernet eth2 address 10.0.4.1/24\
set interfaces ethernet eth1 address 10.3.0.1/24\
set protocols static route 10.2.2.0/24 next-hop 10.1.1.10

**LB1B**\
set system host-name LB1B\
set interfaces ethernet eth0 address 10.1.1.2/24\
set interfaces ethernet eth3 address 10.0.1.2/24\
set interfaces ethernet eth1 address 10.0.2.11/24\
set interfaces ethernet eth2 address 10.1.0.100/24\
set protocols static route 10.2.2.0/24 next-hop 10.1.1.10

**LB2A**\
set system host-name LB2A\
set interfaces ethernet eth0 address 200.1.1.1/24\
set interfaces ethernet eth1 address 10.2.0.12/24\
set interfaces ethernet eth2 address 10.0.5.12/24\
set interfaces ethernet eth3 address 10.0.6.1/24\
set protocols static route 200.2.2.0/24 next-hop 200.1.1.10

**LB2B**\
set system host-name LB2B\
set interfaces ethernet eth0 address 200.1.1.2/24\
set interfaces ethernet eth1 address 10.0.3.21/24\
set interfaces ethernet eth2 address 10.4.0.11/24\
set interfaces ethernet eth3 address 10.0.6.2/24\
set protocols static route 200.2.2.0/24 next-hop 200.1.1.10

### HIGH-AVAILABILITY AND SYNCHRONIZATION ON LOAD BALANCES DEVICES

**LB1A**\
set high-availability vrrp group FWCluster vrid 1\
set high-availability vrrp group FWCluster interface eth3\
set high-availability vrrp group FWCluster virtual-address 192.168.100.1/24\
set high-availability vrrp sync-group FWCluster member FWCluster\
set high-availability vrrp group FWCluster rfc3768-compatibility

conntrack-sync\
set service conntrack-sync accept-protocol 'tcp,udp,icmp'\
set service conntrack-sync failover-mechanism vrrp sync-group FWCluster\
set service conntrack-sync interface eth3\
set service conntrack-sync mcast-group 225.0.0.50\
set service conntrack-sync disable-external-cache\
commit\
save

**LB1B**\
set high-availability vrrp group FWCluster vrid 1\
set high-availability vrrp group FWCluster interface eth3\
set high-availability vrrp group FWCluster virtual-address 192.168.100.1/24\
set high-availability vrrp sync-group FWCluster member FWCluster\
set high-availability vrrp group FWCluster rfc3768-compatibility

conntrack-sync\
set service conntrack-sync accept-protocol 'tcp,udp,icmp'\
set service conntrack-sync failover-mechanism vrrp sync-group FWCluster\
set service conntrack-sync interface eth3\
set service conntrack-sync mcast-group 225.0.0.50\
set service conntrack-sync disable-external-cache\
commit\
save

**LB2A**\
set high-availability vrrp group FWCluster vrid 1\
set high-availability vrrp group FWCluster interface eth3\
set high-availability vrrp group FWCluster virtual-address 192.0.2.1/30\
set high-availability vrrp sync-group FWCluster member FWCluster\
set high-availability vrrp group FWCluster rfc3768-compatibility

conntrack-sync\
set service conntrack-sync accept-protocol 'tcp,udp,icmp'\
set service conntrack-sync failover-mechanism vrrp sync-group FWCluster\
set service conntrack-sync interface eth3\
set service conntrack-sync mcast-group 225.0.0.50\
set service conntrack-sync disable-external-cache\
commit\
save

**LB2B**\
set high-availability vrrp group FWCluster vrid 1\
set high-availability vrrp group FWCluster interface eth3\
set high-availability vrrp group FWCluster virtual-address 192.0.2.1/30\
set high-availability vrrp sync-group FWCluster member FWCluster\
set high-availability vrrp group FWCluster rfc3768-compatibility

conntrack-sync\
set service conntrack-sync accept-protocol 'tcp,udp,icmp'\
set service conntrack-sync failover-mechanism vrrp sync-group FWCluster\
set service conntrack-sync interface eth3\
set service conntrack-sync mcast-group 225.0.0.50\
set service conntrack-sync disable-external-cache\
commit\
save

### LOAD-BALANCERES LOAD BALANCING SERVICE CONFIGURATIONS 

**LB1A**\
set load-balancing wan interface-health eth1 nexthop 10.3.0.10\
set load-balancing wan interface-health eth2 nexthop 10.0.4.2\
set load-balancing wan rule 1 inbound-interface eth0\
set load-balancing wan rule 1 interface eth1 weight 1\
set load-balancing wan rule 1 interface eth2 weight 1\
set load-balancing wan sticky-connections inbound\
set load-balancing wan disable-source-nat 

**LB1B**\
set load-balancing wan interface-health eth1 nexthop 10.0.2.12\
set load-balancing wan interface-health eth2 nexthop 10.1.0.110\
set load-balancing wan rule 1 inbound-interface eth0\
set load-balancing wan rule 1 interface eth4 weight 1\
set load-balancing wan rule 1 interface eth2 weight 1\
set load-balancing wan sticky-connections inbound\
set load-balancing wan disable-source-nat 

**LB2A**\
set load-balancing wan interface-health eth2 nexthop 10.0.5.11\
set load-balancing wan interface-health eth1 nexthop 10.2.0.11\
set load-balancing wan rule 1 inbound-interface eth0\
set load-balancing wan rule 1 interface eth2 weight 1\
set load-balancing wan rule 1 interface eth1 weight 1\
set load-balancing wan sticky-connections inbound\
set load-balancing wan disable-source-nat 

**LB2B**\
set load-balancing wan interface-health eth1 nexthop 10.0.3.20\
set load-balancing wan interface-health eth2 nexthop 10.4.0.10\
set load-balancing wan rule 1 inbound-interface eth0\
set load-balancing wan rule 1 interface eth2 weight 1\
set load-balancing wan sticky-connections inbound\
set load-balancing wan disable-source-nat 

## NETWORK SECURITY ZONES DEFINICIONS and RULES on FWS

**FW1 and FW2**\
set zone-policy zone INSIDE description "Rede interna privada"\
set zone-policy zone INSIDE interface eth0\
set zone-policy zone INSIDE interface eth1\
set zone-policy zone OUTSIDE description "Internet"\
set zone-policy zone OUTSIDE interface eth2\
set zone-policy zone OUTSIDE interface eth3\
set zone-policy zone DMZ description "Zona desmilitarizada"\
set zone-policy zone DMZ interface eth5\
commit\
save 

### RULES CONTROLS FLOWS 

**INSIDE-OUTSIDE and OUTSIDE-INSIDE**\
set firewall name FROM-INSIDE-TO-OUTSIDE rule 1 description "Allow all traffic from inside to outside"\
set firewall name FROM-INSIDE-TO-OUTSIDE rule 1 action accept\
set firewall name FROM-INSIDE-TO-OUTSIDE rule 1 protocol icmp\
set firewall name FROM-INSIDE-TO-OUTSIDE rule 1 icmp type 8\
set firewall name TO-INSIDE rule 1 description "Allow established and related connections from outside to inside"\
set firewall name TO-INSIDE rule 1 action accept\
set firewall name TO-INSIDE rule 1 state established enable\
set firewall name TO-INSIDE rule 1 state related enable

set firewall name FROM-INSIDE-TO-OUTSIDE rule 2 description "Allow access to outside using port 80"\
set firewall name FROM-INSIDE-TO-OUTSIDE rule 2 action accept\
set firewall name FROM-INSIDE-TO-OUTSIDE rule 2 protocol tcp\
set firewall name FROM-INSIDE-TO-OUTSIDE rule 2 destination port 80\
set firewall name TO-INSIDE rule 2 description "Allow established and related connections from outside to inside"\
set firewall name TO-INSIDE rule 2 action accept\
set firewall name TO-INSIDE rule 2 state established enable\
set firewall name TO-INSIDE rule 2 state related enable

set firewall name FROM-INSIDE-TO-OUTSIDE rule 3 description "Allow access to outside using port 443"\
set firewall name FROM-INSIDE-TO-OUTSIDE rule 3 action accept\
set firewall name FROM-INSIDE-TO-OUTSIDE rule 3 protocol tcp\
set firewall name FROM-INSIDE-TO-OUTSIDE rule 3 destination port 443\
set firewall name TO-INSIDE rule 3 description "Allow established and related connections from outside to inside"\
set firewall name TO-INSIDE rule 3 action accept\
set firewall name TO-INSIDE rule 3 state established enable\
set firewall name TO-INSIDE rule 3 state related enable

set zone-policy zone INSIDE from OUTSIDE firewall name TO-INSIDE\
set zone-policy zone OUTSIDE from INSIDE firewall name FROM-INSIDE-TO-OUTSIDE

set firewall name FROM-OUTSIDE-TO-INSIDE rule 8 description "Deny IP similiar to Inside"\
set firewall name FROM-OUTSIDE-TO-INSIDE rule 8 action drop\
set firewall name FROM-OUTSIDE-TO-INSIDE rule 8 source address 10.0.0.0/8

set firewall name FROM-OUTSIDE-TO-INSIDE rule 9 description "Deny incoming traffic from the Internet"\
set firewall name FROM-OUTSIDE-TO-INSIDE rule 9 action drop\
set firewall name FROM-OUTSIDE-TO-INSIDE rule 9 state invalid enable\
set firewall name FROM-OUTSIDE-TO-INSIDE rule 9 destination address 10.0.0.0/8

set zone-policy zone INSIDE from OUTSIDE firewall name FROM-OUTSIDE-TO-INSIDE\
commit

**INSIDE-DMZ**\
set firewall name FROM-INSIDE-TO-DMZ rule 10 description "Accept ICMP Echo Request"\
set firewall name FROM-INSIDE-TO-DMZ rule 10 action accept\
set firewall name FROM-INSIDE-TO-DMZ rule 10 protocol icmp \
set firewall name FROM-INSIDE-TO-DMZ rule 10 icmp type 8\
set firewall name FROM-INSIDE-TO-DMZ rule 10 destination address 192.1.1.100\
set firewall name TO-INSIDE-OF-DMZ rule 10 description "Accept Established-Related Connections"\
set firewall name TO-INSIDE-OF-DMZ rule 10 action accept\
set firewall name TO-INSIDE-OF-DMZ rule 10 state established enable\
set firewall name TO-INSIDE-OF-DMZ rule 10 state related enable\
commit

set firewall name FROM-INSIDE-TO-DMZ rule 11 description "Allow HTTP traffic"\
set firewall name FROM-INSIDE-TO-DMZ rule 11 action accept\
set firewall name FROM-INSIDE-TO-DMZ rule 11 protocol tcp\
set firewall name FROM-INSIDE-TO-DMZ rule 11 destination port 80\
set firewall name FROM-INSIDE-TO-DMZ rule 11 destination address 192.1.1.100/32\
set firewall name TO-INSIDE-OF-DMZ rule 11 description "Accept HTTP Established-Related Connections"\
set firewall name TO-INSIDE-OF-DMZ rule 11 action accept\
set firewall name TO-INSIDE-OF-DMZ rule 11 state established enable\
set firewall name TO-INSIDE-OF-DMZ rule 11 state related enable

set firewall name FROM-INSIDE-TO-DMZ rule 12 description "Allow DNS traffic UDP"\
set firewall name FROM-INSIDE-TO-DMZ rule 12 action accept\
set firewall name FROM-INSIDE-TO-DMZ rule 12 protocol udp\
set firewall name FROM-INSIDE-TO-DMZ rule 12 destination port 53\
set firewall name FROM-INSIDE-TO-DMZ rule 12 destination address 192.1.1.100/32\
set firewall name TO-INSIDE-OF-DMZ rule 12 description "Accept DNS Established-Related Connections"\
set firewall name TO-INSIDE-OF-DMZ rule 12 action accept\
set firewall name TO-INSIDE-OF-DMZ rule 12 state established enable\
set firewall name TO-INSIDE-OF-DMZ rule 12 state related enable

set firewall name FROM-INSIDE-TO-DMZ rule 13 description "Allow DNS traffic TCP"\
set firewall name FROM-INSIDE-TO-DMZ rule 13 action accept\
set firewall name FROM-INSIDE-TO-DMZ rule 13 protocol tcp\
set firewall name FROM-INSIDE-TO-DMZ rule 13 destination port 53\
set firewall name FROM-INSIDE-TO-DMZ rule 13 destination address 192.1.1.100/32\
set firewall name TO-INSIDE-OF-DMZ rule 13 description "Accept DNS Established-Related Connections"\
set firewall name TO-INSIDE-OF-DMZ rule 13 action accept\
set firewall name TO-INSIDE-OF-DMZ rule 13 state established enable\
set firewall name TO-INSIDE-OF-DMZ rule 13 state related enable

set firewall name FROM-INSIDE-TO-DMZ rule 14 description "Allow HTTPS"\
set firewall name FROM-INSIDE-TO-DMZ rule 14 action accept\
set firewall name FROM-INSIDE-TO-DMZ rule 14 protocol tcp\
set firewall name FROM-INSIDE-TO-DMZ rule 14 destination port 443\
set firewall name FROM-INSIDE-TO-DMZ rule 14 destination address 192.1.1.100/32\
set firewall name TO-INSIDE-OF-DMZ rule 14 description "Accept HTTPS Established-Related Connections"\
set firewall name TO-INSIDE-OF-DMZ rule 14 action accept\
set firewall name TO-INSIDE-OF-DMZ rule 14 state established enable\
set firewall name TO-INSIDE-OF-DMZ rule 14 state related enable

set firewall name FROM-INSIDE-TO-DMZ rule 15 description "Allow SSH"\
set firewall name FROM-INSIDE-TO-DMZ rule 15 action accept\
set firewall name FROM-INSIDE-TO-DMZ rule 15 protocol tcp\
set firewall name FROM-INSIDE-TO-DMZ rule 15 destination port 22\
set firewall name FROM-INSIDE-TO-DMZ rule 15 destination address 192.1.1.100/32\
set firewall name TO-INSIDE-OF-DMZ rule 15 description "Accept SSH Established-Related Connections"\
set firewall name TO-INSIDE-OF-DMZ rule 15 action accept\
set firewall name TO-INSIDE-OF-DMZ rule 15 state established enable\
set firewall name TO-INSIDE-OF-DMZ rule 15 state related enable

set firewall name FROM-INSIDE-TO-DMZ rule 16 description "Allow FTP"\
set firewall name FROM-INSIDE-TO-DMZ rule 16 action accept\
set firewall name FROM-INSIDE-TO-DMZ rule 16 protocol tcp\
set firewall name FROM-INSIDE-TO-DMZ rule 16 destination port 20-21\
set firewall name FROM-INSIDE-TO-DMZ rule 16 destination address 192.1.1.100/32\
set firewall name TO-INSIDE-OF-DMZ rule 16 description "Accept FTP Established-Related Connections"\
set firewall name TO-INSIDE-OF-DMZ rule 16 action accept\
set firewall name TO-INSIDE-OF-DMZ rule 16 state established enable\
set firewall name TO-INSIDE-OF-DMZ rule 16 state related enable

set firewall name FROM-INSIDE-TO-DMZ rule 17 description "Allow SMTPS"\
set firewall name FROM-INSIDE-TO-DMZ rule 17 action accept\
set firewall name FROM-INSIDE-TO-DMZ rule 17 protocol tcp \
set firewall name FROM-INSIDE-TO-DMZ rule 17 destination port 465\
set firewall name FROM-INSIDE-TO-DMZ rule 17 destination address 192.1.1.100/32\
set firewall name TO-INSIDE-OF-DMZ rule 17 description "Accept SMTP Established-Related Connections"\
set firewall name TO-INSIDE-OF-DMZ rule 17 action accept\
set firewall name TO-INSIDE-OF-DMZ rule 17 state established enable\
set firewall name TO-INSIDE-OF-DMZ rule 17 state related enable

set firewall name FROM-INSIDE-TO-DMZ rule 18 description "Allow IMAPS"\
set firewall name FROM-INSIDE-TO-DMZ rule 18 action accept\
set firewall name FROM-INSIDE-TO-DMZ rule 18 protocol tcp \
set firewall name FROM-INSIDE-TO-DMZ rule 18 destination port 993\
set firewall name FROM-INSIDE-TO-DMZ rule 18 destination address 192.1.1.100/32\
set firewall name TO-INSIDE-OF-DMZ rule 18 description "Accept SMTP Established-Related Connections"\
set firewall name TO-INSIDE-OF-DMZ rule 18 action accept\
set firewall name TO-INSIDE-OF-DMZ rule 18 state established enable\
set firewall name TO-INSIDE-OF-DMZ rule 18 state related enable\
commit

set zone-policy zone INSIDE from DMZ firewall name TO-INSIDE-OF-DMZ\
set zone-policy zone DMZ from INSIDE firewall name FROM-INSIDE-TO-DMZ

**DMZ-INSIDE**

set firewall name FROM-DMZ-TO-INSIDE rule 30 description "Deny traffic from DMZ to inside"\
set firewall name FROM-DMZ-TO-INSIDE rule 30 action drop\
set firewall name FROM-DMZ-TO-INSIDE rule 30 state invalid enable\
set firewall name FROM-DMZ-TO-INSIDE rule 30 destination address 10.0.0.0/8\

set zone-policy zone INSIDE from DMZ firewall name FROM-DMZ-TO-INSIDE\
commit


**INTERNET-DMZ**

set firewall name FROM-INTERNET-TO-DMZ rule 10 description "Allow HTTP traffic from Internet to DMZ"\
set firewall name FROM-INTERNET-TO-DMZ rule 10 action accept\
set firewall name FROM-INTERNET-TO-DMZ rule 10 protocol tcp\
set firewall name FROM-INTERNET-TO-DMZ rule 10 destination port 80\
set firewall name FROM-INTERNET-TO-DMZ rule 10 destination address 192.1.1.100/32\
set firewall name TO-DMZ-FROM-INTERNET rule 10 description "Accept Established-Related Connections"\
set firewall name TO-DMZ-FROM-INTERNET rule 10 action accept\
set firewall name TO-DMZ-FROM-INTERNET rule 10 state established enable\
set firewall name TO-DMZ-FROM-INTERNET rule 10 state related enable

set firewall name FROM-INTERNET-TO-DMZ rule 20 description "Allow HTTPS traffic from Internet to DMZ"\
set firewall name FROM-INTERNET-TO-DMZ rule 20 action accept\
set firewall name FROM-INTERNET-TO-DMZ rule 20 protocol tcp\
set firewall name FROM-INTERNET-TO-DMZ rule 20 destination port 443\
set firewall name FROM-INTERNET-TO-DMZ rule 20 destination address 192.1.1.100/32\
set firewall name TO-DMZ-FROM-INTERNET rule 20 description "Accept Established-Related Connections"\
set firewall name TO-DMZ-FROM-INTERNET rule 20 action accept\
set firewall name TO-DMZ-FROM-INTERNET rule 20 state established enable\
set firewall name TO-DMZ-FROM-INTERNET rule 20 state related enable

set firewall name FROM-INTERNET-TO-DMZ rule 30 description "Allow DNS traffic from Internet to DMZ"\
set firewall name FROM-INTERNET-TO-DMZ rule 30 action accept\
set firewall name FROM-INTERNET-TO-DMZ rule 30 protocol tcp\
set firewall name FROM-INTERNET-TO-DMZ rule 30 destination port 53\
set firewall name FROM-INTERNET-TO-DMZ rule 30 destination address 192.1.1.100/32\
set firewall name TO-DMZ-FROM-INTERNET rule 30 description "Accept Established-Related Connections"\
set firewall name TO-DMZ-FROM-INTERNET rule 30 action accept\
set firewall name TO-DMZ-FROM-INTERNET rule 30 state established enable\
set firewall name TO-DMZ-FROM-INTERNET rule 30 state related enable

set firewall name FROM-INTERNET-TO-DMZ rule 40 description "Allow DNS traffic from Internet to DMZ"\
set firewall name FROM-INTERNET-TO-DMZ rule 40 action accept\
set firewall name FROM-INTERNET-TO-DMZ rule 40 protocol udp\
set firewall name FROM-INTERNET-TO-DMZ rule 40 destination port 53\
set firewall name FROM-INTERNET-TO-DMZ rule 40 destination address 192.1.1.100/32\
set firewall name TO-DMZ-FROM-INTERNET rule 40 description "Accept Established-Related Connections"\
set firewall name TO-DMZ-FROM-INTERNET rule 40 action accept\
set firewall name TO-DMZ-FROM-INTERNET rule 40 state established enable\
set firewall name TO-DMZ-FROM-INTERNET rule 40 state related enable

set firewall name FROM-INTERNET-TO-DMZ rule 50 description "Allow SMTPS"\
set firewall name FROM-INTERNET-TO-DMZ rule 50 action accept\
set firewall name FROM-INTERNET-TO-DMZ rule 50 protocol tcp \
set firewall name FROM-INTERNET-TO-DMZ rule 50 destination port 465\
set firewall name FROM-INTERNET-TO-DMZ rule 50 destination address 192.1.1.100/32\
set firewall name TO-DMZ-FROM-INTERNET rule 50 description "Accept Established-Related Connections"\
set firewall name TO-DMZ-FROM-INTERNET rule 50 action accept\
set firewall name TO-DMZ-FROM-INTERNET rule 50 state established enable\
set firewall name TO-DMZ-FROM-INTERNET rule 50 state related enable

set firewall name FROM-INTERNET-TO-DMZ rule 60 description "Allow IMAPS"\
set firewall name FROM-INTERNET-TO-DMZ rule 60 action accept\
set firewall name FROM-INTERNET-TO-DMZ rule 60 protocol tcp \
set firewall name FROM-INTERNET-TO-DMZ rule 60 destination port 993\
set firewall name FROM-INTERNET-TO-DMZ rule 60 destination address 192.1.1.100/32\
set firewall name TO-DMZ-FROM-INTERNET rule 60 description "Accept Established-Related Connections"\
set firewall name TO-DMZ-FROM-INTERNET rule 60 action accept\
set firewall name TO-DMZ-FROM-INTERNET rule 60 state established enable\
set firewall name TO-DMZ-FROM-INTERNET rule 60 state related enable

set zone-policy zone DMZ from OUTSIDE firewall name FROM-INTERNET-TO-DMZ\
set zone-policy zone OUTSIDE from DMZ firewall name TO-DMZ-FROM-INTERNET\
commit\
save

**DMZ-INTERNET**

set firewall name FROM-DMZ-TO-OUTSIDE rule 41 description "Allow access to servers to update"\
set firewall name FROM-DMZ-TO-OUTSIDE rule 41 action accept\
set firewall name FROM-DMZ-TO-OUTSIDE rule 41 protocol tcp\
set firewall name FROM-DMZ-TO-OUTSIDE rule 41 destination port 80\
set firewall name FROM-DMZ-TO-OUTSIDE rule 41 source address 200.2.2.100/32\
set firewall name TO-DMZ rule 41 description "Accept Established-Related Connections"\
set firewall name TO-DMZ rule 41 action accept\
set firewall name TO-DMZ rule 41 state established enable\
set firewall name TO-DMZ rule 41 state related enable

set firewall name FROM-DMZ-TO-OUTSIDE rule 42 description "Allow access to servers to update"\
set firewall name FROM-DMZ-TO-OUTSIDE rule 42 action accept\
set firewall name FROM-DMZ-TO-OUTSIDE rule 42 protocol tcp\
set firewall name FROM-DMZ-TO-OUTSIDE rule 42 destination port 443\
set firewall name FROM-DMZ-TO-OUTSIDE rule 42 source address 200.2.2.100/32\
set firewall name TO-DMZ rule 42 description "Accept Established-Related Connections"\
set firewall name TO-DMZ rule 42 action accept\
set firewall name TO-DMZ rule 42 state established enable\
set firewall name TO-DMZ rule 42 state related enable

set firewall name FROM-DMZ-TO-OUTSIDE rule 43 description "Allow access to servers to update"\
set firewall name FROM-DMZ-TO-OUTSIDE rule 43 action accept\
set firewall name FROM-DMZ-TO-OUTSIDE rule 43 protocol tcp\
set firewall name FROM-DMZ-TO-OUTSIDE rule 43 destination port 53\
set firewall name FROM-DMZ-TO-OUTSIDE rule 43 source address 200.2.2.100/32\
set firewall name TO-DMZ rule 43 description "Accept Established-Related Connections"\
set firewall name TO-DMZ rule 43 action accept\
set firewall name TO-DMZ rule 43 state established enable\
set firewall name TO-DMZ rule 43 state related enable

set firewall name FROM-DMZ-TO-OUTSIDE rule 44 description "Allow access to servers to update"\
set firewall name FROM-DMZ-TO-OUTSIDE rule 44 action accept\
set firewall name FROM-DMZ-TO-OUTSIDE rule 44 protocol tcp\
set firewall name FROM-DMZ-TO-OUTSIDE rule 44 destination port 465\
set firewall name FROM-DMZ-TO-OUTSIDE rule 44 source address 200.2.2.100/32\
set firewall name TO-DMZ rule 44 description "Accept Established-Related Connections"\
set firewall name TO-DMZ rule 44 action accept\
set firewall name TO-DMZ rule 44 state established enable\
set firewall name TO-DMZ rule 44 state related enable

set firewall name FROM-DMZ-TO-OUTSIDE rule 45 description "Allow access to servers to update"\
set firewall name FROM-DMZ-TO-OUTSIDE rule 45 action accept\
set firewall name FROM-DMZ-TO-OUTSIDE rule 45 protocol tcp\
set firewall name FROM-DMZ-TO-OUTSIDE rule 45 destination port 993\
set firewall name FROM-DMZ-TO-OUTSIDE rule 45 source address 200.2.2.100/32\
set firewall name TO-DMZ rule 45 description "Accept Established-Related Connections"\
set firewall name TO-DMZ rule 45 action accept\
set firewall name TO-DMZ rule 45 state established enable\
set firewall name TO-DMZ rule 45 state related enable

set zone-policy zone DMZ from OUTSIDE firewall name TO-DMZ\
set zone-policy zone OUTSIDE from DMZ firewall name FROM-DMZ-TO-OUTSIDE\
commit\
save