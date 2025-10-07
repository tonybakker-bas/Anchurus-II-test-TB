from ._anvil_designer import SelectSiteTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import Global

class SelectSite(SelectSiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens
    if anvil.users.get_user() is not None:
      sites_list = anvil.server.call('sites_get_summary')
      Global.site_options = {}
      for x in sites_list:
        val_list = list(x.values())
        option = val_list[0] + " - " + val_list[1]
        Global.site_options[option] = val_list[0]
    else:
        print("in Select Site form without having logged in")
    self.select_site.items = Global.site_options.keys()

  def submit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.select_site.selected_value is not None:
      Global.site_name = self.select_site.selected_value
      Global.site_id = Global.site_options[self.select_site.selected_value]
      Global.selected_site = ": " + Global.site_name
      #Global.title_label.text = Global.title + Global.status + Global.selected_site
      Global.title_label.text = Global.title
      #get more details of sites, e.g. How many areas, contexts, finds 
      site_information = anvil.server.call("site_get_information",Global.site_id)
      Global.header_site_name.text = Global.site_name
      Global.header_site_summary_information.text = "# of Contexts: " + str(site_information["Contexts"]) + ", # of Finds:" + str(site_information["Finds"])
      
    pass

