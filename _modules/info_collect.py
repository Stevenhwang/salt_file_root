# -*- coding: utf-8 -*-
'''
Module for save node specified information to mysql
'''
import sys
import MySQLdb
import datetime
import os

reload(sys)
sys.setdefaultencoding('utf-8')


def process():
    __salt__['saltutil.refresh_pillar']
    mysql_host = __pillar__['mysql_host']
    mysql_user = __pillar__['mysql_user']
    mysql_passwd = __pillar__['mysql_passwd']
    mysql_db = __pillar__['mysql_db']
    mysql_port = __pillar__['mysql_port']

    cpu_info = __grains__['cpu_model']
    cpu_model = cpu_info.split(' @ ')[0]
    cpu_mhz = cpu_info.split(' @ ')[1]

    mac_info = __grains__['hwaddr_interfaces']
    del mac_info['lo']
    mac_list = []
    for k in mac_info.keys():
        mac_list.append(k + ' ' + mac_info[k])
    mac = '; '.join(mac_list)

    disk_info = os.popen(
        "lsblk -l | grep disk | awk '{print $1,$4}'").readlines()
    disk_info = [x.strip('\n') for x in disk_info]
    disk = '; '.join(disk_info)

    outerip_info = os.popen('curl ipecho.net/plain').readlines()
    outerip = '; '.join(outerip_info)

    innerip_info = __grains__['ipv4']
    if '127.0.0.1' in innerip_info:
        innerip_info.remove('127.0.0.1')
    innerip = '; '.join(innerip_info) if isinstance(
        innerip_info, list) else innerip_info

    now = datetime.datetime.utcnow()

    db = MySQLdb.connect(host=mysql_host, user=mysql_user,
                         passwd=mysql_passwd, db=mysql_db, port=mysql_port)
    c = db.cursor()

    query_sql = "SELECT * from `Common_node` WHERE name='%s'" % (__grains__[
                                                                 'id'])
    if c.execute(query_sql) == 0:
        sql = '''INSERT INTO `Common_node`
                     (`create_time`, `update_time`, `name`, `remark`, `innerip`, `outerip`, `operator`, `bak_operator`,
                     `state_name`, `province_name`, `isp_name`, `os_type`, `os_name`, `os_version`, `os_bit`, `cpu`, 
                     `cpu_mhz`, `cpu_module`, `mem`, `disk`, `mac`, `import_from`, `clond_id`)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        uu = (now,
              now,
              __grains__['id'],
              None,
              innerip,
              str(outerip),
              None,
              None,
              None,
              None,
              None,
              str(__grains__['kernel']),
              str(__grains__['oscodename']),
              str(__grains__['osrelease']),
              str(__grains__['osarch']),
              str(__grains__['num_cpus']),
              str(cpu_mhz),
              str(cpu_model),
              str(__grains__['mem_total']) + 'M',
              str(disk),
              str(mac),
              0,
              1)
        c.execute(sql, uu)
        c.execute("COMMIT")
        db.close()
        return 'Success'
    else:
        sql = """UPDATE `Common_node` SET `update_time`='%s', `innerip`='%s', `outerip`='%s', `os_type`='%s', `os_name`='%s',
                `os_version`='%s', `os_bit`='%s', `cpu`='%s', `cpu_mhz`='%s', `cpu_module`='%s', `mem`='%s', `disk`='%s',
                `mac`='%s' WHERE name='%s'""" % (
            now,
            innerip,
            str(outerip),
            str(__grains__['kernel']),
            str(__grains__['oscodename']),
            str(__grains__['osrelease']),
            str(__grains__['osarch']),
            str(__grains__['num_cpus']),
            str(cpu_mhz),
            str(cpu_model),
            str(__grains__['mem_total']) + 'M',
            str(disk),
            str(mac),
            __grains__['id'])
        c.execute(sql)
        c.execute("COMMIT")
        db.close()
        return 'Success'
