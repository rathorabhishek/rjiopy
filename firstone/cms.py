# read first file osc1.txt getting nova list .
# getting host count
# command nova hypervisor-list
# Author : Abhishek Rathor
# ----------------------------------------

class  test:
    def __init__(self):
        pass
    def split_data(self,filename, readline,second_split,data =[]):
        with open(filename, 'r') as osc:
            for i in xrange(readline):
                osc.next()
            for line in osc:
                #print(line.strip())
                data.append(line.strip())

                if line.__contains__(second_split):
                    return data
                    break

    def data_pars(self,filename,first_split,second_split):
        osc_file = open(filename, 'r').read()
        osc_file_split = osc_file.split('\n')
        i = 0
        data=[]
        del data[:]
        for line in osc_file_split:
            i = i + 1
            if line.__contains__(first_split):
                #print(i)
                data=self.split_data(filename,i,second_split)
                return  data
                break

