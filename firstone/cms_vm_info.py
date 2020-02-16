import cms
import glob
import sys

# checking folder and
class nova_cms_vm_info:
    def cms_vm_info_m(self, filename,dbstring):
        #print(filename)
        filex = filename
        file = glob.glob(filex + "*.txt")
        #print(file)
        for filename in file:
            filtername = filename.replace(filex, "")
            circle = str(filtername.split('_')[0])
            entity_type = filtername.split('_')[1]
            dttime = filtername.split('_')[2].replace('.txt', '')
            cms_call = cms.test()
            data = cms_call.data_pars(filename, '--virsh cms1  list start--',
                                      '--virsh cms2  list finish--')
#            delete_data = " delete FROM epc.cms_vm_info where dttime = STR_TO_DATE('" + dttime + "','%Y%m%d%H%i') and circle = '"+circle+"';"
            delete_data=""
            query1 = " insert into epc.cms_vm_info(vmname, status, entity_name, dttime, circle) values"
            query2 = ""
            for x in data:
                #print(x)
                if x.__contains__('vnfm') or x.__contains__('pim') or  x.__contains__('nfvo') or x.__contains__('osc'):
                    #print(x.strip())
                    vmname = x.replace(x.split(' ')[-1].strip(),'').strip().split(' ')[-1].strip()
                    #print(x.strip().split(' ')[0])
                    status = x.split(' ')[-1].strip()
                    # zone = x.split('|')[5].strip()
                    query = "('" + vmname + "','" + status + "','" + entity_type + "',STR_TO_DATE('" + dttime + "','%Y%m%d%H%i'),'" + circle + "'),"
                    query2 = query2 + query

            query_final = query1 + " " + query2
            query_final = delete_data + " " + query_final[0:len(query_final) - 1]
            #print(query_final)
            #sys.exit(0)
            try:
                cnx = dbstring
                print('connected to localhost')
                cursor = cnx.cursor()
                #cursor.execute(query_final)
                for _ in cursor.execute(query_final, multi=True): pass

                cnx.commit()
                cursor.close()
                #cnx.close()
                print("successfully executed")
            except NameError as ex:
                print(ex)

            del data[:]