from ._anvil_designer import RowFormTemplate
from anvil import *
import anvil.server
import re
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras.Quill import Quill

from ..Validation import Validator
from .. import Global

class RowForm(RowFormTemplate):
  def input_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    column = event_args["sender"].placeholder
    if str(type(event_args["sender"])) == "<class 'anvil_extras.Quill.Quill'>":
      self.form_fields[column]["header"].text = column + " (" + str(len(self.form_fields[column]["field"].get_html())) + "/" + str(self.form_fields[column]["length"]) + "):"
    else:
      self.form_fields[column]["header"].text = column + " (" + str(len(self.form_fields[column]["field"].text)) + "/" + str(self.form_fields[column]["length"]) + "):"
  pass
  
  def __init__(self, site_id, table_name, data_list, action, page_info, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.site_id = site_id
    # Global.site_id is only None when form called from server side (e.g. printing form)
    if Global.site_id is None:
      # initialise some Globals variables for when the function is called from the server side
      Global.site_id = site_id
      Global.action = "View " + table_name.capitalize()
      Global.current_work_area_name = Global.action
      Global.table_name = table_name
      Global.work_area = {}
      Global.work_area[Global.current_work_area_name] = {}
      print(data_list)
      Global.work_area[Global.current_work_area_name]["data_list"] = data_list
    else:
      # set table_name to one of "context", "find", from the action Global variable
      Global.table_name = Global.action.split(" ")[1].rstrip("s").lower()

    self.validator = Validator()
    # we need to find out which table we are dealing with
    self.title.text = "This form is to " + Global.action
    # get table information
    table_info = anvil.server.call("describe_table",Global.table_name)
    # And then we need to create all the fields based on table information 
    # loop over table columns
    self.field_details = {}
    self.form_fields = {}
    #print(Global.table_items)
    #print(Global.work_area[Global.current_work_area_name]["data_list"])
    for item in table_info:
      column_name = item["Field"]
      column_type = item["Type"]
      # types can be varchar(length),int(length),text,float,double,date
      # type text can be 65535 char so need to be a TextArea, other can be a TextBox
      # create the label and the input field
      #lab = Label(text=column_name, font_size=14,placeholder=column_name)
      if column_type == "text":
        #create TextArea input field for text type
        #input = TextArea(tag=column_name)
        input = Quill(placeholder=column_name,toolbar=Global.Quill_toolbarOptions)
        max_length = 65535
        input.add_event_handler('text_change',self.input_change)
      elif column_type == "date":
        # by default create TextBox fields
        input = TextBox(placeholder=column_name)
        # date type is 10 long
        max_length = 10
        # add event handler for when input field is changed to update the character count
        input.add_event_handler('change',self.input_change)
      else:
        # by default create TextBox fields
        input = TextBox(placeholder=column_name)
        # extract length from type
        match = re.search(r'\d+',column_type)
        max_length = match.group()
        # add event handler for when input field is changed to update the character count
        input.add_event_handler('change',self.input_change)
        
      # if field is None make is "" (empty)
      #if Global.work_area[Global.current_work_area_name]["data_list"][column_name] is None:
      #  Global.work_area[Global.current_work_area_name]["data_list"][column_name] = ""
      #print(column_name, Global.work_area[Global.current_work_area_name]["data_list"][column_name])
      # set specific settings (like validators) for the various fields
      if column_name in ["SiteId"]:
        input.text = Global.site_id
        input.enabled = False
        input.foreground = "#ffffff"
      elif column_name in ["YearEnd","YearStart"]:
        self.validator.regex(component=input,
                           events=['lost_focus', 'change'],
                           pattern="^-?\d{1,4}(?:BC|AD)?$",
                           required=False,
                           message="Please enter a valid year YYYY BC|AD (or -YYYY for BC year)")
      elif column_name in ["Year"]:   
        self.validator.regex(component=input,
                                       events=['lost_focus', 'change'],
                                       pattern="^\d{4}$",
                                       required=True,
                                       message="Please enter a valid year in YYYY format")
      # end of validation 
      
      # if action is View or Edit then fill all fields
      cur_len = 0
      if Global.action in ["Edit Context","Edit Find","View Context","View Find"]:
        if str(type(input)) == "<class 'anvil_extras.Quill.Quill'>":
          html_text = Global.work_area[Global.current_work_area_name]["data_list"][0][column_name]
          delta = input.clipboard.convert(html_text)
          input.setContents(delta, 'silent')
          cur_len = 0
          if html_text is not None:
            cur_len = len(html_text)
        else:
          input.text = Global.work_area[Global.current_work_area_name]["data_list"][0][column_name]
          cur_len = 0
          if input.text is not None:
            cur_len = len(input.text)
          
      # set default label text
      col = column_name + " (" + str(cur_len) + "/" + str(max_length) + ")" 
      lab = Label(text=col,font_size=14,tag=column_name)
      # add columns details to nested dictionary
      field_details = {"header": lab, "field": input, "length": max_length}
      self.form_fields[column_name] = field_details
      # add label and imput field to column_panel
      self.column_panel_1.add_component(lab)
      self.column_panel_1.add_component(input)
    #
    if Global.action in ["Edit Context","Edit Find","Add Context","Add Find"]:
      # Add a Submit button if Edit or Add action
      submit_btn = Button(text="Submit")
      submit_btn.add_event_handler("click",self.submit_btn_click)
      self.column_panel_1.add_component(submit_btn)

    # For this form the page_info details are all set to 0; this is for when the server print function call the form
    Global.work_area[Global.current_work_area_name]["page_info"] = {"page_num": 0, "rows_per_page": 0, "total_rows": 0}


  def submit_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    for col in self.form_fields.items():
      if str(type(col[1]["field"])) == "<class 'anvil_extras.Quill.Quill'>":
        print(col[0],col[1]["field"].get_html())
      else:
        print(col[0],col[1]["field"].text)
    pass

  def submit_button_click(self, **evemt_args):
    if self.validator.are_all_valid():
      # All fields are filled in correct (I think)
      # collect context form details and then call anvil.server add_context
      Global.context_items["ContextId"] = self.ContextId.text
      Global.context_items["SiteId"] = self.SiteId.text
      Global.context_items["Name"] = self.Name.text
      Global.context_items["Year"] = self.Year.text
      #Global.context_items["AreaId"] = self.AreaId.selected_value
      Global.context_items["AreaId"] = self.AreaId.text
      Global.context_items["RecordStatus"] = self.RecordStatus.text
      Global.context_items["FillOf"] = self.FillOfFindId.text
      Global.context_items["ContextType"] = self.ContextType.selected_value
      Global.context_items["Description"] = self.Description.text
      Global.context_items["Interpretation"] = self.Interpretation.text
      Global.context_items["DatesAssignedBy"] = self.DatesAssignedBy.text
      Global.context_items["YearStart"] = self.YearStart.text
      Global.context_items["YearEnd"] = self.YearEnd.text
      #
      if (self.ContextType.selected_value) is not None:
        # call server for database update
        # set all empty fields to None (will be Null in DB)
        for x in Global.context_items:
          if Global.context_items[x] == "":
            Global.context_items[x] = None
        msg = "This message text should not be seen. Global.action = " + Global.action
        #print(Global.action)
        if Global.work_area[Global.current_work_area_name]["action"] == "Add Context":
          ret = anvil.server.call("context_add",Global.context_items)
          # if success then goto list contexts
          if ret[:2] == "OK":
            msg = "The context has been successfully inserted to the database."
          else:
            msg = "The context has not been inserted to the database, because of " + ret
        elif Global.work_area[Global.current_work_area_name]["action"] == "Edit Context":
          ret = anvil.server.call("context_update",Global.context_items)
          # if success then goto list contexts
          if ret[:2] == "OK":
            msg = "The context has been successfully updated in the database."
          else:
            msg = "The context has not been updated in the database, because of " + ret
        alert(content=msg)
      else:
        alert("Please select a value for Contect Type and/or Area ID.")
    else:
      alert("Please correct the field(s) with errors before submitting.")
    pass