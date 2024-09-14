from aws_cdk import (
    Stack,
    aws_ec2 as ec2,  # Para EC2 y Security Groups
    DefaultStackSynthesizer,
    CfnOutput,       # Para las salidas
    aws_iam as iam,  # Importar IAM para usar IRole
)
from constructs import Construct

class CdkPythonStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        # Definir el sintetizador personalizado
        synthesizer = DefaultStackSynthesizer(
            file_assets_bucket_name="cf-templates-1k0oguavt109r-us-east-1",  # Nombre del bucket S3 para los archivos de activos
            deploy_role_arn="arn:aws:iam::239245338181:role/LabRole",  # Rol de IAM que se usará para desplegar
            cloud_formation_execution_role= "arn:aws:iam::239245338181:role/LabRole",
            file_asset_publishing_role_arn="arn:aws:iam::239245338181:role/LabRole",
            deploy_role_external_id="arn:aws:iam::239245338181:role/LabRole",
            image_asset_publishing_role_arn="arn:aws:iam::239245338181:role/LabRole",
        )
        
        # Llamar al constructor de Stack y pasar el sintetizador
        super().__init__(scope, construct_id, synthesizer=synthesizer, **kwargs)

        # VPC
        existing_vpc = ec2.Vpc.from_vpc_attributes(
            self, 'ExistingVPC',
            vpc_id='vpc-0d6ed0ab35089f55a',
            availability_zones=['us-east-1a', 'us-east-1c'],
            public_subnet_ids=['subnet-068e54de0032f5a1f', 'subnet-0056d79a26a2b99cc']
        )

        # Security Group
        security_group1 = ec2.SecurityGroup.from_security_group_id(
            self, 'SG1', 'sg-0f6b89062a9d16e2c'
        )

        # instancia EC2
        instance = ec2.Instance(
            self,
            "cdkPython", # Nombre de la instancia
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.generic_linux({
                "us-east-1": "ami-0aa28dab1f2852040"
            }),
            vpc=existing_vpc,
            security_group=security_group1,
            associate_public_ip_address=True,
            key_name="vockey",
            role=iam.Role.from_role_arn(self, "Role", "arn:aws:iam::239245338181:role/LabRole"),
        )

        instance.add_user_data(
            "git clone https://github.com/RodrigoLiC/webplantilla.git",  # Clonar el primer repositorio
            "git clone https://github.com/RodrigoLiC/websimple.git",  # Clonar el segundo repositorio
        )
    
        CfnOutput(self, "InstanceId", value=instance.instance_id, description="ID de la instancia EC2")
        CfnOutput(self, "InstancePublicIP", value=instance.instance_public_ip, description="IP pública de la instancia")
        
