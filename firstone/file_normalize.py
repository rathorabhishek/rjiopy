import os

def deleteLine(path1):

    circl_dict = {"UW": 1, "GJ": 2, "HR": 3, "WB": 4, "KA": 5, "MP": 6, "OR": 7, "KL": 9, "AS": 10, "AP": 11, "KO": 12,
                  "UE": 13, "PB": 14,"RC": 15, "MU": 16, "MH": 17, "DL": 18, "BR": 19, "RJ": 20, "HP": 21, "JK": 22, "TN": 24, "NE": 29}
    listOfFiles = os.listdir(path1)
    for files in listOfFiles:
        print(files)
        os.chdir(path1)
        if (files.__contains__(".csv") and os.stat(files).st_size >0):
            fn = files
            cir = files.split('.')[0]
            typ = files.split('.')[1]
            if (cir == "PB"):
                cir = "PU"

            f = open(path1 + fn)
            output = []
            for line in f:
                node = line.split('|')[0][0:2]
                # need to put except for bihar and punjab circle ...
                if (node.upper() == cir):
                    output.append(line)

            f.close()
            os.remove(path1 + fn)
            if (cir == "PU"):
                cir = "PB"
            opnpath =path1 + cir+"."+typ+"."+str(circl_dict[cir])+".csv"
            print(opnpath)
            f = open(opnpath , 'a+')
            f.writelines(output)

            f.close()


def copy(path1):
    # first read file .. if txt find .then search file for same an
    print("you entered ")
    listOfFiles = os.listdir(path1)

    for files in listOfFiles:
        #print(files)

        os.chdir(path1)
        if (files.__contains__(".csv") and os.stat(files).st_size >0):
            fileread = open(path1 + files, 'r+').readlines()
            cir = files.split('.')[0]
            if(cir=="PB"):
                cir="PU"
            typ = files.split('.')[1]
            print(cir,typ)
            for x in fileread:
                node = x.split('|')[0][0:2]
                #print(node)
                print(node.upper())
                # print(cir)

                if (node.upper() != cir):
                    print("you are here")

                    # print("in " +cir + " node :" +node + " existed")
                    # checking all avialable file to insert data of node into respective circle file
                    for checkfile in listOfFiles:
                        cir_in_chckfile=checkfile.split('.')[0]
                        type_in_chckfile= checkfile.split('.')[1]

                        if (cir_in_chckfile == node.upper() and type_in_chckfile== typ):
                            # print(checkfile)
                            fileappend = open(path1 + checkfile, 'a+')
                            fileappend.writelines(x)
                            print(x + ' is written on file ' + checkfile)
                            # time.sleep(1)
                            #files.replace(x, '\n')
                            # fileread.remove(x);
                            fileappend.close()
                            break
path = "C:\\abhishek\project\python\\sgw_mme_throughput\\201906251045\\"
copy(path)
deleteLine(path)