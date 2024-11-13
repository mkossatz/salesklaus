import click
from salesklaus.report_crawling import deserialize_report, SFSessionIDs
from salesklaus.models.opportunity import Opportunity

#todo: create CLI options for saving session data to remove hard-coding
sf_session_ids = SFSessionIDs(
    sid="xxx", 
    sid_Client="xxx")


@click.group()
def cli():
    """CLI for interacting with Salesforce reports."""
    pass


@cli.command()
@click.option('--url', default=None, help="Custom URL of the report to crawl.")
def crawl_report(url):
    """
    Crawl a Salesforce report using a provided or default URL.
    """
    if not url:
        click.echo("You must provide a URL for the report.")
        return

    click.echo(f"Crawling report from URL: \n{url}\n")

    report_entries = deserialize_report(
        report_url=url,
        sf_session_ids=sf_session_ids
    )
    for entry in report_entries:
        click.echo("--------------------")
        click.echo(entry)
        click.echo("--------------------")
    num_entries = len(report_entries)
    print(f"\nFound {num_entries} report entries.\n")


@cli.command()
@click.option('--url', default=None, help="Custom URL of the Opportunity report to crawl.")
def crawl_opportunities(url):
    """
    Crawl an Opportunity report using a provided or default URL.
    """
    report_url = url or "https://redhatcrm.lightning.force.com/lightning/r/Report/00O6e000009fYYdEAM/view"
    click.echo(f"Crawling Opportunity report from URL: \n{report_url}\n")
    opportunities = list()

    report_entries = deserialize_report(
        report_url=report_url,
        sf_session_ids=sf_session_ids
    )
    for entry in report_entries:
        try:
            opportunity = Opportunity.from_dict(entry)
        except ValueError as ve:
            pass
        else:
            opportunities.append(opportunity)
            click.echo(opportunity)

    num_opps = len(opportunities)
    print(f"\nFound {num_opps} opportunities.\n")


if __name__ == '__main__':
    cli()
