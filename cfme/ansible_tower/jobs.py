import attr

from navmazing import NavigateToAttribute
from widgetastic.widget import Text, View
from widgetastic_patternfly import Accordion, BootstrapNav, Dropdown
from widgetastic_manageiq import ManageIQTree, Search, ItemsToolBarViewSelector

from cfme.base.login import BaseLoggedInPage
from cfme.modeling.base import BaseEntity, BaseCollection
from cfme.utils.appliance.implementations.ui import navigator, CFMENavigateStep


class TowerJobsToolbar(View):
    configuration = Dropdown('Configuration')
    policy = Dropdown('Policy')
    download = Dropdown('Download')
    view_selector = View.nested(ItemsToolBarViewSelector)


class TowerJobsView(BaseLoggedInPage):
    search = View.nested(Search)
    toolbar = View.nested(TowerJobsToolbar)

    @property
    def in_jobs(self):
        return (self.logged_in_as_current_user and
                self.navigation.currently_selected == ['Automation', 'Ansible Tower', 'Jobs'])

    @View.nested
    class my_filters(Accordion):  # noqa
        ACCORDION_NAME = "My Filters"

        navigation = BootstrapNav('.//div/ul')
        tree = ManageIQTree()


class TowerJobsDefaultView(TowerJobsView):
    title = Text('//div[@id="main-content"]//h1')

    @property
    def is_displayed(self):
        return (
            self.in_jobs and
            self.title.text == 'Ansible Tower Jobs'
        )


@attr.s
class TowerJobs(BaseEntity):
    pass


@attr.s
class TowerJobsCollection(BaseCollection):
    ENTITY = TowerJobs


@navigator.register(TowerJobsCollection, 'All')
class All(CFMENavigateStep):
    VIEW = TowerJobsDefaultView
    prerequisite = NavigateToAttribute('appliance.server', 'LoggedIn')

    def step(self, *args, **kwargs):
        self.prerequisite_view.navigation.select('Automation', 'Ansible Tower', 'Jobs')
