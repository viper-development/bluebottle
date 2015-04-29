from decimal import Decimal
from datetime import timedelta
from bluebottle.bb_projects.models import ProjectPhase
from bluebottle.utils.model_dispatcher import get_project_payout_model
from bluebottle.utils.utils import StatusDefinition

from django.utils import timezone


def _set_properties():
    # If this signal is being triggered from a cron job then 
    # the tenant properties will not be loaded. Check below
    # and setup the tenant properties if required.
    from bluebottle.clients import properties
    from django.db import connection
    
    try:
        tenant = properties.tenant 
    except AttributeError:
        tenant = connection.tenant
        properties.set_tenant(tenant)


def create_payout_finished_project(sender, instance, created, **kwargs):
    """
    Create or update Payout for finished projects.
    Project finish when deadline is hit or when it's changed manually in admin.
    """

    project = instance
    now = timezone.now()

    if (project.is_realised or project.is_closed) and project.amount_asked:

        if now.day <= 15:
            next_date = timezone.datetime(now.year, now.month, 15)
        else:
            next_date = timezone.datetime(now.year, now.month, 1) + timedelta(days=20)

        PROJECT_PAYOUT_MODEL = get_project_payout_model()

        try:
            # Update existing Payout
            payout = PROJECT_PAYOUT_MODEL.objects.get(project=project)

            if payout.status == StatusDefinition.NEW:
                _set_properties()

                # Update planned payout date for new Payouts
                payout.calculate_amounts()
                payout.planned = next_date
                payout.save()

        except PROJECT_PAYOUT_MODEL.DoesNotExist:

            if project.campaign_started:
                _set_properties()

                # Create new Payout
                payout = PROJECT_PAYOUT_MODEL(
                    planned=next_date,
                    project=project
                )

                # Calculate amounts
                payout.calculate_amounts()

                if project.is_closed:
                    payout.status = StatusDefinition.SETTLED

                payout.save()

                # Set payment details
                payout.receiver_account_bic = project.account_bic
                payout.receiver_account_iban = project.account_number
                payout.receiver_account_number = project.account_number
                payout.receiver_account_name = project.account_holder_name
                payout.receiver_account_city = project.account_holder_city
                payout.receiver_account_country = project.account_bank_country

                # Generate invoice reference, saves twice
                payout.update_invoice_reference(auto_save=True)
