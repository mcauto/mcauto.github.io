class ProjectBuilder(Builder):
	def build(self):
		json = {
			'type': 'project builder'
		}
		self.crud = {
			'project_created': self.create,
			'project_updated': self.update,
			'project_deleted': self.delete
		}
		func = self.crud[self.event.webhookEvent]
		result = json if func == None else func()
		return result

	def create(self):
		e = self.event
		create_json = {
			'rson': {
				'project': {
					'name': e.proj_name,
					'identifier': e.proj_key,
					'description': '',
          'custom_fields': [
              {
                  'name': 'jira::project_id',
                        'value': e.proj_id,
                  'id': 3
              }
          ]
				},
				'type': 'POST'
			}
		}
		return create_json

	def update(self):
		e = self.event
		update_json = {
			'rson': {
				'project': {
					'name': e.proj_name,
					'identifier': e.proj_key,
					'description': '',
					'custom_fields': [
						{
							'name': 'jira::project_id',
							'value': e.proj_id,
							'id': 3
						}
					]
				},
				'type': 'PUT'
			}
		}
		return update_json

	def delete(self):
		e = self.event
		delete_json = {
			'rson': {
				'project': {
					'identifier': e.proj_key,
					'description': '',
					'custom_fields': [
						{
							'name': 'jira::project_id',
							'value': e.proj_id,
							'id': 3
						}
					]
				},
				'type': 'DELETE'
			}
		}
		return delete_json


class IssueBuilder(Builder):
	def build(self):
		json = {
			'type': 'issue builder'
		}
		self.crud = {
			'jira:issue_created': self.create,
			'jira:issue_updated': self.update,
			'jira:issue_deleted': self.delete
		}
		func = self.crud[self.event.webhookEvent]
		result = json if func == None else func()
		return result

	def create(self):
		e = self.event
		create_json = {
			'rson': {
				'issue': {
					'id': e.issue_id,
					'project_id': e.issue_proj_key,
					'priority_id': e.issue_priority,
					'status_id': 1,
					'subject': e.issue_summary,
					'description': e.issue_description,
					'assigned_to_id': 1,
          'custom_fields': [
              {
                  'name': 'jira::issue_id',
                        'value': e.issue_id,
                  'id': 4
              }
          ]
				},
				'type': 'POST'
			}
		}
		return create_json

	def update(self):
		e = self.event
		status = 2
		print(e.changelog.get('items'))
		if e.changelog.get('items') is not None:
			item = e.changelog.get('items').pop()
			status = int(item.get('to'))
			if status == 10002:
				status = 3
			elif status == 10001:
				status = 5
			else:
				status = 2
		e.issue_priority = 6 - int(e.issue_priority)
		update_json = {
			'rson': {
				'issue': {
					'id': e.issue_id,
					'project_id': e.issue_proj_key,
					'priority_id': (e.issue_priority),
					'status_id': status,
					'subject': e.issue_summary,
					'description': e.issue_description,
					'assigned_to_id': 1,
					'custom_fields': [
						{
							'name': 'jira::issue_id',
							'value': e.issue_id,
							'id': 4
						}
					]
				},
				'type': 'PUT'
			}
		}
		return update_json

	def delete(self):
		e = self.event
		delete_json = {
			'rson': {
				'issue': {
					'id': e.issue_id,
					'custom_fields': [
						{
							'name': 'jira::issue_id',
							'value': e.issue_id,
							'id': 4
						}
					]
				},
				'type': 'DELETE'
			}
		}
		return delete_json


class CommentBuilder(Builder):
	def build(self):
		json = {
			'type': 'comment builder'
		}
		self.crud = {
			'comment_created': self.create,
			'comment_updated': self.update,
			'comment_deleted': self.delete
		}
		func = self.crud[self.event.webhookEvent]
		result = json if func == None else func()
		return result

	def create(self):
		create_json = {
			'rson': {
				'issue': {
					'project_id': '',
					'priority_id': '',
					'status_id': '',
					'subject': '',
					'description': '',
					'assigned_to_id': '',
				},
				'type': 'POST'
			}
		}
		return 'comment create'

	def update(self):
		update_json = {
			'rson': {
				'issue': {
					'project_id': '',
					'priority_id': '',
					'status_id': '',
					'subject': '',
					'description': '',
					'assigned_to_id': '',
				},
				'type': 'PUT'
			}
		}
		return 'comment update'

	def delete(self):
		delete_json = {
			'rson': {
				'issue': {
					'project_id': '',
					'priority_id': '',
					'status_id': '',
					'subject': '',
					'description': '',
					'assigned_to_id': '',
				},
				'type': 'DELETE'
			}
		}
		return 'comment delete'
