from typing import Optional
from dataclasses import dataclass


@dataclass
class Task:
    date: str
    account_name: str
    account_id: str
    related_to_opportunity: Optional[str]
    related_to_opportunity_id: Optional[str]
    related_to_contact: Optional[str]
    related_to_contact_id: Optional[str]
    related_to: Optional[str]
    related_to_id: Optional[str]
    assigned_name: str
    assigned_id: str
    priority: str
    comments: str
    status: str
    completed_dt: Optional[str]
    last_modified_date: str
    last_modified_name: str
    last_modified_id: str
    created_date: str
    created_by_name: str
    created_by_id: str

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            date = data.get('Date'),
            account_name = data.get('Company / Account'),
            account_id = data.get('Company / Account ID', ''),
            related_to_opportunity = data.get('Opportunity', None),
            related_to_opportunity_id = data.get('Opportunity ID', None),
            related_to_contact = data.get('Contact', None),
            related_to_contact_id = data.get('Contact ID', None),
            related_to = data.get('Related To', None),
            related_to_id = data.get('Related To ID', None),
            assigned_name= data.get('Assigned'),
            assigned_id= data.get('Assigned ID', ''),
            priority= data.get('Priority'),
            comments= data.get('Full Comments'),
            status= data.get('Status'),
            completed_dt= data.get('Completed Date/Time', None),
            last_modified_date= data.get('Last Modified Date'),
            last_modified_name= data.get('Last Modified By'),
            last_modified_id= data.get('Last Modified By ID', ''), #todo
            created_date= data.get('Created Date'),
            created_by_name= data.get('Created By'),
            created_by_id= data.get('Created By ID', '') #todo
        )
    
    def __post_init__(self):
        def validate_not_empty_or_invalid(attribute_name, value):
            invalid_values = ["", " ", "-", " - "]
            if value in invalid_values:
                raise ValueError(
                    f"The attribute '{attribute_name}' is invalid.")

        # Validate specific attributes
        #todo

    def __str__(self):
        return (
            f"--------------------\n"
            f"Task:\n"
            f"  Account: {self.account_name} (ID: {self.account_id}) \n"
            f"  Related Opportunity: {self.related_to_opportunity} (ID: {self.related_to_opportunity_id}) \n"
            f"  Related Contact: {self.related_to_contact} (ID: {self.related_to_contact_id}) \n"
            f"  Related To: {self.related_to} (ID: {self.related_to_id}) \n"
            f"  Assigned: {self.assigned_name} (ID: {self.assigned_id}) \n"
            f"  Priority: {self.priority} \n"
            f"  Status: {self.status}\n"
            f"  Completed: {self.completed_dt} \n"
            f"  Last Modified: {self.last_modified_date} by {self.last_modified_name} (ID: {self.last_modified_id}) \n"
            f"  Created: {self.created_date} by {self.created_by_name} (ID: {self.created_by_id}) \n"
            f"  Comments: {self.comments} \n"
            f"--------------------\n")