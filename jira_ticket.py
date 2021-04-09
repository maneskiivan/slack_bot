import requests
from requests.auth import HTTPBasicAuth
import json
import os


class Jira:

  def __init__(self):
    self.__jira_api_email = os.environ.get('JIRA_API_EMAIL')
    self.__jira_api_token = os.environ.get('JIRA_API_TOKEN')
    self.__headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
    self.__jira_acc_id = None
    self.__group_admin = None

  def get_user_id(self, username):
    url = f"https://gumgum.jira.com/rest/api/3/user/search?query={username}"
    auth = HTTPBasicAuth(self.__jira_api_email, self.__jira_api_token)
    

    response = requests.request(
      "GET",
      url,
      headers=self.__headers,
      auth=auth
    )

    response_dict = response.json()
    return response_dict[0]['accountId']

  def open_it_help(self, summary, description, username):
    url = "https://gumgum.jira.com/rest/api/2/issue"
    auth = HTTPBasicAuth(self.__jira_api_email, self.__jira_api_token)
    self.__jira_acc_id = self.get_user_id(username)
    payload = json.dumps(
      {
        'fields': {
          'project': {
            'id': '14900'
          },
          'issuetype': {
            'id': '10000'
          },
          'summary': summary,
          'description': description,
          'reporter': {
            'accountId': self.__jira_acc_id
          }
        }
      }
    )

    response = requests.request(
      "POST",
      url,
      data=payload,
      headers=self.__headers,
      auth=auth
    )

    response_str = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(',', ': '))
    response_dict = json.loads(response_str)

    return f"The following ticket was created: https://gumgum.jira.com/projects/ITS/board?issue-key={response_dict['key']}"

  def open_nml(self, summary, alias, purp_of_alias, group_admin, allow, members, username):
    url = "https://gumgum.jira.com/rest/api/2/issue"
    auth = HTTPBasicAuth(self.__jira_api_email, self.__jira_api_token)
    self.__jira_acc_id = self.get_user_id(username)
    self.__group_admin = self.get_user_id(group_admin)
    payload = json.dumps(
      {
        'fields': {
          'project': {
            'id': '14900'
          },
          'issuetype': {
            'id': '10602'
          },
          'summary': summary,
          'customfield_13515': alias,
          'customfield_13516': purp_of_alias,
          'customfield_13513': {
            'accountId': self.__group_admin
          },
          'customfield_13532': {
            'value': allow
          },
          'customfield_13514': members,
          'reporter': {
            'accountId': self.__jira_acc_id
          }
        }
      }
    )

    response = requests.request(
      "POST",
      url,
      data=payload,
      headers=self.__headers,
      auth=auth
    )

    response_str = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(',', ': '))
    response_dict = json.loads(response_str)

    return f"The following ticket was created: https://gumgum.jira.com/projects/ITS/board?issue-key={response_dict['key']}"

  def open_purchase(self, summary, description, username):
    url = "https://gumgum.jira.com/rest/api/2/issue"
    auth = HTTPBasicAuth(self.__jira_api_email, self.__jira_api_token)
    self.__jira_acc_id = self.get_user_id(username)
    payload = json.dumps(
      {
        'fields': {
          'project': {
            'id': '14900'
          },
          'issuetype': {
            'id': '10001'
          },
          'summary': summary,
          'description': description,
          'reporter': {
            'accountId': self.__jira_acc_id
          }
        }
      }
    )

    response = requests.request(
      "POST",
      url,
      data=payload,
      headers=self.__headers,
      auth=auth
    )

    response_str = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(',', ': '))
    response_dict = json.loads(response_str)

    return f"The following ticket was created: https://gumgum.jira.com/projects/ITS/board?issue-key={response_dict['key']}"

  def open_event(self, summary, description, date_time, event_location, hardware_needed, zoom_meeting, zoom_meeting_link, record_or_not, username):
    url = "https://gumgum.jira.com/rest/api/2/issue"
    auth = HTTPBasicAuth(self.__jira_api_email, self.__jira_api_token)
    self.__jira_acc_id = self.get_user_id(username)
    payload = json.dumps(
      {
        'fields': {
          'project': {
            'id': '14900'
          },
          'issuetype': {
            'id': '10604'
          },
          'summary': summary,
          'description': description,
          'customfield_13522': date_time,
          'customfield_13526': event_location,
          'customfield_13523': hardware_needed,
          'customfield_13530': {
            'value': zoom_meeting
          },
          'customfield_14013': zoom_meeting_link,
          'customfield_13529': {
            'value': record_or_not
          },
          'reporter': {
            'accountId': self.__jira_acc_id
          }
        }
      }
    )

    response = requests.request(
      "POST",
      url,
      data=payload,
      headers=self.__headers,
      auth=auth
    )

    response_str = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(',', ': '))
    response_dict = json.loads(response_str)

    return f"The following ticket was created: https://gumgum.jira.com/projects/ITS/board?issue-key={response_dict['key']}"