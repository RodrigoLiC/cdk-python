from aws_cdk import (
    Stack,
    aws_ec2 as ec2,  # Para EC2 y Security Groups
    CfnOutput,       # Para las salidas
)
from constructs import Construct

class CdkPythonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Parámetros (nombre de instancia y AMI ID)
        instance_name = "MV Reemplazar"  # Nombre por defecto de la instancia
        ami_id = "ami-0aa28dab1f2852040"  # AMI ID especificada
        
        # Crear un Security Group
        security_group = ec2.SecurityGroup(self, "InstanceSecurityGroup",
            vpc=ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True),  # Usar la VPC por defecto
            description="Permitir tráfico SSH, HTTP y en el puerto 8000 desde cualquier lugar",
            allow_all_outbound=True
        )
        
        # Agregar reglas de ingreso al Security Group
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Permitir SSH desde cualquier lugar"
        )
        
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Permitir HTTP desde cualquier lugar"
        )

        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(8000),
            description="Permitir tráfico en el puerto 8000 desde cualquier lugar"
        )

        # Crear una instancia EC2
        ec2_instance = ec2.Instance(self, "EC2Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.generic_linux({
                "us-east-1": ami_id  # Especificar la AMI en la región
            }),
            vpc=ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True),
            key_name="vockey",  # El nombre del par de claves
            security_group=security_group,
            block_devices=[ec2.BlockDevice(
                device_name="/dev/sda1",
                volume=ec2.BlockDeviceVolume.ebs(20)  # Tamaño del volumen en GB
            )],
        )

        # Salidas
        CfnOutput(self, "InstanceId", value=ec2_instance.instance_id, description="ID de la instancia EC2")
        CfnOutput(self, "InstancePublicIP", value=ec2_instance.instance_public_ip, description="IP pública de la instancia")
