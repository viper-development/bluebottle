from django.urls.base import reverse
from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import DefaultAppIndexDashboard
from jet.dashboard.modules import DashboardModule

from bluebottle.funding.models import Funding, Payout


class RecentFunding(DashboardModule):
    title = _('Recently submitted funding activities')
    title_url = "{}?status[]=draft&status[]=open".format(reverse('admin:funding_funding_changelist'))
    template = 'dashboard/recent_funding.html'
    limit = 5
    column = 0

    def init_with_context(self, context):
        activities = Funding.objects.filter(status__in=['draft', 'open']).order_by('-created')
        self.children = activities[:self.limit]


class PayoutsReadForApprovalDashboardModule(DashboardModule):
    title = _('Payouts ready for approval')
    title_url = "{}?status[]=draft&status[]=new".format(reverse('admin:funding_payout_changelist'))
    template = 'dashboard/payouts_ready_for_approval.html'
    limit = 5
    column = 0

    def init_with_context(self, context):
        payouts = Payout.objects.filter(status='new').order_by('created')
        self.children = payouts[:self.limit]


class AppIndexDashboard(DefaultAppIndexDashboard):

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.children.append(RecentFunding())
        self.children.append(PayoutsReadForApprovalDashboardModule())