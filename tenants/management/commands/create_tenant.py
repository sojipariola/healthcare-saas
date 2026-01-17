"""
Management command to create a new tenant
"""
from django.core.management.base import BaseCommand
from tenants.models import Tenant, Domain


class Command(BaseCommand):
    help = 'Create a new tenant for the healthcare SaaS platform'

    def add_arguments(self, parser):
        parser.add_argument('--schema_name', type=str, required=True,
                          help='Schema name (e.g., clinic1)')
        parser.add_argument('--name', type=str, required=True,
                          help='Organization name (e.g., Main Street Clinic)')
        parser.add_argument('--domain', type=str, required=True,
                          help='Domain name (e.g., clinic1.example.com)')
        parser.add_argument('--organization_type', type=str, default='clinic',
                          choices=['hospital', 'clinic', 'private_practice', 'laboratory', 'pharmacy'],
                          help='Type of healthcare organization')

    def handle(self, *args, **options):
        schema_name = options['schema_name']
        name = options['name']
        domain_name = options['domain']
        org_type = options['organization_type']

        # Create tenant
        try:
            tenant = Tenant.objects.create(
                schema_name=schema_name,
                name=name,
                organization_type=org_type,
                hipaa_compliance_enabled=True,
                gdpr_compliance_enabled=True,
                is_active=True
            )

            # Create domain
            domain = Domain.objects.create(
                domain=domain_name,
                tenant=tenant,
                is_primary=True
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created tenant: {name} (schema: {schema_name})'
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Domain: {domain_name}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating tenant: {str(e)}')
            )
