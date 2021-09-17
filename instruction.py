from config.node_config import *


def datanode_intro():
    company_info = read_in_companyinfo()
    str_info = ''
    for i in company_info:
        if i != '':
            str_info = str_info+i + '\n'
    print(f"""============================================
    Welcome to DP-Face v0.01 System
============================================
\nThere are some company information as follow 
name : ip_addr
{str_info}
============================================
""")


def companynode_intro():
    consensus_info = read_in_consensusinfo()
    str_info = ''
    for i in consensus_info:
        if i != '':
            str_info = str_info+i + '\n'
    print(f"""============================================
    Welcome to DP-Face v0.01 System
============================================
\nThere are some consensus as follow 
{str_info}
============================================
""")


def consensusnode_intro():
    company_info = read_in_companyinfo()
    str_info = ''
    for i in company_info:
        if i != '':
            str_info = str_info+i + '\n'
    print(f"""============================================
    Welcome to DP-Face v0.01 System
============================================
\nThere are some company information as follow 
name : ip_addr
{str_info}
============================================
""")
