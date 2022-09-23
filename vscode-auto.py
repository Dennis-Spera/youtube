#!/usr/local/bin/python
import paramiko
from paramiko import SSHClient
from scp import SCPClient
import os

servers = [
            {
              'server':'???.???.???.???', 
              'user':'????',
              'password':'??????????'
            },
            {
              'server':'???.???.???.???', 
              'user':'????',
              'password':'??????????'
            },
            {
              'server':'???.???.???.???', 
              'user':'????',
              'password':'??????????'
            }              
          ]

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
for server in servers:

    client.connect( server['server'], 22, server['user'], server['password'] )
    scp = SCPClient(client.get_transport())         
    scp.put(os.environ["HOME"]+'/.ssh/id_rsa.pub', '/tmp')    

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server['server'], 22, server['user'], server['password'], timeout=5)

    sshCmd = "cd $HOME; cat /tmp/id_rsa.pub >> $HOME/.ssh/authorized_keys; rm /tmp/id_rsa.pub"

    stdin, stdout, stderr = ssh.exec_command(sshCmd)
    stdin.write(server['password']+"\n")  # Password for sudo
    stdin.flush()
    stdin.close()


   # git-bash running under native win10
   # sh-5.1$ ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa <<<y >/dev/null 2>&1;  python vscode-auto.py
