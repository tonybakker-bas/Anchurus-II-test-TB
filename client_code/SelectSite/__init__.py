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
        print("in SelectSite form without having logged in")
    self.select_site.items = Global.site_options.keys()

  def submit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.select_site.selected_value is not None:
      Global.site_name = self.select_site.selected_value
      Global.site_id = Global.site_options[self.select_site.selected_value]
      Global.selected_site = ": " + Global.site_name
      Global.title_label.text = Global.title + Global.status + Global.selected_site
      #get more details of sites, e.g. How many areas, contexts, finds 
      site_information = anvil.server.call("site_get_information",Global.site_id)
      self.site_summary.text = "Site summary for " + Global.site_id + ": #Contexts: " + str(site_information["Contexts"]) + ", Finds:" + str(site_information["Finds"])
    pass

  def work_area_name_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    new_work_area_name = self.work_area_name.text
    #replace old work area name with new work area name in the two list (work area name list and work area list)
    #Global.work_area_name_list[Global.current_work_area].text = self.work_area_name.text
    #Global.work_area_list[Global.current_work_area]
    pass
