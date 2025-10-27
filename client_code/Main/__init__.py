from ._anvil_designer import MainTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

from ..Header import Header
from .. import Global
from .. import Function
from ..Help import Help

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    
    # get client variable settings from server configuration file
    globals_from_config = anvil.server.call("client_globals")
    Global.rows_per_page = globals_from_config["rows_per_page"]
    Global.version = globals_from_config["client_version"]
    Global.admin_domain = globals_from_config["admin_domain"]
    Global.admin_user = globals_from_config["admin_user"]
    Global.admin_user_initials = globals_from_config["admin_user_initials"]
    
    # add Header component (but make it invisible)
    Global.header = Header()
    self.add_component(Global.header, slot='header_slot')
    Global.header.visible = False
    
    # add Help component (but make it invisible)
    Global.help_page = Help()
    self.add_component(Global.help_page, slot='help_slot')
    Global.help_page.visible = False

    # set Main title field with name of organisation (defined in Anchurus-2.cgf file from server)
    Global.title_label = self.title
    self.title.text = Global.title + Global.status + Global.selected_site
    
    # add the about_us_text (taken from Anchurus-2.cfg file) to the about_us_box text field by adding a Rich Text Component
    rt = RichText(content=Global.about_us_text,format="restricted_html")
    self.about_us_box.add_component(rt)
    
    # Create empty work_area_list
    Global.work_area_list = {}

    # Get table list and create dropdown options for list and insert
    list = anvil.server.call("db_table_list")
    table_list = []
    print(list)
    for item in list:
      print(item)
      table_name = item.values()
      print(table_name)
      if table_name != "site" and table_name != "dbdiary":
        table_list.append(table_name)
    print(table_list)
    
    Global.insert_action_dropdown = table_list
    Global.list_action_dropdown = table_list
    # fill action menu options  
    self.insert_dropdown.items = Global.insert_action_dropdown
    self.list_dropdown.items = Global.list_action_dropdown
    self.admin_dropdown.items = Global.admin_action_dropdown
    self.file_dropdown.items = Global.file_list
    self.view_dropdown.items = Global.view_action_dropdown
    self.help_dropdown.items = Global.help_action_dropdown
    #
    self.file_dropdown.items = Global.file_action_dropdown

    #self.action_list.items = Global.user_action_list
    # make all fields invisible to only show about_us_text box as welcome followed by login and registration buttons (see design of Main)
    #self.action_list.visible = False
    self.menu_block.visible = False
    self.menu_top.visible = False
    self.menu_panel_left.visible = False
    self.menu_panel_right.visible = False
    self.admin_dropdown.visible = False

  def work_area_click(self, **event_args):
    # Here the user clicked on a button in the left navigation list, requested to go to a different work area.
    for name in Global.work_area:
      Global.work_area[name]["form"].visible = False
      Global.work_area[name]["button"].bold = False
      Global.work_area[name]["button"].background = Global.button_normal_background_clour
    # now get the name of the button (work_area_name) that was clicked and make this and the associated work_area visible
    work_area = event_args['sender']
    Global.current_work_area_name = work_area.text
    
    # Set Global.table_name linked with work_area_type
    Global.table_name = Global.work_area[Global.current_work_area_name]["action"].split(" ")[1][:-1].lower()
    
    # set Global variables for site information
    Global.site_name = Global.work_area[Global.current_work_area_name]["site_name"]
    Global.site_id = Global.work_area[Global.current_work_area_name]["site_id"]
    Global.selected_site = ": " + Global.site_name
    
    # Fill header fields with work_area name and work_area Form name
    Global.header_work_area_name.text = Global.current_work_area_name
    Global.header_work_area_type.text = str(type(Global.work_area[Global.current_work_area_name]["form"])).split(".")[2][:-2]
    Global.header_site_name.text = Global.work_area[Global.current_work_area_name]["site_name"]

    # Show work_area and set focus on work_area_name
    Global.work_area[Global.current_work_area_name]["form"].visible = True
    Global.work_area[Global.current_work_area_name]["button"].bold = False
    Global.work_area[Global.current_work_area_name]["button"].background = Global.button_highlight_background_clour
    Global.header.visible = True
    Global.action_form_type = str(type(Global.work_area[Global.current_work_area_name]["form"])).split(".")[2][:-2]

    # Set selected buttons on Header for work area type
    if Global.action_form_type in Global.action_forms_with_refresh:
      # Make refresh button visible for Global.action_form_type
      Global.header_refresh_button.visible = True
    else:
      Global.header_refresh_button.visible = False
    if Global.action_form_type in Global.action_forms_with_print:
      # Make print button visible for Global.action_form_type
      Global.header_print_button.visible = True
    else:
      Global.header_print_button.visible = False
    if Global.action_form_type in Global.action_forms_with_download:
      # Make download button visible for Global.action_form_type
      Global.header_download_button.visible = True
    else:
      Global.header_download_button.visible = False
    if Global.action_form_type in Global.action_forms_with_filter:
      # Make filter button visible for Global.action_form_type
      Global.header_filter_button.visible = True
    else:
      Global.header_filter_button.visible = False
  pass

  def create_new_work_area(self,action):
    # First make sure the header is visible
    Global.header.visible = True
    # set name of work_area to be action name if action is view or edit
    work_area_name = action
    if action == "View Context" or action == "Edit Context":
      # modify work_area name to add XxxxId number (ContextId, FindId, AeraId, etc); for now only implemented for Context
      Global.context_items = Global.table_items
      work_area_name = action + " " + Global.context_items["ContextId"]
    if action == "View Site" or action == "Edit Site":
      # modify work_area name to add XxxxId number (ContextId, FindId, AeraId, etc); for now only implemented for Context
      work_area_name = action + " " + Global.site_items["SiteId"]
    if action == "View Area" or action == "Edit Area":
      # modify work_area name to add XxxxId number (ContextId, FindId, AeraId, etc); for now only implemented for Context
      work_area_name = action + " " + Global.area_items["AreaId"]
    if action == "View Find" or action == "Edit Find":
      # modify work_area name to add XxxxId number (ContextId, FindId, AeraId, etc); for now only implemented for Context
      Global.find_items = Global.table_items
      work_area_name = action + " " + Global.find_items["FindId"]
    # check if work_area_name exists and keep counter
    if (Global.work_area.get(work_area_name) is None):
      if Global.action_seq_no.get(work_area_name) is None:
        # only set seq_no to 1 if the work_area_name has never been used before 
        Global.action_seq_no[work_area_name] = 1
      else:
        # this is for increasing the counter eventhough the work_area_name is not in use.
        # this code will cater if there have already been instances of work_area_name but 'earlier' ones have been deleted.
        Global.action_seq_no[work_area_name] += 1
        work_area_name = work_area_name + " (" + str(Global.action_seq_no[work_area_name]) + ")"
    else:
      # work_area_name exists, so update work_area_name to add seq_no in brackets
      Global.action_seq_no[work_area_name] += 1
      work_area_name = work_area_name + " (" + str(Global.action_seq_no[work_area_name]) + ")"

    # create new 'empty row' in nested work_area dictionary for the new work_area_name
    Global.work_area[work_area_name] = {}
    Global.work_area[work_area_name]["action"] = action
    Global.current_work_area_name = work_area_name

    # Set Global.table_name linked with work_area_type
    Global.table_name = Global.work_area[work_area_name]["action"].split(" ")[1].lower()

    # create the button for the work_area in the navigation panel and add it to the work_area_name_list
    Global.work_area[work_area_name]["button"] = Button(text=work_area_name,align="left")
    #Global.work_area[work_area_name]["button"] = Global.work_area_name_list[work_area_name]
    self.work_area_list.add_component(Global.work_area[work_area_name]["button"])
    Global.work_area[work_area_name]["button"].add_event_handler('click', self.work_area_click)
    # add the table_items to the work_area_name
    Global.work_area[work_area_name]["data_list"] = [Global.table_items]
    # create a new work_space and add this to the work_area_list      
    Global.work_area[work_area_name]["form"] = Function.create_work_space(action,Global.table_items)
    self.add_component(Global.work_area[work_area_name]["form"])
       
    # set button name to new work_area_name
    Global.work_area[work_area_name]["button"].text = work_area_name
    Global.work_area[work_area_name]["form_type"] = str(type(Global.work_area[work_area_name]["form"])).split(".")[2][:-2]
    #
    Global.work_area[work_area_name]["site_name"] = Global.site_name
    Global.header_site_name.text = Global.work_area[work_area_name]["site_name"]
    Global.work_area[work_area_name]["site_id"] = Global.site_id
    # set selected rows list to empty
    Global.work_area[work_area_name]["selected_rows"] = []

    # make all work spaces invisible
    for name in Global.work_area:
      Global.work_area[name]["form"].visible = False
      Global.work_area[name]["button"].bold = False
      Global.work_area[name]["button"].background = Global.button_normal_background_clour
    
    # create an empty filter and empty hidden_columns
    Global.work_area[Global.current_work_area_name]["filter"] = []
    Global.work_area[Global.current_work_area_name]["hidden_columns"] = []
    
    # Make selected work area visible and have Focus
    Global.work_area[work_area_name]["form"].visible = True
    Global.work_area[work_area_name]["button"].bold = False
    Global.work_area[work_area_name]["button"].background = Global.button_highlight_background_clour
    #
    Global.header_work_area_name.text = work_area_name
    Global.current_work_area_name = work_area_name
    Global.header_work_area_type.text = str(type(Global.work_area[Global.current_work_area_name]["form"])).split(".")[2][:-2]
    Global.header_work_area_type.enabled = False
    #Global.action_form_type = Global.header_work_area_type.text.split(".")[2][:-2]
    
    # Set selected buttons on Header for work area type
    Global.action_form_type = Global.header_work_area_type.text
    if Global.action_form_type in Global.action_forms_with_refresh:
      # make Refresh button visible if action_form_type has refresh function (i.e. in list Global.action_forms_with_refresh) 
      Global.header_refresh_button.visible = True
    else:
      Global.header_refresh_button.visible = False
    if Global.action_form_type in Global.action_forms_with_print:
      # make print button visible if action_form_type has print function (i.e. in list Global.action_forms_with_print) 
      Global.header_print_button.visible = True
    else:
      Global.header_print_button.visible = False    
    if Global.action_form_type in Global.action_forms_with_download:
      # Make download button visible for Global.action_form_type
      Global.header_download_button.visible = True
    else:
      Global.header_download_button.visible = False
    if Global.action_form_type in Global.action_forms_with_filter:
      # Make filter button visible for Global.action_form_type
      Global.header_filter_button.visible = True
    else:
      Global.header_filter_button.visible = False
    # reset action dropdown list
    #self.action_list.selected_value = None
    pass
  
  def login_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.login_with_form(allow_cancel=True)
    # check if user is logged in as newly registered account needs explicit enabling by administrator 
    # user = anvil.users.get_user()
    #if user is None and Global.admin_user != "":
      # this code should only run if Global.admin_user is disabled (which should only be at fist time run of anvil web server with clean user database)
      # this will set admin role and enable account for admin_user
      #print("First time login, set admin role and enable account for admin_user")
      #anvil.server.call('user_update',Global.admin_user,"admin",True,Global.admin_user_initials)
    #
    if user is not None:
      # make welcome block of Main form invisible
      self.welcome_page.visible = False
      
      # when user is logged in, enable Action menu, username field and logout button, and disable content panel (welcome message)
      # also set username  to user email address
      Global.username = user["email"]
      
      #Global.DBAcontrol = anvil.server.call("check_DBAcontrol",Global.username,"i")
      #self.username.text = Global.username + "\n (" + Global.user_role + ")"
      self.username_dropdown.placeholder = Global.username
      self.username_dropdown.items = ["Logout"]
      
      # check user authorisation - role columns will be updated in anvil user table
      Global.ip_address = anvil.server.call("user_authorisation")
      
      # if users has admin role, add admin actions list and set it visible
      user = anvil.users.get_user()
      Global.user_role = user["role"]
      if Global.user_role == "admin":
        #print(Global.username, Global.user_role)
        self.admin_dropdown.visible = True
      
      # make menu bar variable visible
      self.menu_block.visible = True
      self.menu_top.visible = True

      if anvil.users.get_user() is not None:
        sites_list = anvil.server.call('sites_get_summary')
        Global.site_options = {}
        for x in sites_list:
          val_list = list(x.values())
          option = val_list[0] + " - " + val_list[1]
          Global.site_options[option] = val_list[0]
        
      self.select_site_dropdown.items = Global.site_options.keys()

      # create a introduction message and add it to the introduction_message of the introduction_message block and make it visible
      Global.help_page.visible = True

    pass

  def register_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.signup_with_form(allow_cancel=True)
    # check if user logged in (should not be, as registration requires an administrator to enable account)
    # user = anvil.users.get_user()
    if user is not None:
      # when user is logged in enable Action menu, username field and logout button, and disable content panel (welcome message)
      # also set username  to user email address
      Global.username = user["email"]
      self.username_dropdown.placeholder = Global.username
      self.action_list.visible = True
      self.menu_top.visible = True
      self.welcome_page.visible = False
    pass

  def username_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    # This dropdown change means that the user selected for a Logout
    # as the only selection available in the dropdown list is Logout
    # But we just check in case it is not ;)
    if self.username_dropdown.selected_value == "Logout":
      # logout user, hide action menu, username and logout button; also delete all workspaces
      anvil.server.call("user_logout_notification",Global.ip_address,Global.username)
      anvil.users.logout()

      # make help_page invisible
      Global.help_page.visible = False

      # Welcome_page will show the login page
      self.welcome_page.visible = True
      
      # make menu block and admin menu invisible
      self.menu_block.visible = False
      self.menu_top.visible = False
      self.menu_panel_left.visible = False
      self.menu_panel_right.visible = False
      self.admin_dropdown.visible = False
      self.username_dropdown.placeholder = Global.username
      self.username_dropdown.items = []

      # To be done: save work areas in table for user for loading when login

      #delete all work_areas and all work_area names/buttons
      temp_work_area_name_list = list(Global.work_area.keys())
      for work_area_name in temp_work_area_name_list:
        Function.delete_workspace(work_area_name)

      # clear selected site
      self.select_site_dropdown.selected_value = None
      
      # clear work_area list and action_seq_no
      Global.work_area = {}
      Global.action_seq_no = {}
      
      #components = self.get_components()
      #print(f"{len(components)} components after deleting all workspaces")
    pass

  def select_site_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    # print("select_site_dropdown selected")
    if self.select_site_dropdown.selected_value is not None:
      # clear help_page_text 
      #Global.help_page.help_page_text.visible = True
      #Global.help_page.help_page_text.clear()
      Global.help_page.visible = False
      
      Global.site_name = self.select_site_dropdown.selected_value
      Global.site_id = Global.site_options[self.select_site_dropdown.selected_value]
      Global.selected_site = ": " + Global.site_name
      #Global.title_label.text = Global.title + Global.status + Global.selected_site
      Global.title_label.text = Global.title
      #get more details of sites, e.g. How many areas, contexts, finds 
      site_information = anvil.server.call("site_get_information",Global.site_id)
      #Global.header_site_name.text = Global.site_name
      self.site_summary.text = str(site_information["Contexts"]) + " Contexts, " + str(site_information["Finds"]) + " Finds"
      #
      self.menu_panel_left.visible = True
      self.menu_panel_right.visible = True

    pass
    
  def admin_dropdown_change(self, **event_args):
    """This method is called when an item from the dropdown menu is selected"""
    # Action has been selected, but only take action if action in not a separator
    # save a link to the Main form in a Global variable 
    Global.main_form = get_open_form()
    Global.action = self.admin_dropdown.selected_value

    if Global.action not in Global.action_list_not_implemented:
      # Action has been selected, create button in work area list, and make this work area in focus (highlight button)
      # for any action that has a Form defined create a new work_area
      if Global.site_id is None and Global.action not in (Global.admin_action_dropdown):
        # if site is not yet selected alert user
        alert(
          content="Site has not been selected. Please select a site.",
          title="Site selection warning",
          large=True,
          buttons=[("Ok", True)],
        )
      else:
        self.create_new_work_area(Global.action)
    else:
      if Global.action != Global.separator:
        alert("Action not yet implemented.")
        
    # clear selected_value
    self.admin_dropdown.selected_value = None
    pass

  def insert_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    Global.main_form = get_open_form()
    # make action to be "Add ..." 
    Global.action = "Add " + str(self.insert_dropdown.selected_value).capitalize()
    #print("Insert action - ",Global.action)
    if Global.action not in Global.action_list_not_implemented:
      # Action has been selected, create button in work area list, and make this work area in focus (highlight button)
      # for any action that has a Form defined create a new work_area
      if Global.site_id is None and Global.action not in (Global.admin_action_dropdown):
        # if site is not yet selected alert user
        alert(
          content="Site has not been selected. Please select a site.",
          title="Site selection warning",
          large=True,
          buttons=[("Ok", True)],
        )
      else:
        self.create_new_work_area(Global.action)
    else:
      if Global.action != Global.separator:
        alert("Action not yet implemented.")

    # clear selected_value
    self.insert_dropdown.selected_value = None
    pass

  def list_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    # clear selected_value
    Global.main_form = get_open_form()
    # make action to be "List ..."
    Global.action = "List " + str(self.list_dropdown.selected_value).capitalize()
    
    if Global.action not in Global.action_list_not_implemented:
      # Action has been selected, create button in work area list, and make this work area in focus (highlight button)
      # for any action that has a Form defined create a new work_area
      if Global.site_id is None and Global.action not in (Global.admin_action_dropdown):
        # if site is not yet selected alert user
        alert(
          content="Site has not been selected. Please select a site.",
          title="Site selection warning",
          large=True,
          buttons=[("Ok", True)],
        )
      else:
        self.create_new_work_area(Global.action)
    else:
      if Global.action != Global.separator:
        alert("Action not yet implemented.")
    
    self.list_dropdown.selected_value = None
    pass

  def help_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    Global.main_form = get_open_form()
    Global.action = self.help_dropdown.selected_value

    self.help_dropdown.selected_value = None
    pass

  def view_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    Global.main_form = get_open_form()
    Global.action = self.view_dropdown.selected_value

    self.view_dropdown.selected_value = None
    pass

  def file_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    
    Global.action = self.file_dropdown.selected_value
    if Global.action == "Import":
      self.create_new_work_area(Global.action)
    elif Global.action == "Save":
      Function.save_work_areas()
      
    self.file_dropdown.selected_value = None
    pass

