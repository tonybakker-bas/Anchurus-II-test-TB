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
    Global.header_site_name = self.site_name
    Global.header_site_summary_information = self.more_information
    Global.gh_file_list = self.File
    Global.gh_view_list = self.View
    Global.gh_list_list = self.List
    Global.gh_insert_list = self.Insert
    Global.gh_admin_list = self.Admin
    Global.gh_admin_list.visible = False

    if anvil.users.get_user() is not None:
      sites_list = anvil.server.call('sites_get_summary')
      Global.site_options = {}
      for x in sites_list:
        val_list = list(x.values())
        option = val_list[0] + " - " + val_list[1]
        Global.site_options[option] = val_list[0]
    else:
      print("in SelectSite form without having logged in")
      
    self.select_site.items = Global.site_options.keys()




