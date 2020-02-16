import cms
import glob
import mysql.connector

cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='cms')


class cms_healthcheck_class:
    def nova_host_list(self, filename):
        # filex = 'C:\\mylog\\cms\\raw\\20190528\\'
        filex_nova_host_list = filename
        file = glob.glob(filex_nova_host_list + "*.txt")
        for filename in file:

            filtername = filename.replace(filex_nova_host_list, "")
            circle = str(filtername.split('_')[0])
            entity_type = filtername.split('_')[1]
            dttime = filtername.split('_')[2].replace('.txt', '')

            cms_call = cms.test()
            data = cms_call.data_pars(filename, '--nova host-list-start--', '--nova host-list-finish---')

            query1 = "insert into cms.nova_host_list(hostname, service, zone, entity_name, dttime, circle) values"
            # query2 = ""
            for x_nova_host_list in data:
                if not x_nova_host_list.__contains__('----') and not x_nova_host_list.__contains__('osc') and not x_nova_host_list.__contains__(
                        'OSC') and not x_nova_host_list.__contains__(
                    'host_name'):
                    # print(x.strip())
                    hostname = x_nova_host_list.split('|')[1].strip()
                    service = x_nova_host_list.split('|')[2].strip()
                    zone = x_nova_host_list.split('|')[3].strip()
                    query = "('" + hostname + "','" + service + "','" + zone + "','" + entity_type + "',STR_TO_DATE('" + dttime + "','%Y%m%d%H%i'),'" + circle + "'),"
                    # query2 = query2 + query

            query_final = query1 + " " + query
            query_final = query_final[0:len(query_final) - 1]
            print(query_final)
            try:
                # cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='cms')
                # print('connected to localhost')
                cursor = cnx.cursor()
                cursor.execute(query_final)
                cnx.commit()
                cursor.close()
                # cnx.close()
                print("nova host list successfully executed")
            except NameError as ex:
                print(ex)

    def nova_hypervisor(self, filename):
        # filex = 'C:\\mylog\\cms\\raw\\20190528\\'
        filex = filename
        file = glob.glob(filex + "*.txt")
        for filename in file:

            filtername = filename.replace(filex, "")

            circle = str(filtername.split('_')[0])
            entity_type = filtername.split('_')[1]
            dttime = filtername.split('_')[2].replace('.txt', '')

            cms_call = cms.test()
            data = cms_call.data_pars(filename, '-nova hypervisor-list-start-', '-nova hyporvisor-list-finish-')

            query1 = "insert into cms.hypervisor_list(hypervs_hostname, state, status, entity_name, dttime, circle) values"
            # query2 = ""
            for x in data:
                if not x.__contains__('----') and not x.__contains__('osc') and not x.__contains__(
                        'OSC') and not x.__contains__(
                    'host_name'):
                    print(x.strip())
                    hostname = x.split('|')[2].strip()
                    service = x.split('|')[3].strip()
                    zone = x.split('|')[4].strip()
                    query = "('" + hostname + "','" + service + "','" + zone + "','" + entity_type + "',STR_TO_DATE('" + dttime + "','%Y%m%d%H%i'),'" + circle + "'),"
                    # query2 = query2 + query

            query_final = query1 + " " + query
            query_final = query_final[0:len(query_final) - 1]
            print(query_final)
            # exit()
            try:
                # cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='cms')
                # print('connected to localhost')
                cursor = cnx.cursor()
                cursor.execute(query_final)
                cnx.commit()
                cursor.close()
                # cnx.close()
                print(" nova_hypervisor successfully executed")
            except NameError as ex:
                print(ex)


    def nova_list_vm_cnt(self, filename):
        # filex = 'C:\\mylog\\cms\\raw\\20190528\\'
        #print("enter in nova list vm count ")
        filex = filename
        file = glob.glob(filex + "*.txt")
        for filename in file:

            filtername = filename.replace(filex, "")

            circle = str(filtername.split('_')[0])
            entity_type = filtername.split('_')[1]
            dttime = filtername.split('_')[2].replace('.txt', '')

            cms_call = cms.test()
            data_vm_cnt = cms_call.data_pars(filename, '--nova list-start--', '-nova list-finish-')
            print(data_vm_cnt)

            query1 = "insert into cms.nova_list_vm_cnt(vm_name, status, power_state, entity_name, dttime, circle) values"
            # query2 = ""
            for x_vm_cnt in data_vm_cnt:
                if not x_vm_cnt.__contains__('----') and not x_vm_cnt.__contains__('osc') and not x_vm_cnt.__contains__(
                        'OSC') and not x_vm_cnt.__contains__(
                    'host_name'):
                    #print(x_vm_cnt.strip())
                    #print(x_vm_cnt)
                    hostname = x_vm_cnt.split('|')[2].strip()
                    service = x_vm_cnt.split('|')[3].strip()
                    zone = x_vm_cnt.split('|')[5].strip()
                    query = "('" + hostname + "','" + service + "','" + zone + "','" + entity_type + "',STR_TO_DATE('" + dttime + "','%Y%m%d%H%i'),'" + circle + "'),"
                    # query2 = query2 + query

            query_final = query1 + " " + query
            query_final = query_final[0:len(query_final) - 1]
            print(query_final)
            # exit()
            try:
                # cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='cms')
                # print('connected to localhost')
                cursor = cnx.cursor()
                cursor.execute(query_final)
                cnx.commit()
                cursor.close()
                # cnx.close()
                print(" nova_list_vm_cnt successfully executed")
            except NameError as ex:
                print(ex)

    def openstack_service(self, filename):
        # filex = 'C:\\mylog\\cms\\raw\\20190528\\'
        filex = filename
        file = glob.glob(filex + "*.txt")
        for filename in file:
            filtername = filename.replace(filex, "")
            circle = str(filtername.split('_')[0])
            entity_type = filtername.split('_')[1]
            dttime = filtername.split('_')[2].replace('.txt', '')
            cms_call = cms.test()
            data_openstack = cms_call.data_pars(filename, '--Openstack service status-start--',
                                      '--Openstack service status-finish--')
            query1 = "insert into cms.open_stack_service(servicename, status, entity_name, dttime, circle) values"
            # query2 = ""
            for x_openstack in data_openstack:
                if not x_openstack.__contains__('----') and not x_openstack.__contains__('osc') and not x_openstack.__contains__(
                        'OSC') and not x_openstack.__contains__(
                    'host_name'):
                    #print(x.strip())
                    service = x_openstack.split('=')[2].replace('.service ActiveState', '').strip()
                    status = x_openstack.split('=')[3].strip()
                    # zone = x.split('|')[5].strip()
                    query = "('" + service + "','" + status + "','" + entity_type + "',STR_TO_DATE('" + dttime + "','%Y%m%d%H%i'),'" + circle + "'),"
                    # query2 = query2 + query

            query_final = query1 + " " + query
            query_final = query_final[0:len(query_final) - 1]
            print(query_final)
            # exit()
            try:
                # cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='cms')
                # print('connected to localhost')
                cursor = cnx.cursor()
                cursor.execute(query_final)
                cnx.commit()
                cursor.close()
                # cnx.close()
                print("openstack_service successfully executed")
            except NameError as ex:
                print(ex)

        del data_openstack[:]

    def storage_cinder_list(self, filename):

        # filex = 'C:\\mylog\\cms\\raw\\20190528\\'
        filex = filename
        file = glob.glob(filex + "*.txt")
        for filename in file:

            filtername = filename.replace(filex, "")

            circle = str(filtername.split('_')[0])
            entity_type = filtername.split('_')[1]
            dttime = filtername.split('_')[2].replace('.txt', '')

            cms_call = cms.test()
            data = cms_call.data_pars(filename, '--cinder service-list-start--', '--cinder service-list-finish--')

            query1 = "insert into cms.storage_cinder_list(`binary`, host, zone, `status`, state, entity_name, dttime, circle) values"
            # query2 = ""
            for x in data:
                if not x.__contains__('----') and not x.__contains__('Host'):
                    # print(x.strip())
                    binary = x.split('|')[1].strip()
                    host = x.split('|')[2].strip()
                    zone = x.split('|')[3].strip()
                    status = x.split('|')[4].strip()
                    state = x.split('|')[5].strip()
                    query = "('" + binary + "','" + host + "','" + zone + "','" + status + "','" + state + "','" + entity_type + "',STR_TO_DATE('" + dttime + "','%Y%m%d%H%i'),'" + circle + "'),"
                    # query2 = query2 + query

            query_final = query1 + " " + query
            query_final = query_final[0:len(query_final) - 1]
            print(query_final)
            # exit()
            try:
                # cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='cms')
                # print(' connected to localhost')
                cursor = cnx.cursor()
                cursor.execute(query_final)
                cnx.commit()
                cursor.close()
                # cnx.close()
                print("storage_cinder_list successfully executed")
            except NameError as ex:
                print(ex)

    def process(self, filen, process, start_split, end_split):
        filename = glob.glob(filen + "*.txt")
        z = filename[0]

        filtername = z.strip().replace(filen, '')

        circle = str(filtername.split('_')[0])
        entity_type = filtername.split('_')[1]
        dttime = filtername.split('_')[2].replace('.txt', '')

        cms_call = cms.test()
        data = cms_call.data_pars(filename[0], start_split, end_split)

        query1 = "insert into cms.process_list(`process`,`status`, entity_name, dttime, circle) values"

        query = ""
        for x in data:
            if x.__contains__('Active:'):
                # print(x.strip())
                binary = x.split(':')[0].strip()
                status = x.split(':')[1].replace('[1;32m', '').replace('[0m', '').strip()

                query = "('" + process + "','" + status + "','" + entity_type + "',STR_TO_DATE('" + dttime + "','%Y%m%d%H%i'),'" + circle + "'),"

        query_final = query1 + " " + query
        query_final = query_final[0:len(query_final) - 1]
        print(query_final)

        try:
            # cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='cms')
            # print('connected to localhost')
            cursor = cnx.cursor()
            cursor.execute(query_final)
            cnx.commit()
            cursor.close()
            # cnx.close()
            print("process successfully executed")
        except NameError as ex:
            print(ex)

# cnx.close()
