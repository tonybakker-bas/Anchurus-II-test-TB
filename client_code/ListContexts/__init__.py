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
    #print(self.ContextList.items)
    # 2. set nr of rows per page from Global variable (which is defined by a parameter in the server-side config file)
    if Global.nr_of_rows is not None:
      self.Context_list_1.rows_per_page = Global.nr_of_rows
    # 3.save the list of items in the Global 'work-area' dictionary
    if Global.current_work_area_name is not None:
      Global.work_area[Global.current_work_area_name]["data_list"] = self.ContextList.items
    # Display the total number of rows 
    self.total_context_number.text = "Total number of Contexts: " + str(len(self.ContextList.items))
  pass
  
  def __init__(self, site_id, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #
    self.site_id = site_id
    # Any code you write here will run before the form open
    # Global.site_id is only None when form called from server side (e.g. printing form)
    if Global.site_id is None:
      # initialise some Globals variables for server side function call
      Global.site_id = site_id
      Global.current_work_area_name = "ContextList"
      Global.work_area[Global.current_work_area_name] = {}

    # Create your Data Grid 
    grid = DataGrid()
    # Add the Data Grid to your Form
    self.add_component(grid,full_width_row=True)
    table_info = anvil.server.call("describe_table","context")
    
    #print(table_info)
    # The DESCRIBE result structure is:
    # (Field:, Type:, Null:, Key:, Default:, Extra:)
    id = 0
    grid.columns = []
    for column_data in table_info:
      # Select Column Field
      field_name = column_data["Field"]
      id = id + 1
      grid.columns.append({"id": id, "title": field_name, "data_key": field_name}) 
      #'text': column_name, 'id': option_id})
    print(grid.columns)
    # Add two columns to your Data Grid
    grid.columns = [
      { "id": "1", "title": "SiteId", "data_key": "SiteId" },
      { "id": "2", "title": "ContextId", "data_key": "ContextId" },
    #  { "id": "3", "title": "Address2", "data_key": "address2" },
    #  { "id": "4", "title": "Address3", "data_key": "address3" },
    #  { "id": "5", "title": "Address4", "data_key": "address4" },
    #  { "id": "6", "title": "Address5", "data_key": "address5" },
    #  { "id": "7", "title": "Address6", "data_key": "address6" },
    #  { "id": "8", "title": "Address7", "data_key": "address7" },
    #  { "id": "9", "title": "Address8", "data_key": "address8" },
    #  { "id": "10", "title": "Address9", "data_key": "address9" },
    #  { "id": "11", "title": "Address10", "data_key": "address10" },
    #  { "id": "12", "title": "Address11", "data_key": "address11" },
    #  { "id": "13", "title": "Address12", "data_key": "address12" },
    #  { "id": "14", "title": "Address13", "data_key": "address13" },
    ]
    #print(grid.columns)
    rp = RepeatingPanel(item_template=DataRowPanel)
    # Set its items property
    rp.items = [
      #{'name': 'Alice', 'address': 'London'},
      #{'name': 'John', 'address': 'Amsterdam'}
      {'SiteId': 'S10001', 'ContextId': 'C10001'},
      {'SiteID': 'S10001', 'ContextId': 'C10002'}
    ]
    # Add the repeating panel to your data grid
    grid.add_component(rp,full_width_row=True)
    grid.rows_per_page = 20
    
    Global.context_id = ""
    # refresh the table content
    self.list_contexts_refresh()




