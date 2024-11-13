from typing import Optional
from dataclasses import dataclass


@dataclass
class Account:
    uuid: str # 18-digit ID
    account_name: str
    account_id: str
    parent_account: Optional[str]
    parent_account_id: Optional[str]
    billing_city: Optional[str]
    billing_state: Optional[str]
    last_modified_date: str
    last_activity_date: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> "Account":
        return cls(
            uuid=data.get(
                '18-digit ID'),
            account_name=data.get(
                'Account Name'),
            account_id=data.get(
                'Account ID'),
            parent_account_id=data.get(
                'Parent Account ID', ''),
            parent_account=data.get(
                'Parent Account', ''),
            billing_city=data.get(
                'Billing City'),
            billing_state=data.get(
                'Billing State/Province (text only)'),
            last_modified_date=data.get(
                'Last Modified Date'),
            last_activity_date=data.get(
                'Last Activity')
            )
    def __post_init__(self):
        # Loop through all fields in the dataclass
        for field_name, field_value in self.__dict__.items():
            # Check the type hint of the field
            field_type = self.__annotations__[field_name]
            # If the field is not Optional and is None, raise an error
            if field_value is None and not (field_type is Optional[str]):
                #todo: log this as warning
                raise ValueError(f"The field '{field_name}' cannot be None because it is not optional.")
    
    def __str__(self):
        return (
            f"--------------------\n"
            f"Account:\n"
            f"  uuid: {self.uuid}\n"
            f"  Account ID: {self.account_id} \n"
            f"  Account Name: {self.account_name} \n"
            f"  Parent Account: {self.parent_account} (ID: {self.parent_account_id})\n"
            f"  Billing Address: {self.billing_city}, {self.billing_state} \n"
            f"  Last Modified: {self.last_modified_date} \n"
            f"  Last Activity: {self.last_activity_date}\n"
            f"--------------------\n")