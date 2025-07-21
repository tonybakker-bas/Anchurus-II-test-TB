from ._anvil_designer import SelectSystemTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import Global


class SelectSystem(SelectSystemTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens
    if anvil.users.get_user() is not None:
      systems_list = anvil.server.call("systems_get_summary")
      Global.site_options = {}
      for x in sites_list:
        val_list = list(x.values())
        option = val_list[0] + " - " + val_list[1]
        Global.site_options[option] = val_list[0]
    else:
      print("in SelectSystem form without having logged in")
    self.select_system.items = Global.site_options.keys()

  def submit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.select_system.selected_value is not None:
      Global.system_name = self.select_site.selected_value
      Global.title_label.text = Global.title + Global.status + Global.selected_site
      # get more details of sites, e.g. How many areas, contexts, finds
      site_information = anvil.server.call("site_get_information", Global.site_id)
      self.site_summary.text = (
        "Site summary for "
        + Global.site_id
        + ": #Contexts: "
        + str(site_information["Contexts"])
        + ", Finds:"
        + str(site_information["Finds"])
      )
    pass


