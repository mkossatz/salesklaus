from typing import Optional
from dataclasses import dataclass


@dataclass
class Opportunity:
    opportunity_territory_name: str
    parent_account_id: Optional[str]
    parent_account: Optional[str]
    account_id: str
    account_name: str
    fiscal_period: str
    opportunity_id: str
    opportunity_name: str
    opportunity_owner: str
    close_date: str
    stage: str
    amount_converted: str
    acv_opportunity_converted: str

    @classmethod
    def from_dict(cls, data: dict) -> "Opportunity":
        return cls(
            opportunity_territory_name=data.get(
                'Opportunity Territory Name'),
            parent_account_id=data.get(
                'Parent Account ID', ''),
            parent_account=data.get(
                'Parent Account', ''),
            account_id=data.get(
                'Account ID'),
            account_name=data.get(
                'Account Name'),
            fiscal_period=data.get(
                'Fiscal Period'),
            opportunity_id=data.get(
                'Opportunity ID'),
            opportunity_name=data.get(
                'Opportunity Name'),
            opportunity_owner=data.get(
                'Opportunity Owner'),
            close_date=data.get(
                'Close Date'),
            stage=data.get(
                'Stage'),
            amount_converted=data.get(
                'Amount (converted)'),
            acv_opportunity_converted=data.get(
                'ACV Opportunity (converted)')
        )

    def __post_init__(self):
        # Loop through all fields in the dataclass
        for field_name, field_value in self.__dict__.items():
            # Check the type hint of the field
            field_type = self.__annotations__[field_name]
            # If the field is not Optional and is None, raise an error
            if field_value is None and not (field_type is Optional[str]):
                raise ValueError(f"The field '{field_name}' cannot be None because it is not optional.")

    def __str__(self):
        return (
            f"--------------------\n"
            f"Opportunity:\n"
            f"  Territory: {self.opportunity_territory_name}\n"
            f"  Account: {self.account_name} (ID: {self.account_id})\n"
            f"  Parent Account: {self.parent_account} (ID: {self.parent_account_id})\n"
            f"  Opportunity: {self.opportunity_name} (ID: {self.opportunity_id})\n"
            f"  Opportunity Owner: {self.opportunity_owner}\n"
            f"  Fiscal Period: {self.fiscal_period}\n"
            f"  Close Date: {self.close_date}\n"
            f"  Stage: {self.stage}\n"
            f"  Amount (Converted): {self.amount_converted}\n"
            f"  ACV (Converted): {self.acv_opportunity_converted}\n"
            f"--------------------\n")
