from ._anvil_designer import MainTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

#from ..WorkArea import WorkArea
from ..Header import Header
from ..GlobalHeader import GlobalHeader
#from ..Welcome import Welcome
from .. import Global
from .. import Function

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    globals_from_config = anvil.server.call("client_globals")
    Global.nr_of_rows = globals_from_config["rows_per_page"]
    Global.version = globals_from_config["client_version"]
    Global.admin_domain = globals_from_config["admin_domain"]
    Global.admin_user = globals_from_config["admin_user"]
    Global.admin_user_initials = globals_from_config["admin_user_initials"]
    #
    Global.GlobalHeader = GlobalHeader()
    self.add_component(Global.GlobalHeader, slot='GlobalHeaderheaderSlot')
    Global.GlobalHeader.visible = False
    Global.header = Header()
    self.add_component(Global.header, slot='header_slot')
    Global.header.visible = False
    # set Main title field with name of organisation (defined in Anchurus-2.cgf file from server)
    Global.title_label = self.title
    self.title.text = Global.title + Global.status + Global.selected_site
    # add the about_us_text (taken from Anchurus-2.cfg file) to the about_us_box text field by adding a Rich Text Component
    rt = RichText(content=Global.about_us_text,format="restricted_html")
    self.about_us_box.add_component(rt)
    # fill action menu options - taken from action_list defined in Global 
    Global.work_area_list = {}
    self.action_list.items = Global.user_action_list
    # make all fields invisible to only show about_us_text box as welcome followed by login and registration buttons (see design of Main)
    self.admin_action_list.visible = False
    self.action_list.visible = False
    self.logout_button.visible = False
    self.username.visible = False
      
  def work_area_click(self, **event_args):
    # Here the user clicked on a button in the left navigation list, requested to go to a different work area.
    # Firstly make all work_area_list elements invisible and set to unfocus (unbold) work_area_name_list elements
    #for name in Global.work_area_list:
    for name in Global.work_area:
      #print(name)
      Global.work_area[name]["form"].visible = False
      Global.work_area[name]["button"].bold = False
      Global.work_area[name]["button"].background = Global.button_normal_background_clour
    # now get the name of the button (work_area_name) that was clicked and make this and the associated work_area visible
    work_area = event_args['sender']
    Global.current_work_area_name = work_area.text
    #print("Work Area click: ", Global.current_work_area_name)
    # Fill header fields with work_area name and work_area Form name
    Global.header_work_area_name.text = Global.current_work_area_name
    Global.header_work_area_type.text = str(type(Global.work_area[Global.current_work_area_name]["form"])).split(".")[2][:-2]
    # Show work_area and set focus on work_aerea_name
    Global.work_area[Global.current_work_area_name]["form"].visible = True
    Global.work_area[Global.current_work_area_name]["button"].bold = True
    Global.work_area[Global.current_work_area_name]["button"].background = Global.button_highlight_background_clour
    Global.header.visible = True
    Global.action_form_type = str(type(Global.work_area[Global.current_work_area_name]["form"])).split(".")[2][:-2]
    #print("header_refresh_button: ",Global.header_refresh_button)

    # Set selected buttons on Header for work area type
    if Global.action_form_type in Global.action_forms_with_refresh:
      # Make refresh button visible for Global.action_form_type
      Global.header_refresh_button.visible = True
    else:
      Global.header_refresh_button.visible = False
    #print("header_print_button: ",Global.header_print_button)
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
      work_area_name = action + " " + Global.context_items["ContextId"]
    if action == "View Site" or action == "Edit Site":
      # modify work_area name to add XxxxId number (ContextId, FindId, AeraId, etc); for now only implemented for Context
      work_area_name = action + " " + Global.site_items["SiteId"]
    if action == "View Area" or action == "Edit Area":
      # modify work_area name to add XxxxId number (ContextId, FindId, AeraId, etc); for now only implemented for Context
      work_area_name = action + " " + Global.area_items["AreaId"]
    if action == "View Find" or action == "Edit Find":
      # modify work_area name to add XxxxId number (ContextId, FindId, AeraId, etc); for now only implemented for Context
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

    # create the button for the work_area in the navigation panel and add it to the work_area_name_list
    Global.work_area[work_area_name]["button"] = Button(text=work_area_name,align="left")
    #Global.work_area[work_area_name]["button"] = Global.work_area_name_list[work_area_name]
    self.work_area_list.add_component(Global.work_area[work_area_name]["button"])
    Global.work_area[work_area_name]["button"].add_event_handler('click', self.work_area_click)
    # create a new work_space and add this to the work_area_list      
    Global.work_area[work_area_name]["form"] = Function.create_work_space(action)
    self.add_component(Global.work_area[work_area_name]["form"])
    # set button name to new work_area_name
    Global.work_area[work_area_name]["button"].text = work_area_name
    
    # make all work spaces invisible
    for name in Global.work_area:
      Global.work_area[name]["form"].visible = False
      Global.work_area[name]["button"].bold = False
      Global.work_area[name]["button"].background = Global.button_normal_background_clour
    
    # Make selected work area visible and have Focus
    Global.work_area[work_area_name]["form"].visible = True
    Global.work_area[work_area_name]["button"].bold = True
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
    self.action_list.selected_value = None
    pass
  
  def action_list_change(self, **event_args):
    """This method is called when an item from the dropdown menu is selected"""
    # Action has been selected, but only take action if action in not a separator
    # save a link to the Main form in a Global variable 
    Global.main_form = get_open_form()
    #
    Global.action = self.action_list.selected_value
    if Global.action not in Global.action_list_not_implemented:
      # Action has been selected, create button in work area list, and make this work area in focus (highlight button)
      # for any action that has a Form defined create a new work_area
      if Global.site_id is None and Global.action not in (Global.admin_action_list + ["Select Site"]):
        # if site is not yet selected alert user
        alert(
        content="Site has not been selected. Please select a site.",
        title="Select Site",
        large=True,
        buttons=["Ok", True],
        )
      else:
        self.create_new_work_area(Global.action)
    else:
      if Global.action != Global.separator:
        alert("Action not yet implemented.")
    self.action_list.selected_value = None
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
      # when user is logged in, enable Action menu, username field and logout button, and disable content panel (welcome message)
      # also set username  to user email address
      Global.GlobalHeader.visible = True
      Global.username = user["email"]
      Global.user_role = user["role"]
      #Global.DBAcontrol = anvil.server.call("check_DBAcontrol",Global.username,"i")
      #self.username.text = Global.username + "\n (" + Global.user_role + ")"
      self.username.text = Global.username
      Global.ip_address = anvil.server.call("user_login_notification")
      # if users has admin role, add admin actions list and set it visible
      self.admin_action_list.visible = False
      if Global.user_role == "admin":
        print(Global.username, Global.user_role)
        self.admin_action_list.items = Global.admin_action_list
        self.admin_action_list.visible = True
      # make menu bar varianble visible
      self.action_list.items = Global.user_action_list
      self.action_list.visible = True
      self.logout_button.visible = True
      self.username.visible = True
      # make content_panel of Main form invisible
      self.content_panel.visible = False
      # once logged in, show "Select Site" form
      Global.action = "Select Site"
      self.create_new_work_area(Global.action)
    pass

  def logout_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    #logout user, hide action menu, username and logout button; also delete all workspaces
    anvil.server.call("user_logout_notification",Global.ip_address,Global.username)
    anvil.users.logout()
    self.content_panel.visible = True
    self.action_list.items = Global.user_action_list
    self.admin_action_list.visible = False
    self.action_list.visible = False
    self.logout_button.visible = False
    self.username.visible = False
    Global.GlobalHeader.visible = False
    #delete all work_areas and all work_area names/buttons
    temp_work_area_name_list = list(Global.work_area.keys())
    for work_area_name in temp_work_area_name_list:
      Function.delete_workspace(work_area_name)
    #components = self.get_components()
    #print(f"{len(components)} components after deleting all workspaces")
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
      self.username.text = Global.username
      self.action_list.visible = True
      self.logout_button.visible = True
      self.username.visible = True
      self.content_panel.visible = False
    pass

  def admin_action_list_change(self, **event_args):
    """This method is called when an item is selected"""
    # Action has been selected, but only take action if action in not a separator
    # save a link to the Main form in a Global variable 
    Global.main_form = get_open_form()
    #
    Global.admin_action = self.admin_action_list.selected_value
    if Global.admin_action in Global.admin_action_list:
      # Action has been selected, create button in work area list, and make this work area in focus (highlight button)
      # for any action that has a Form defined create a new work_area

      self.create_new_work_area(Global.admin_action)
    else:
      if Global.action != Global.separator:
        alert("Action not yet implemented.")
    self.action_list.selected_value = None
    pass
