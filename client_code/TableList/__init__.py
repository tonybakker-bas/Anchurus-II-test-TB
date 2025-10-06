from ._anvil_designer import TableListTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
from .. import Global
import anvil.server

class TableList(TableListTemplate):
  def table_list_refresh(self, **event_args):
    # This function does the filling of the table contents
    # 1. call server function '"table_name"s_get', which retrieves all rows of the table_name for the given site
    self.repeating_panel_1.items= anvil.server.call("table_get",Global.site_id,Global.table_name)

    # 2. set nr of rows per page from Global variable (which is defined by a parameter in the server-side config file)
    if Global.nr_of_rows is not None:
      self.table.rows_per_page = Global.nr_of_rows

    # 3.save the list of items in the Global 'work-area' dictionary
    if Global.current_work_area_name is not None:
      Global.work_area[Global.current_work_area_name]["data_list"] = (
        self.repeating_panel_1.items
      )
    # Display the total number of rows
    self.total_number.text = "Total number of rows: " + str(len(self.repeating_panel_1.items))
    self.information.text = Global.table_name
  pass

  def __init__(self, site_id, table_name, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #
    self.site_id = site_id
    # Any code you write here will run before the form open
    # Global.site_id is only None when form called from server side (e.g. printing form)
    if Global.site_id is None:
      # initialise some Globals variables for when the function is called from the server side
      Global.site_id = site_id
      Global.current_work_area_name = "TableList"
      Global.table_name = table_name
      Global.work_area[Global.current_work_area_name] = {}
      Global.table_name = table_name
    else:
    # set table_name to one of "context", "find", from the action Global variable 
      Global.table_name = Global.action.split(" ")[1][:-1].lower()
    
    # get the Table information form the Database
    table_info = anvil.server.call("describe_table", Global.table_name)

    # Extract the columns names from the table_info
    # Frist two columns are vor View and Edit icon
    # The DESCRIBE result structure is:
    # (Field:, Type:, Null:, Key:, Default:, Extra:)
    columns_titles = []
    columns_titles.append({"id": 1, "title": "", "data_key": "view", "width": 30, "expand": True })
    columns_titles.append({"id": 2, "title": "", "data_key": "edit", "width": 30, "expand": True })
    columns_titles.append({"id": 3, "title": "", "data_key": "delete", "width": 30, "expand": True })
    id = 3
    for column_data in table_info:
      # Select Column "Field"
      field_name = column_data["Field"]
      id = id + 1
      columns_titles.append({"id": id, "title": field_name, "data_key": field_name, "width": 150, "expand": True })
      #'text': column_name, 'id': option_id})

    # assign the columns titles to the grid columns
    self.table.columns = columns_titles

    # Add the repeating panel to the data grid and set rows_per_page
    #self.grid.add_component(self.rp, full_width_row=True)
    self.table.rows_per_page = Global.nr_of_rows
    self.table.role = "horizontal-scroll"

    #???
    Global.context_id = ""
    # refresh the table content
    self.table_list_refresh()