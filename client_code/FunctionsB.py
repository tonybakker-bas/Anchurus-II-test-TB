import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .. import Module1
from  . import Global
#

def update_status_label(self):
  """ Calculates and updates the page control row information label with the current row range."""
  page_num = int(self.table.get_page())
  rows_per_page = int(self.table.rows_per_page)
  total_rows = len(self.repeating_panel_1.items)
  # Calculate the start and end row numbers
  start_row = (page_num) * rows_per_page + 1
  end_row = min((page_num + 1) * rows_per_page, total_rows)
  # The page control buttons are not in self but in main form
  if page_num == 0:
    # disable first_page_btn and prev_page_btn if on page 0
    Global.main_form.first_page.enabled = False
    Global.main_form.prev_page.enabled = False
  else:
    Global.main_form.first_page.enabled = True
    Global.main_form.prev_page.enabled = True
  if (rows_per_page != 0) and (page_num == (total_rows // rows_per_page)):
    # disable last_page_btn and next_page_btn if on last page
    Global.main_form.last_page.enabled = False
    Global.main_form.next_page.enabled = False
  else:
    Global.main_form.last_page.enabled = True
    Global.main_form.next_page.enabled = True

  # Display the formatted string in the status label if 
  if total_rows > rows_per_page and rows_per_page != 0:
    Global.main_form.row_number_info.text = f"{start_row}-{end_row} of {total_rows}"
  else:
    # No need to display page control buttons as nr of rows is less than 
    Global.main_form.last_page.visible = False
    Global.main_form.next_page.visible = False      
    Global.main_form.first_page.visible = False
    Global.main_form.prev_page.visible = False
    Global.main_form.row_number_info.text = "Total " + str(total_rows) + " rows"
  #
  Global.work_area[Global.current_work_area_name]["page_info"] = {"page_num": page_num, "rows_per_page": rows_per_page, "total_rows": total_rows}
  return

def clear_selection(self):
  # clear select checkbox of rows
  for row in self.repeating_panel_1.get_components():
    row.btn_select.checked = False
    row.background = ""

  # clear selection list
  Global.work_area[Global.current_work_area_name]["selected_rows"].clear()

  # clear select_all checkbox
  Global.main_form.select_all.checked = False
  return

def table_list_refresh(self):
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
  update_status_label(self)

  #self.information.text = Global.table_name
  return