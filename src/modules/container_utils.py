from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (ResourceRequests,
                                                 ResourceRequirements,
                                                 Container,
                                                 ContainerPort,
                                                 Port,
                                                 IpAddress,
                                                 ContainerGroupNetworkProtocol,
                                                 OperatingSystemTypes,
                                                 ContainerGroup)
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import ResourceGroup


def create_new_container_group(aci_client=None, reg_client=None, reg_name=None,
                               con_group_name=None, con_group_image=None):
    try:
        res_request = ResourceRequests(memory_in_gb=2, cpu=1.0)
        res_requirement = ResourceRequirements(requests=res_request)
        res_group_obj = reg_client.resource_groups.get(reg_name)
        container_1 = Container(
            name=con_group_name,
            image="microsoft\aci-helloworld:latest",
            resources=res_requirement,
            ports=[ContainerPort(port=80)]
        )
        ports = [Port(protocol=ContainerGroupNetworkProtocol.tcp, port=80)]
        group_ip_address = IpAddress(
            ports=ports,
            dns_name_label=con_group_name,
            type="Public")

        group = ContainerGroup(
            location=res_group_obj.location,
            containers=[container_1],
            os_type=OperatingSystemTypes.linux,
            ip_address=group_ip_address)
        aci_client.container_groups.begin_create_or_update(res_group_obj.name,
                                                           con_group_name,
                                                           group)

    except Exception as err:
        print(err)
