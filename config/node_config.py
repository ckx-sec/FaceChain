
def write_in_companyinfo(company_node_info: str):
    filename = "./config/company_info.txt"
    with open(filename, "a") as f:
        f.write(company_node_info+'\n')


def read_in_companyinfo():
    filename = "./config/company_info.txt"
    with open(filename, "r") as f:
        company_node_info = f.read()
        alist = company_node_info.split('\n')
        alist.pop()
        return alist


def write_in_consensusinfo(consensus_node_info: str):

    filename = "./config/consensus_info.txt"
    with open(filename, "a") as f:
        f.write(consensus_node_info+'\n')


def read_in_consensusinfo():
    filename = "./config/consensus_info.txt"
    with open(filename, "r") as f:
        consensus_node_info = f.read()
        alist = consensus_node_info.split('\n')
        alist.pop()
        return alist
