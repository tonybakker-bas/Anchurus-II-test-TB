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
    # this function does the filling of the table contents
    self.ContextList.items = anvil.server.call("contexts_get", Global.site_id)
    self.Context_list_1.rows_per_page = Global.nr_of_rows
    self.total_context_number.text = "Total number of Contexts: " + str(len(self.ContextList.items))
  pass
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
      
    # ask the server for a list of the contexts and set nr of item per page on DataGrid (i.e. table) Context_list_1
    Global.context_id = ""
    # refresh the table content
    self.list_contexts_refresh()




