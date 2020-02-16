
import py_lib

filex = open('C:\\mylog\\dra\\output\\processed.txt',"w")
#file.close()
#exit()
def v6_filter(path):
    file = open(path, 'r')
    hostname = path.split('//')[1].split('_')[1]
    print(hostname)
    line = "src,destination,result "
    line =  line + '\n'
    for x in file:
        if (x.__contains__('Internet Protocol Version 6, Src:')):
            line = line + 'IPV6,' + hostname + ','
            line = line + x.split(' ')[6].strip().replace('(', '').replace(')', '')
            line = line + x.split(' ')[9].strip().replace('(', '').replace(')', '')
            line = line + ','
        if (x.__contains__('Differentiated Services Field:')):
            if line.__contains__(':'):
                line = line + x.strip()
                line = line + '\n'
    filex.writelines(line)
    #print(line)
    #return line

def v4_filter(path):
    file = open(path, 'r')
    hostname = path.split('//')[1].split('_')[1]
    line = "src,destination,result "
    line =  line + '\n'
    for x in file:
        if (x.__contains__('Internet Protocol Version 4, Src:')):
            line = line + 'IPV4,' + hostname + ','
            line = line + x.split(' ')[6].strip().replace('(', '').replace(')', '')
            line = line + x.split(' ')[9].strip().replace('(', '').replace(')', '')
            line = line + ','
        if (x.__contains__('Differentiated Services Field:')):
            if(len(line)>30):
                line = line + x.strip()
                line = line + '\n'
        #print(line)
    filex.writelines(line)
    #print(line)
    #return(line)


path='C:\\mylog\\dra\\raw'
file_name=py_lib.py_help_r.get_file_detail(path,'*')
for files in file_name:
    print("Processing for file : " +files)
    v6_filter(path+"//"+ files)
    v4_filter(path + "//" + files)


