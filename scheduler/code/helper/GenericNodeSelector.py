import logging
###
#Generic Class
###
class GenericNodeSelector:
    def __init__(self):
        pass

    ##
    #Takes a Node Dictionary of key: NodeName val: ip
    #Then will select the first node in the dictionary and return the node name
    ##
    def node_selection(self,nodeList: dict) -> str:
        if len(nodeList.values()) == 0:
            pass
        else:
            ##
            #Just select the first node off the list
            ##
            return list(nodeList.values())[0]
