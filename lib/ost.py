import os_client_config


class OST:
    """OST: Class wrapper for openstack nova client calls"""
    nova_api = None

    def __init__(self, version, username, password, project_name, auth_url, insecure=False):

        self.nova_api = os_client_config.make_client('compute',
                                                     version=version,
                                                     username=username,
                                                     password=password,
                                                     project_name=project_name,
                                                     auth_url=auth_url,
                                                     insecure=str(insecure))

    def get_servers(self, only_status=None):
        """return: generator of server objects.
        only_state: limits generator results to a state"""
        for server in self.nova_api.servers.list():
            if only_status is not None:
                if server.status == only_status:
                    yield server
            else:
                yield server

    def get_instance_names_string(self, only_status=None):
        """Return string output of instance names"""
        output = ""
        for server in self.get_servers(only_status):
            output += "%s\n"% server.name
        return output.strip()

    def get_instances_with_states_string(self, only_status=None):
        output = ""
        for server in self.get_servers(only_status):
            output += "%s %s" % (server.name, server.status)
        return output.strip()

    def poweron_server_by_name(self, name):
        """Return: Bool
        True: successfully found server and made attempt.
        Hint: no guaranteed that it actually worked.  Sorry in a rush here."""
        server_obj = None
        for server in self.get_servers():
            if name == server.name:
                server_obj = self.nova_api.servers.get(server.id)
        if server_obj is not None:
            server_obj.start()
            return True
        else:
            return False

    def shutdown_server_by_name(self, name):
        """Return: Bool
        True: successfully found server and made attempt.
        Hint: no guaranteed that it actually worked.  Sorry in a rush here."""
        server_obj = None
        for server in self.get_servers():
            if name == server.name:
                server_obj = self.nova_api.servers.get(server.id)
        if server_obj is not None:
            server_obj.stop()
            return True
        else:
            return False

    def reboot_server_by_name(self, name):
        """Return: Bool
        True: successfully found server and made attempt.
        Hint: no guaranteed that it actually worked.  Sorry in a rush here."""
        server_obj = None
        for server in self.get_servers():
            if name == server.name:
                server_obj = self.nova_api.servers.get(server.id)
        if server_obj is not None:
            server_obj.reboot()
            return True
        else:
            return False

