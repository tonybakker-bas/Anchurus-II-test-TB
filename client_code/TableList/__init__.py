from ._anvil_designer import TableListTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import indeterminate

# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
from .. import Global
import anvil.server

class TableList(TableListTemplate):
  def table_list_refresh(self, **event_args):
    # This function does the filling of the table contents
    # 1. call server function '"table_name"s_get', which retrieves all rows of the table_name for the given site
    self.repeating_panel_1.items = anvil.server.call("table_get",Global.site_id,Global.table_name)

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

  def view_button_click(self, **event_args):
    """This handler is called by the dynamically created button."""
    #print("View selected rows")
    #print(Global.work_area[Global.current_work_area_name]["selected_rows"])
    for row in Global.work_area[Global.current_work_area_name]["selected_rows"]:
      Global.table_items = row
      Global.action = "View " + Global.table_name.capitalize()
      if Global.main_form:  # Important to check if the form exists
        # Create new work_area "View Context" and set focus on this new work_area
        #print("From repatingPanel row calling create_new_work_area for:",Global.action)
        Global.main_form.create_new_work_area(Global.action)
      else:
        print("Main form not found!")
  pass

  def edit_button_click(self, **event_args):
    """This handler is called by the dynamically created button."""
    #print("View selected rows")
    #print(Global.work_area[Global.current_work_area_name]["selected_rows"])
    for row in Global.work_area[Global.current_work_area_name]["selected_rows"]:
      Global.table_items = row
      Global.action = "Edit " + Global.table_name.capitalize()
      if Global.main_form:  # Important to check if the form exists
        # Create new work_area "View Context" and set focus on this new work_area 
        Global.main_form.create_new_work_area(Global.action)
      else:
        print("Main form not found!")
  pass

  def delete_button_click(self, **event_args):
    """This handler is called by the dynamically created button."""
    #print(self.item)
    #print(Global.table_name)
    message = ""
    for row in Global.work_area[Global.current_work_area_name]["selected_rows"]:
      Global.table_items = row
      print(row)
      Global.action = "Delete " + Global.table_name.capitalize()
      message = message + "\nYou have seleted to delete " + Global.table_name.capitalize() + "\n\n" + str(row)
    
    # ask confirmation to delete selected rows
    message = message + "\n\nDo you wish to continue?"
    confirm(message)
  pass

  def __init__(self, site_id, table_name, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #
    self.table.set_event_handler('x-selection-change', self.selection_change)
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
    # Frist column if for Select
    # The DESCRIBE result structure is:
    # (Field:, Type:, Null:, Key:, Default:, Extra:)
    columns_titles = []
    columns_titles.append({"id": 1, "title": "", "data_key": "select", "width": 30, "expand": True })
    id = 1
    for column_data in table_info:
      # Select Column "Field"
      field_name = column_data["Field"]
      if field_name not in ["SiteId"]: # do not create a columns for SiteId
        id = id + 1
        columns_titles.append({"id": id, "title": field_name, "data_key": field_name, "width": 150, "expand": True })

    # assign the columns titles to the grid columns
    self.table.columns = columns_titles

    # add table to work_area data structure for Global.current_work_area_name
    Global.work_area[Global.current_work_area_name]["table"] = self.table
    
    # Add the repeating panel to the data grid and set rows_per_page
    self.table.rows_per_page = Global.nr_of_rows
    self.table.role = "horizontal-scroll"
    
    # set menu_select_opti0ns as invisible
    Global.menu_select_options = self.menu_select_options
    Global.menu_select_options.visible = False

    #???
    #Global.context_id = ""
    # refresh the table content
    self.table_list_refresh()

  def selection_change(self, **event_args):
    print("in selection_change")

    rows = [row for row in self.table.get_components()]
    any_checked = any(row.btn_select.checked for row in rows)
    all_checked = all(row.btn_select.checked for row in rows)

    self.select_all.checked = any_checked
    self.select_all.indeterminate = not all_checked and any_checked
    self.action_button.visible = any_checked
    pass
    
  def select_all_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    checked = self.select_all.checked
    for row in self.repeating_panel_1.get_components():
      print(row)
      row.btn_select.checked = checked
      # also add row to word_area data_structure

    self.select_all.indeterminate = False
    #self.action_button.visible = checked
    Global.menu_select_options.visible = checked
    pass

