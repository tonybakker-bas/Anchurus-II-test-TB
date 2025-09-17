from ._anvil_designer import HeaderTemplate
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

class Header(HeaderTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    Global.header_work_area_name = self.work_area_name
    Global.header_work_area_type = self.work_area_type
    Global.header_refresh_button = self.refresh_button
    Global.header_refresh_button.visible = False

  def delete_work_area_click(self, **event_args):
    """This method is called when the button is clicked"""
    Function.delete_workspace(self.work_area_name.text)
    pass

  def work_area_name_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    # This is the work_area_name field and a new name has been enterd.
    new_work_area_name = self.work_area_name.text
    # No we need to check if it is acceptable, i.e. unique; can do the check on one of the two lists (work_area_list or work_area_name_list)
    if new_work_area_name in Global.work_area:
      # name exists, so not unique, hence name change not accepted
      alert("The new work area name is already in use. Please change it.")
    else:
      # new name is unique so now add new work area name in the two lists (one for buttons and one for the forms 
      #Global.work_area_list[new_work_area_name] = Global.work_area_list[Global.current_work_area_name]
      #Global.work_area_action[new_work_area_name] = Global.work_area_action[Global.current_work_area_name] 
      #Global.work_area_name_list[new_work_area_name] = Global.work_area_name_list[Global.current_work_area_name]
      #Global.work_area_name_list[new_work_area_name].text = new_work_area_name
      Global.work_area[new_work_area_name] = {}
      Global.work_area[new_work_area_name] = Global.work_area[Global.current_work_area_name]
      Global.work_area[new_work_area_name]["button"].text = new_work_area_name
      # remove old key/value pair for the old work_area_name from the dictionaries
      #Global.work_area_list.pop(Global.current_work_area_name)
      #Global.work_area_action.pop(Global.current_work_area_name)
      #Global.work_area_name_list.pop(Global.current_work_area_name)
      #print(Global.work_area)
      Global.work_area.pop(Global.current_work_area_name)
      #print(Global.work_area)
      # update Global.curret_work_area_name with new name
      Global.current_work_area_name = new_work_area_name
      #
    pass

  def print_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    print("calling print_form on server")
    pdf_form = anvil.server.call('print_form','ListContexts',Global.site_id)
    anvil.media.download(pdf_form)
    pass

  def refresh_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # select correct refresh function to call
    #print("Refresh button clicked. Action is:", Global.work_area[Global.current_work_area_name]["action"], ", Action_form_type is: ",Global.work_area[Global.current_work_area_name]["form"])
    # select the correct refresh depending on Global.action_form_type
    if Global.work_area[Global.current_work_area_name]["action"] == "List Contexts":
      ListContexts.list_contexts_refresh(Global.work_area[Global.current_work_area_name]["form"])
    elif Global.work_area[Global.current_work_area_name]["action"] == "List Finds":
      ListFinds.list_finds_refresh(Global.work_area[Global.current_work_area_name]["form"])
    elif Global.work_area[Global.current_work_area_name]["action"] == "List Areas":
      ListAreas.list_areas_refresh(Global.work_area[Global.current_work_area_name]["form"])  
    elif Global.work_area[Global.current_work_area_name]["action"] == "List Sites":
      ListSites.list_sites_refresh(Global.work_area[Global.current_work_area_name]["form"]) 
    elif Global.work_area[Global.current_work_area_name]["action"] == "List Users":
      ListUsers.list_users_refresh(Global.work_area[Global.current_work_area_name]["form"]) 
    elif Global.work_area[Global.current_work_area_name]["action"] == "BulkUpload":
      BulkUpload.bulk_upload_refresh(Global.work_area[Global.current_work_area_name]["form"])
    pass


    
