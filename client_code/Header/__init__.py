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

from ..TableList import TableList
from ..ListContexts import ListContexts
from ..ListFinds import ListFinds
from ..ListAreas import ListAreas
from ..ListSites import ListSites
from ..ListUsers import ListUsers
from ..BulkUpload import BulkUpload
from ..FilterList import FilterList 

class Header(HeaderTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    Global.header_work_area_name = self.work_area_name
    Global.header_work_area_type = self.work_area_type
    Global.header_site_name = self.site_name
    Global.header_refresh_button = self.refresh_button
    Global.header_print_button = self.print_button
    Global.header_download_button = self.download_button
    Global.header_filter_button = self.filter_button
    Global.header_refresh_button.visible = False
    Global.header_print_button.visible = False
    Global.header_download_button.visible = False
    Global.header_filter_button.visible = False

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
      Global.work_area[new_work_area_name] = {}
      Global.work_area[new_work_area_name] = Global.work_area[Global.current_work_area_name]
      Global.work_area[new_work_area_name]["button"].text = new_work_area_name
      
      # remove old key/value pair for the old work_area_name from the dictionaries     
      Global.work_area.pop(Global.current_work_area_name)

      # update Global.curret_work_area_name with new name
      Global.current_work_area_name = new_work_area_name
      
    pass

  def print_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    form = str(type(Global.work_area[Global.current_work_area_name]["form"])).split(".")[2][:-2]
    #print("calling print_form on server for form: ",form)
    table_name = Global.work_area[Global.current_work_area_name]["action"].split(" ")[1][:-1].lower()
    print("table name for print = ",table_name)
    pdf_form = anvil.server.call('print_form',form,Global.site_id,table_name)
    anvil.media.download(pdf_form)
    pass

  def refresh_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # select correct refresh function to call
    #print("Refresh button clicked. Action is:", Global.work_area[Global.current_work_area_name]["action"], ", Action_form_type is: ",Global.work_area[Global.current_work_area_name]["form"])
    # select the correct refresh depending on Global.action_form_type
    if Global.work_area[Global.current_work_area_name]["action"] in ["List Contexts", "List Finds"]:
      TableList.table_list_refresh(Global.work_area[Global.current_work_area_name]["form"])
    #  ListContexts.list_contexts_refresh(Global.work_area[Global.current_work_area_name]["form"])
    #elif Global.work_area[Global.current_work_area_name]["action"] == "List Finds":
    #  ListFinds.list_finds_refresh(Global.work_area[Global.current_work_area_name]["form"])
    elif Global.work_area[Global.current_work_area_name]["action"] == "List Areas":
      ListAreas.list_areas_refresh(Global.work_area[Global.current_work_area_name]["form"])  
    elif Global.work_area[Global.current_work_area_name]["action"] == "List Sites":
      ListSites.list_sites_refresh(Global.work_area[Global.current_work_area_name]["form"]) 
    elif Global.work_area[Global.current_work_area_name]["action"] == "List Users":
      ListUsers.list_users_refresh(Global.work_area[Global.current_work_area_name]["form"]) 
    elif Global.work_area[Global.current_work_area_name]["action"] == "BulkUpload":
      BulkUpload.bulk_upload_refresh(Global.work_area[Global.current_work_area_name]["form"])
    pass

  def delete_work_area_click(self, **event_args):
    """This method is called when the button is clicked"""
    Function.delete_workspace(self.work_area_name.text)
    pass

  def download_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    #form = str(type(Global.work_area[Global.current_work_area_name]["form"])).split(".")[2][:-2]
    csv_file = anvil.server.call('create_csv',Global.work_area[Global.current_work_area_name]["data_list"])
    anvil.media.download(csv_file)
    pass

  def filter_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # extract table columns names
    if Global.work_area[Global.current_work_area_name]["data_list"]:
      # Get the keys (which are the column headings) from the first item
      column_headings = list(Global.work_area[Global.current_work_area_name]["data_list"][0].keys())
 
    # 1. Define the options you want to display
    option_id = 0
    options_data = []
    for column_name in column_headings:
      option_id = option_id + 1
      options_data.append({'text': column_name, 'id': option_id})

    # 2. Create an instance of your Dialog Form
    dialog = FilterList(options_list=options_data)

    # 3. Use alert() to show the form as a modal popup
    # The alert() function will return the 'value' passed when 'x-close-alert' is raised
    selected_list = alert(
      content=dialog, 
      title="",
      buttons=[] # Crucial: set buttons=[] to use your custom button for submission
    )
    
    # 4. Process the result after the dialog is closed
    # loop through columns and hide the one not seleced (but not the cols with empty titles!)
    all_columns_titles = [col["title"] for col in Global.work_area[Global.current_work_area_name]["table"].columns if "title" in col]
    selected_columns_titles = [col["text"] for col in selected_list if "text" in col]
    print(all_columns_titles)
    print(selected_columns_titles)
    columns_not_selected = list(set(all_columns_titles).difference(selected_columns_titles))
    print(columns_not_selected)
    
    #if selected_list:
    #  print("User selected the following columns:")
    #  for item in selected_list:
    #    print(f"- {item['text']} (ID: {item['id']})")
    #else:
    #  # This occurs if the user closes the modal without clicking a button
    #  print("Selection was cancelled or dismissed.")
    pass


    
