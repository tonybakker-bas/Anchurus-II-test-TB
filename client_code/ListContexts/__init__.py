from ._anvil_designer import ListContextsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
#import anvil.google.auth, anvil.google.drive
#from anvil.google.drive import app_files
from .. import Global
import anvil.server

class ListContexts(ListContextsTemplate):
  def list_contexts_refresh(self, **event_args):
    # This function does the filling of the table contents
    # 1. call server function 'context_get', which retrieves all conrtext for the given site
    self.ContextList.items = anvil.server.call("contexts_get", Global.site_id)
    # 2. set nr of rows per page from Global variable (which is defined by a parameter in the server-side config file)
    self.Context_list_1.rows_per_page = Global.nr_of_rows
    # 3.save the lilst of items in the Global 'work-area' dictionary
    Global.work_area[Global.current_work_area_name]["data_list"] = self.ContextList.items
    # Display the total number of rows 
    self.total_context_number.text = "Total number of Contexts: " + str(len(self.ContextList.items))
  pass

  def filter_columns(self, **event_args):
    # Extract columns headers from data_list
    if Global.work_area[Global.current_work_area_name]["data_list"]:
      # Get the keys (which are the column headings) from the first item
      column_headings = list(Global.work_area[Global.current_work_area_name]["data_list"][0].keys())

  pass
  
  def __init__(self, site_id, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.site_id = site_id
    # Any code you write here will run before the form opens.
    if Global.site_id is None:
      Global.site_id = site_id
    # ask the server for a list of the contexts and set nr of item per page on DataGrid (i.e. table) Context_list_1
    Global.context_id = ""
    #print("from Init ListContexts:",Global.site_id)
    # refresh the table content
    self.list_contexts_refresh()




