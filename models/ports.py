"""
ports
"""
import models


class Ports:
    """
    for storing ports details
    """
    name = "ports"
    @classmethod
    def get_a_port(cls, rep=0):
        """
        get a single free port from database
        """
        if rep == 3:
            return None
        port = models.storage.findOne(cls, {"available": True})
        if port:
            port = port["port"]
        else:
            from util.getport import main
            main()
            return cls.get_a_port(rep+1)
        models.storage.update(cls, {"port": port}, {"available": False})
        return port

    @classmethod
    def load_available_ports(cls, port_list):
        """
        add available ports to the database
        """
        documents = [{"port": p, "available": True, "broject_id": "0"} for p in port_list]
        # considering the 1000 insertion limit
        for i in range(0, len(documents),  900):
            models.storage.newMany(cls, documents[i: i + 900])
        return

    @classmethod
    def update_port_status(cls):
        """
        """
        return
