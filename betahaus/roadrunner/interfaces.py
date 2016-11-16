from arche.interfaces import IBase
from arche.interfaces import IContent


class IOrganisation(IContent):
    pass


class ICustomer(IContent):
    pass


class IProject(IContent):
    pass


class ITask(IContent):
    pass


class ITimeEntry(IBase):
    pass


class ITariff(IBase):
    pass
