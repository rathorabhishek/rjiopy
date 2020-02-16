import mysql.connector
import os

from multiprocessing import Process

cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='cms')
import time
filex = 'C:\\mylog\\cms\\raw\\'
import openstack_service
import nova_list_vm_cnt
import nova_host_list
import nova_hypervisor
import storage_cinder_list
import process

if __name__=='__main__':
    openstack_service_call = openstack_service.openstack()
    nova_list_vm_cnt_call = nova_list_vm_cnt.nov_list_vm_cnt()
    nova_host_list_call = nova_host_list.nova_host_list()
    nova_hypervisor_call = nova_hypervisor.nova_hypervisor()
    storage_cinder_list_call = storage_cinder_list.stroage_cinder_list_c()
    # gettting all folder inside
    cir=os.listdir(filex)
    for x in cir:

        if not x.__contains__('_OSC'):
            print(filex+'\\'+x+'\\')
            openstack_service_call.openstack_service(filex+'\\'+x+'\\', cnx)

    #openstack_service_call.openstack_service(filex, cnx)
    #p1 = Process(target=openstack_service_call.openstack_service(filex, cnx))
    #p1.start()
    #p2 = Process(target=nova_list_vm_cnt_call.nova_list_vm_cnt(filex, cnx))
    #p2.start()
    #p3 = Process(target= nova_host_list_call.nova_host_list_m(filex, cnx))
    #p3.start()
    #p4 = Process(target=nova_hypervisor_call.nova_hypervisor_m(filex, cnx))
    #p4.start()
    #p5 = Process(target=storage_cinder_list_call.storage_cinder_list_m(filex, cnx))
    #p5.start()
    #p1.join()
    #p2.join()
    #p3.join()
    #p4.join()
    #p5.join()

    #process_call = process.process_c()
    #process_call.process_m(filex, 'redis', '--redis status start--', '--redis status finish--', cnx)
    #time.sleep(2)
    #process_call.process_m(filex, 'mongodb', '--mongod status start--', '--mongod status finish--', cnx)
    #time.sleep(2)
    #process_call.process_m(filex, 'rabbitmq', '--rabbitmq-server status start--', '--rabbitmq-server status finish--',
    #                       cnx)
    #time.sleep(2)
    #process_call.process_m(filex, 'ntpd', '--ntpd status start--', '--ntpd status finish--', cnx)
    #time.sleep(2)
    #process_call.process_m(filex, 'httpd', '--httpd status start--', '--httpd status finish--', cnx)

    try:
        cnx.close()
        print ("connection succesfully closed")
    except NameError as ex:
        print(ex)

        # cms_call.storage_cinder_list(filex)
        # time.sleep(2)
        # cms_call.process(filex,'redis','--redis status start--','--redis status finish--')
        # time.sleep(2)
        # cms_call.process(filex,'mongodb','--mongod status start--','--mongod status finish--')
        # time.sleep()
        # cms_call.process(filex,'rabbitmq','--rabbitmq-server status start--', '--rabbitmq-server status finish--')
        # time.sleep()
        # cms_call.process(filex,'rabbitmq','ntpd','--ntpd status start--', '--ntpd status finish--')
        # time.sleep(2)
        # cms_call.process(filex,'rabbitmq','httpd','--httpd status start--', '--httpd status finish--')




