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
from .. import Function
from .. import Global
import anvil.server

class TableList(TableListTemplate):
  def update_status_label(self, **event_args):
    """Calculates and updates the label with the current row range."""
    page_num = int(self.table.get_page())
    rows_per_page = int(self.table.rows_per_page)
    total_rows = len(self.repeating_panel_1.items)
    # Calculate the start and end row numbers
    start_row = (page_num) * rows_per_page + 1
    end_row = min((page_num + 1) * rows_per_page, total_rows)
    # 
    if page_num == 0:
      # disable first_page_btn and prev_page_btn if on page 0
      self.first_page_btn.enabled = False
      self.prev_page_btn.enabled = False
    else:
      self.first_page_btn.enabled = True
      self.prev_page_btn.enabled = True
    if (rows_per_page != 0) and (page_num == (total_rows // rows_per_page)):
      # disable last_page_btn and next_page_btn if on last page
      self.last_page_btn.enabled = False
      self.next_page_btn.enabled = False
    else:
      self.last_page_btn.enabled = True
      self.next_page_btn.enabled = True

    # Display the formatted string in the status label if 
    if total_rows > rows_per_page and rows_per_page != 0:
      self.row_number_info.text = f"{start_row}-{end_row} of {total_rows}"
    else:
      # No need to display page control buttons as nr of rows is less than 
      self.last_page_btn.visible = False
      self.next_page_btn.visible = False      
      self.first_page_btn.visible = False
      self.prev_page_btn.visible = False
      self.row_number_info.text = "Total " + str(total_rows) + " rows"
    #
    Global.work_area[Global.current_work_area_name]["page_info"] = {"page_num": page_num, "rows_per_page": rows_per_page, "total_rows": total_rows}
  pass

  def clear_selection(self, **event_args):
    # clear select checkbox of rows
    for row in self.repeating_panel_1.get_components():
      row.btn_select.checked = False
      row.background = ""
        
    # clear selection list
    Global.work_area[Global.current_work_area_name]["selected_rows"].clear()
    
    # clear select_all checkbox
    self.select_all.checked = False
  pass
  
  def table_list_refresh(self, **event_args):
    # This function does the filling of the table contents
    # 1. call server function '"table_name"s_get', which retrieves all rows of the table_name for the given site
    self.repeating_panel_1.items = anvil.server.call("table_get",Global.site_id,Global.table_name)

    # 2. set nr of rows per page from Global variable (which is defined by a parameter in the server-side config file)
    #if Global.rows_per_page is not None:
    self.table.rows_per_page = Global.rows_per_page
    if len(self.page_info) != 0:# this means this form is called from the server (print function)
      self.table.rows_per_page = self.page_info["rows_per_page"]
      self.table.set_page(self.page_info["page_num"])
      
    # 3.save the list of items in the Global 'work-area' dictionary
    if Global.current_work_area_name is not None:
      Global.work_area[Global.current_work_area_name]["data_list"] = self.repeating_panel_1.items
       
    # Trigger the initial update
    self.update_status_label()
    
    # Display the total number of rows
    self.information.text = Global.table_name
  pass

  def view_button_click(self, **event_args):
    """This handler is called by the dynamically created button."""
    #
    for row in Global.work_area[Global.current_work_area_name]["selected_rows"]:
      Global.table_items = row
      #print("View button for row: ",row)
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
    #
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
    message = ""
    for row in Global.work_area[Global.current_work_area_name]["selected_rows"]:
      Global.table_items = row
      #print(row)
      Global.action = "Delete " + Global.table_name.capitalize()
      message = message + "\nYou have seleted to delete " + Global.table_name.capitalize() + "\n\n" + str(row)
    
    # ask confirmation to delete selected rows
    message = message + "\n\nDo you wish to continue?"
    confirm(message)
  pass

  def __init__(self, site_id, table_name, data_list, action, page_info, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #
    self.column_panel_1.visible = False
    #
    self.repeating_panel_1.set_event_handler('x-selection-change', self.selection_change)
    #
    self.page_info = page_info
    self.site_id = site_id
    # Any code you write here will run before the form open
    # Global.site_id is only None when form called from server side (e.g. printing form)
    if Global.site_id is None:
      # initialise some Globals variables for when the function is called from the server side
      Global.site_id = site_id
      Global.current_work_area_name = "TableList"
      Global.work_area = {}
      Global.work_area[Global.current_work_area_name] = {}
      Global.table_name = table_name.rstrip("s")
    else:
    # set table_name to one of "context", "find", from the action Global variable 
      Global.table_name = Global.action.split(" ")[1].lower()
    
    # get the Table information form the Database
    table_info = anvil.server.call("describe_table", Global.table_name)

    # Extract the columns names from the table_info
    # Frist column if for Select
    # The DESCRIBE result structure is:
    # (Field:, Type:, Null:, Key:, Default:, Extra:)
    Global.work_area[Global.current_work_area_name]["columns_show"] = []
    columns_titles = []
    columns_titles.append({"id": 1, "title": "", "data_key": "select", "width": 30, "expand": True })
    id = 1
    for column_data in table_info:
      # Select Column "Field"
      field_name = column_data["Field"]
      Global.work_area[Global.current_work_area_name]["columns_show"].append(field_name)
      col_width = Global.table_colwidth_default
      if field_name in Global.table_colwidth_60:
        col_width = 60
      if field_name in Global.table_colwidth_80:
        col_width = 80
      if field_name in Global.table_colwidth_100:
        col_width = 100
      if field_name in Global.table_colwidth_120:
        col_width = 120
      if field_name in Global.table_colwidth_140:
        col_width = 140
      if field_name not in ["SiteId"]: # do not create a columns for SiteId
        id = id + 1
        columns_titles.append({"id": id, "title": field_name, "data_key": field_name, "width": col_width, "expand": True })

    # assign the columns titles to the grid columns
    self.table.columns = columns_titles

    # add table to work_area data structure for Global.current_work_area_name
    Global.work_area[Global.current_work_area_name]["table"] = self.table
    
    # Set table role to horizontal scroll
    self.table.role = "horizontal-scroll"
    
    # set menu_select_opti0ns as invisible
    #Global.work_area[Global.current_work_area_name]["menu_select_options"] = self.menu_select_options
    #Global.work_area[Global.current_work_area_name]["menu_select_options"].visible = False

    # save self in Global.work_area
    Global.work_area[Global.current_work_area_name]["self"] = self

    #self.table_list_refresh()
    Function.table_list_refresh(self)


    
  def selection_change(self, **event_args):
    #
    rows = [row for row in self.repeating_panel_1.get_components()]
    any_checked = any(row.btn_select.checked for row in rows)
    all_checked = all(row.btn_select.checked for row in rows)
    print("any_checked: ",any_checked)
    print("all_checked: ",all_checked)
    indeterminate_value = not all_checked and any_checked
    print("indeterminate: ",indeterminate_value)
    # make select_all a Global.work_area[Global.Global.current_work_area_name]["select_all"]
    self.select_all.checked = any_checked
    self.select_all.indeterminate = not all_checked and any_checked
    Global.main_form.select_all.checked = any_checked
    Global.main_form.select_all.indeterminate = not all_checked and any_checked
    Global.work_area[Global.current_work_area_name]["menu_select_options"].visible = any_checked
    #
    pass
    
  def select_all_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    checked = self.select_all.checked
    #
    for row in self.repeating_panel_1.get_components():
      prev_status_btn_select = row.btn_select.checked
      row.btn_select.checked = checked
      #
      if checked:
        Global.work_area[Global.current_work_area_name]["selected_rows"].append(row.item)
        row.background = Global.selected_highlight_colour
      else:
        if prev_status_btn_select:
          Global.work_area[Global.current_work_area_name]["selected_rows"].remove(row.item)
          row.background = ""
    #
    self.select_all.indeterminate = False
    Global.main_form.select_all.indeterminate = False
    #
    if len(Global.work_area[Global.current_work_area_name]["selected_rows"]) == 0:
      Global.work_area[Global.current_work_area_name]["menu_select_options"].visible = False
    else:
      Global.work_area[Global.current_work_area_name]["menu_select_options"].visible = True
    pass

  def first_page_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.clear_selection()
    self.table.set_page(0)
    self.update_status_label()
    pass

  def prev_page_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.clear_selection()
    self.table.set_page(self.table.get_page() - 1)
    self.update_status_label()
    pass

  def next_page_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.clear_selection()
    self.table.set_page(self.table.get_page() + 1)
    self.update_status_label()
    pass

  def last_page_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.clear_selection()
    rows_per_page = int(self.table.rows_per_page)
    total_rows = len(self.repeating_panel_1.items)
    self.table.set_page(total_rows // rows_per_page)
    self.update_status_label()
    pass
    

