from dataclasses import dataclass


@dataclass
class Opportunity:
    opportunity_territory_name: str
    parent_account_id: str
    parent_account: str  # can be emptry str
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
                'Opportunity Territory Name', ''),
            parent_account_id=data.get(
                'Parent Account ID', ''),
            parent_account=data.get(
                'Parent Account', ''),
            account_id=data.get(
                'Account ID', ''),
            account_name=data.get(
                'Account Name', ''),
            fiscal_period=data.get(
                'Fiscal Period', ''),
            opportunity_id=data.get(
                'Opportunity ID', ''),
            opportunity_name=data.get(
                'Opportunity Name', ''),
            opportunity_owner=data.get(
                'Opportunity Owner', ''),
            close_date=data.get(
                'Close Date', ''),
            stage=data.get(
                'Stage', ''),
            amount_converted=data.get(
                'Amount (converted)', ''),
            acv_opportunity_converted=data.get(
                'ACV Opportunity (converted)', '')
        )

    def __post_init__(self):
        def validate_not_empty_or_invalid(attribute_name, value):
            invalid_values = ["", " ", "-", " - "]
            if value in invalid_values:
                raise ValueError(
                    f"The attribute '{attribute_name}' is invalid.")

        # Validate specific attributes
        validate_not_empty_or_invalid(
            "opportunity_territory_name", self.opportunity_territory_name)
        validate_not_empty_or_invalid(
            "account_id", self.account_id)
        validate_not_empty_or_invalid(
            "opportunity_id", self.opportunity_id)
        validate_not_empty_or_invalid(
            "opportunity_name", self.opportunity_name)
        validate_not_empty_or_invalid(
            "opportunity_owner", self.opportunity_owner)
        validate_not_empty_or_invalid(
            "close_date", self.close_date)
        validate_not_empty_or_invalid(
            "stage", self.stage)
        validate_not_empty_or_invalid(
            "amount_converted", self.amount_converted)
        validate_not_empty_or_invalid(
            "acv_opportunity_converted", self.acv_opportunity_converted)

    def __str__(self):
        return (
            f"--------------------\n"
            f"Opportunity Details:\n"
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
