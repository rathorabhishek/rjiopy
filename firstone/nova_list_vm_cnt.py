import cms
import glob
import mysql.connector
# checking folder and

class nov_list_vm_cnt:
    def nova_list_vm_cnt(self, filename,dbstring):
        filex = filename
        file = glob.glob(filex + "*.txt")
        for filename in file:

            filtername = filename.replace(filex, "")

            circle = str(filtername.split('_')[0])
            entity_type = filtername.split('_')[1]
            dttime = filtername.split('_')[2].replace('.txt', '')

            cms_call = cms.test()
            data = cms_call.data_pars(filename, '--nova list-start--', '-nova list-finish-')
            #delete_data = "delete FROM epc.cms_nova_list_vm_cnt where dttime = STR_TO_DATE('" + dttime + "','%Y%m%d%H%i') and circle = '"+circle+"' ;"
            delete_data=""
            query1 = "insert into epc.cms_nova_list_vm_cnt(vm_name, status, power_state, entity_name, dttime, circle) values"
            query2 = ""
            for x in data:
                if not x.__contains__('----') and not x.__contains__('osc') and not x.__contains__(
                        'OSC') and not x.__contains__(
                    'host_name'):
                    # print(x.strip())
                    hostname = x.split('|')[2].strip()
                    service = x.split('|')[3].strip()
                    zone = x.split('|')[5].strip()
                    query = "('" + hostname + "','" + service + "','" + zone + "','" + entity_type + "',STR_TO_DATE('" + dttime + "','%Y%m%d%H%i'),'" + circle + "'),"
                    query2 = query2 + query

            query_final = query1 + " " + query2
            query_final = delete_data + " " + query_final[0:len(query_final) - 1]
            print(query_final)
            # exit()
            try:
                cnx = dbstring
                print('connected to localhost')
                cursor = cnx.cursor()
                for _ in cursor.execute(query_final, multi=True): pass
                cnx.commit()
                cursor.close()
               # cnx.close()
                print("successfully executed")
            except NameError as ex:
                print(ex)


            del data[:]
