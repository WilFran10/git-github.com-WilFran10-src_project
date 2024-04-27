
#!/usr/bin/python3

import paramiko
from argparse import ArgumentParser, ArgumentTypeError




def block_ip_addresses(ipList, username, password, hostname):
    # Conectando ao firewall via SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)

    for ip in ipList:

        # Comando para bloquear o IP no firewall
        comando = f"configure\nset firewall name BLOQUEIO rule 1 source address {ip}\ncommit\nsave\nexit"

        # Enviando o comando via SSH
        stdin, stdout, stderr = ssh.exec_command(comando)

        # Verificando se ocorreu algum erro
        if stderr.channel.recv_exit_status() != 0:
            print(f"Erro ao bloquear o IP {ip}")
    # Fechando a conexão SSH
    ssh.close()


#----------------------------------------------------------------------------
# Arguments


def get_argument_parser():
    parser = ArgumentParser(
        usage='%(prog)s [OPTIONS]',
        description='Block ip addresses firewall using ssh'
    )

    # IP addresses to blacklsit

    source_group = parser.add_mutually_exclusive_group()


    source_group.add_argument(
        '-i',
        '--ip',
        help='specify a single ip address to blacklist'
    )
    source_group.add_argument(
        '-l',
        '--listFile',
        help='specify a file wich contains a list of ip addresses to blacklist\nList seperated by line breaks'
    )

    # Hostname, user and password

    parser.add_argument(
        '-u',
        '--user',
        help='specify the ssh user to login to the firewall',required=True
    )

    parser.add_argument(
        '-o',
        '--hostname',
        help='specify the ssh hostname to login to the firewall',required=True
    )

    parser.add_argument(
        '-p',
        '--password',
        help='specify the ssh password to login to the firewall',required=True
    )



    return parser

def parse_arguments():
    parser = get_argument_parser()
    return parser.parse_args()



#----------------------------------------------------------------------------
# Parse file

def parse_ip_list_file(filename: str) -> list:
    
    lines = []
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]

    
    return lines

#----------------------------------------------------------------------------
# Main

if __name__ == "__main__":


    # Parse Arguments
    args = parse_arguments()


    username = args.user
    password = args.password
    hostname = args.hostname


    singleIp = args.ip
    fileList = args.listFile
    

    list_of_ips = []

    if singleIp != None:

        list_of_ips.append(singleIp)
        print(list_of_ips)
        block_ip_addresses(list_of_ips, username, password, hostname)
    
    else: 

        list_of_ips = parse_ip_list_file(filename=fileList)
 
        print(list_of_ips)
        block_ip_addresses(list_of_ips, username, password, hostname)