from cloudmesh_base.Shell import Shell
import subprocess
import yaml


class command_apachestorm(object):

    @classmethod
    def status(cls, host):
        msg = "Unknown host"
        try:
            msg = Shell.ping("-c", "1", host)
        except:
            pass
        if "1 packets transmitted, 1 packets received" in msg:
            return True
        elif "Unknown host" in msg:
            return False
        else:
            return False
    
    @classmethod
    def start(cls, alive_time):
        try:
            #pip.main(['install', packageName])
            print "start"
            setStormClusterAliveTime(alive_time)
            return_code = subprocess.call("ansible-playbook -i inventory.txt -c ssh storm_start.yaml", shell=True)
        except:
            pass

    @classmethod
    def stop(cls):
        try:
            #pip.main(['install', packageName])
	    print "stopping storm "
            return_code = subprocess.call("ansible-playbook -i inventory.txt -c ssh storm_stop.yaml", shell=True)
        except:
            pass

    @classmethod
    def deploy(cls, nimbusNode, zookeeperNode, supervisorNodes):
        try:
            print "deploy"
            createInventoryFile(nimbusNode,zookeeperNode, supervisorNodes)
            createStormYamlFile(nimbusNode, zookeeperNode)
            return_code = subprocess.call("ansible-playbook -i inventory.txt -c ssh storm_deploy.yaml", shell=True)
        except:
            pass

def createInventoryFile(nimbusNode, zookeeperNode, supervisorNodes):
    print "creating inventory file"
    file_inventory = open("inventory.txt", "w")
    file_inventory.write("[zookeeper]\n")
    file_inventory.write(zookeeperNode+"\n")
    file_inventory.write("[nimbus]\n")
    file_inventory.write(nimbusNode+"\n")
    file_inventory.write("[supervisor]\n")
    file_inventory.write('\n'.join(supervisorNodes))
    file_inventory.close()

def createStormYamlFile(nimbusNode, zookeeperNode):
    print "create storm.yaml file"
    file1 = open("storm.yaml")
    dataMap = yaml.safe_load(file1)
    dataMap["storm.zookeeper.servers"] = [zookeeperNode]
    dataMap["nimbus.host"] = nimbusNode    
    file1.close()
    file2 = open("storm.yaml", "w")
    yaml.dump(dataMap, file2)
    file2.close()

def setStormClusterAliveTime(set_alive_time):
    print "modifying the alive time"
    file1 = open("storm_start.yaml")
    dataMap = yaml.safe_load(file1)
    for data in dataMap:
        for data2 in data["tasks"]:
            if data2.has_key("async"):
                data2["async"] = set_alive_time
