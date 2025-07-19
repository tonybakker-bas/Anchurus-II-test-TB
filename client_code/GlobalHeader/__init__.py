from ._anvil_designer import GlobalHeaderTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.media
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import Global
from .. import Function
from ..ListContexts import ListContexts
from ..ListFinds import ListFinds
from ..ListAreas import ListAreas
from ..ListSites import ListSites
from ..ListUsers import ListUsers
from ..BulkUpload import BulkUpload

class GlobalHeader(GlobalHeaderTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.







