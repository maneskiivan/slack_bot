from slack_bolt import App
from datetime import date
import json
from jira_ticket import Jira
import os
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
import logging

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SIGNING_SECRET"),
    process_before_response=True
)


# open the initial modal when the command is called
@app.command("/ithelp")
def open_modal(ack, client, body):
  # Acknowledge command request
  ack()

  with open('it_support_modal.json') as file:
    it_support_modal = json.load(file)

  client.views_open(
    # Pass a valid trigger_id within 3 seconds of receiving it
    trigger_id=body["trigger_id"],
    # View payload
    view=it_support_modal
  )

  @app.action('button-action')
  def update_modal(ack):
    ack()

# update the modal when an issue type is selected
@app.action("static_select-action")
def update_modal(ack, body, client):
  view_id = body['container']['view_id']
  # Retrieving the issue type selection
  selection = body['view']['state']['values']
  for v in selection.values():
    selection = v['static_select-action']['selected_option']['text']['text']
  # Acknowledge issue type selection request
  ack()

  if selection == 'IT Help':
    with open('it_help_modal.json') as file:
      it_help_modal = json.load(file)
    client.views_update(
      view_id=view_id,
      view=it_help_modal
    )
  elif selection == 'New Mailing List':
    with open('nml_modal.json') as file:
      nml_modal = json.load(file)
    client.views_update(
      view_id=view_id,
      view=nml_modal
    )
    #handling action requests caused by the updated modals
    @app.action('static_select-action')
    def update_modal(ack):
      ack()
    @app.action('users_select-action')
    def update_modal(ack):
      ack()
  elif selection == 'Purchase':
    with open('purchase_modal.json') as file:
      purchase_modal = json.load(file)
    client.views_update(
      view_id=view_id,
      view=purchase_modal
    )
  elif selection == 'Event Set-Up':
    with open('event_modal.json') as file:
      event_modal = json.load(file)
    # adding today's date to the dict from the modal
    today = date.today()
    date_time = today.strftime("%Y-%m-%d")
    temp_list = event_modal['blocks']
    temp_list[1]['accessory']['initial_date'] = date_time
    event_modal['blocks'] = temp_list
    client.views_update(
      view_id=view_id,
      view=event_modal
    )
    #handling action requests caused by the updated modals
    @app.action('datepicker-action')
    def update_modal(ack):
      ack()
    @app.action('timepicker-action')
    def update_modal(ack):
      ack()
    @app.action('static_select-action')
    def update_modal(ack):
      ack()
    @app.action('checkboxes-action')
    def update_modal(ack):
      ack()

# handle the it help submission and respond to the end user
@app.view('it_help')
def handle_it_help(ack, body, client, view):
  user = body["user"]['id']
  username = body["user"]['username']
  values_input = view['state']['values']
  values_input_list = []
  for v in values_input.values():
    values_input_list.append(v['plain_text_input-action']['value'])
  summary = values_input_list[0]
  description = values_input_list[1]
  # Acknowledge the view_submission event and close the modal
  ack()
  # Open the ticket in Jira
  new_ticket = Jira()
  msg = new_ticket.open_it_help(summary, description, username)
  client.chat_postMessage(channel=user, text=msg)

# handle the nml submission and respond to the end user
@app.view('nml')
def handle_nml(ack, body, client, view):
  user = body["user"]['id']
  username = body["user"]['username']
  values_input = view['state']['values']
  values_input_list = []
  group_admin_id = None
  for v in values_input.values():
    for k, v1 in v.items():
      if k == 'plain_text_input-action':
        values_input_list.append(v['plain_text_input-action']['value'])
      elif k == 'static_select-action':
        values_input_list.append(v['static_select-action']['selected_option']['text']['text'])
      elif k == 'users_select-action':
        group_admin_id = v['users_select-action']['selected_user']
  summary = values_input_list[0]
  alias = values_input_list[1]
  purp_of_alias = values_input_list[2]
  group_admin = client.users_info(
        user=group_admin_id
    )
  group_admin = group_admin['user']['name']
  allow = values_input_list[3]
  members = values_input_list[4]

  # Acknowledge the view_submission event and close the modal
  ack()
  # Open the ticket in Jira
  new_ticket = Jira()
  msg = new_ticket.open_nml(summary, alias, purp_of_alias, group_admin, allow, members, username)
  client.chat_postMessage(channel=user, text=msg)

# handle the purchase submission and respond to the end user
@app.view('purchase')
def handle_purchase(ack, body, client, view):
  user = body["user"]['id']
  username = body["user"]['username']
  values_input = view['state']['values']
  values_input_list = []
  for v in values_input.values():
    values_input_list.append(v['plain_text_input-action']['value'])
  summary = values_input_list[0]
  description = values_input_list[1]
  # Acknowledge the view_submission event and close the modal
  ack()
  # Open the ticket in Jira
  new_ticket = Jira()
  msg = new_ticket.open_purchase(summary, description, username)
  client.chat_postMessage(channel=user, text=msg)

# handle the event submission and respond to the end user
@app.view('event')
def handle_purchase(ack, body, client, view):
  user = body["user"]['id']
  username = body["user"]['username']
  values_input = view['state']['values']
  values_input_list = []
  for v in values_input.values():
    for k, v1 in v.items():
      if k == 'plain_text_input-action':
        values_input_list.append(v['plain_text_input-action']['value'])
      elif k == 'datepicker-action':
        values_input_list.append(v['datepicker-action']['selected_date'])
      elif k == 'timepicker-action':
        values_input_list.append(v['timepicker-action']['selected_time'])
      elif k == 'checkboxes-action':
        values_input_list.append(v['checkboxes-action']['selected_options'])
      elif k == 'static_select-action':
        values_input_list.append(v['static_select-action']['selected_option']['text']['text'])
  summary = values_input_list[0]
  date_time = f"{values_input_list[1]}T{values_input_list[2]}:00.000-0700"
  event_location = values_input_list[3]
  hardware_needed = []
  for check in values_input_list[4]:
    hardware_needed_dict = {
      'value': check['text']['text']
    }
    hardware_needed.append(hardware_needed_dict)
  zoom_meeting = values_input_list[5]
  zoom_meeting_link = values_input_list[6]
  record_or_not = values_input_list[7]
  description = values_input_list[8]

  # Acknowledge the view_submission event and close the modal
  ack()

  # Open the ticket in Jira
  new_ticket = Jira()
  msg = new_ticket.open_event(summary, description, date_time, event_location, hardware_needed, zoom_meeting,
                              zoom_meeting_link, record_or_not, username)
  client.chat_postMessage(channel=user, text=msg)

# Acknowledge the end user opening the home app
@app.event("app_home_opened")
def update_home_tab(ack):
  ack()


SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)