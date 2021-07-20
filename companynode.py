import requests

class companynode:
    def __init__(self,ip_addr):
        self.name = ''
        self.ip_addr = ip_addr
        self.public_key = ''
        self.private_key = ''
        self.employeelist = []
        self.mpks = []
        self.z = []
        self.sks = []
        self.training_images_hash = []
        self.test_images = []

    def broadcast_z(self):
        for employee in self.employeelist:
            try:
                # modify
                requests.post('{0}/DP-Face/{1}/z'.format(employee,self.name),json=self.z)
            except Exception as e:
                print('[{0} broadcast z error:{1}'.format(self.name,e))
        return


    def store_in_IPFS(self):
        """
        store z in IPFS
        """
        z_hash = ''
        return z_hash

    def pull(self,blockchain):
        pass

    def broadcast_public_key(self):
        for employee in self.employeelist:
            try:
                # modify
                requests.post('{0}/DP-Face/{1}/public_key'.format(employee,self.name),json=self.public_key)
            except Exception as e:
                print('[{0} broadcast public key error:{1}'.format(self.name,e))
        return

    def pull_sk(self):
        """
        Get the employees' sk
        """
        pass

    def padding_z(self):
        """
        To use mpks padding in 512*512 Matrix
        """
        pass

    def issue_task(self,tasklist):
        """
        Package the mpks and training_images_hash to task

        """
        task = {
            'mpks': self.mpks,
            'training_images_hash': self.training_images_hash,
        }
        tasklist.append(task)
        
        return tasklist


    def issue_sks(self,blockchain):
        """
        if the task in the last block is issued by this company, issue the sks at that time
        in order to prevent too early training
        """
        pass

    def issue_test_images_hash(self,):

        pass