import os
from datetime import datetime
import json
import click
from salesklaus import report_crawling
from salesklaus.models.opportunity import Opportunity
from salesklaus.models.task import Task
from salesklaus.models.account import Account

SF_SID_FILE = ".sf_session"

def _load_sf_sid()->str:
    if not os.path.exists(SF_SID_FILE):
        click.echo("Error: You are not logged in to Sales Force in this CLI.\n")
        exit(1)
    with open(SF_SID_FILE, 'r') as file:
        sf_sid = file.read()
        if not report_crawling.is_logged_in(sf_sid):
            click.echo("Error: Your Sales Force session has expired. Please log in again in this CLI.\n")
            exit(1)
        return sf_sid

@click.group()
def cli():
    """CLI for interacting with Salesforce reports."""
    pass

@cli.command()
def login():
    """
    Prompt the user to securely input the redhatcrm.my.salesforce.com sid and sid_Client.
    """
    sf_sid = click.prompt("Enter redhatcrm.my.salesforce.com sid", hide_input=True)
    if report_crawling.is_logged_in(sf_sid):
        with open(SF_SID_FILE, 'w') as file:
            file.write(sf_sid)
        click.echo(f"You are logged in to Salesforce (session data stored in .sf_session.json file)")

@cli.command()
def logout():
    """
    Logout by deleting the local .sf_session.json file if it exists.
    """
    if os.path.exists(SF_SID_FILE):
        os.remove(SF_SID_FILE)
        click.echo("Successfully logged out. The session file has been deleted.")
    else:
        click.echo("No session file found. You are already logged out.")


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

    report_entries = report_crawling.deserialize_report_from_url(
        report_url=url,
        sf_sid=_load_sf_sid()
    )
    for entry in report_entries:
        click.echo("--------------------")
        click.echo(entry)
        click.echo("--------------------")
    num_entries = len(report_entries)
    print(f"\nFound {num_entries} Entries.\n")


@cli.command()
@click.option('--url', default=None, help="Custom URL of the report to crawl.")
@click.option('--output',
              type=click.Choice(['html', 'json'], 
              case_sensitive=False))
def download_report(url, output):
    """
    Download a Salesforce report using a provided or default URL.
    """
    if not url:
        click.echo("You must provide a URL for the report.")
        return

    click.echo(f"Crawling report from URL: \n{url}\n")

    REPORT_FILE_NAME = "./downloaded_reports/report-"+str(datetime.now().strftime("%y-%m-%d-%H-%M-%S"))

    if output == "html":
        html = str(report_crawling._table_soup_from_report(
            report_url=url,
            sf_sid=_load_sf_sid()))
        with open(REPORT_FILE_NAME+".html", "w") as file:
            file.write(html)
        print(f"Saved the report to {REPORT_FILE_NAME}.html\n")
    if output == "json":
        report_entries = report_crawling.deserialize_report_from_url(
            report_url=url,
            sf_sid=_load_sf_sid()
        )
        json_content = json.dumps(report_entries)
        with open(REPORT_FILE_NAME+".json", "w") as file:
            file.write(json_content)
        print(f"Saved the report to {REPORT_FILE_NAME}.json\n")


@cli.command()
@click.option('--url', default=None, help="Custom URL of the Opportunity report to crawl.")
def crawl_opportunities(url):
    """
    Crawl an Opportunities report using a provided or default URL.
    """
    report_url = url or "https://redhatcrm.lightning.force.com/lightning/r/Report/00O6e000009fYYdEAM/view"
    click.echo(f"Crawling Opportunities report from URL: \n{report_url}\n")
    opportunities = list()

    report_entries = report_crawling.deserialize_report_from_url(
        report_url=report_url,
        sf_sid=_load_sf_sid()
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
    print(f"Found {num_opps} Opportunities.\n")

@cli.command()
@click.option('--html_file', default=None, help="Custom html file of the Tasks report to crawl.")
def load_tasks(html_file):
    click.echo(f"Loading Tasks report from html file: \n{html_file}\n")
    tasks = list()
    report_entries = report_crawling.deserialize_report_from_html_file(
        file_name=html_file)
    for entry in report_entries:
        try:
            task = Task.from_dict(entry)
        except ValueError as ve:
            pass
        else:
            tasks.append(task)
            click.echo(task)

    num_opps = len(tasks)
    print(f"Loaded {num_opps} Tasks.\n")




@cli.command()
@click.option('--url', default=None, help="Custom URL of the Tasks report to crawl.")
def crawl_tasks(url):
    """
    Crawl an Tasks report using a provided or default URL.
    """
    report_url = url or "https://redhatcrm.lightning.force.com/lightning/r/Report/00O6e000009fYtbEAE/view"
    click.echo(f"Crawling Tasks report from URL: \n{report_url}\n")
    tasks = list()
    report_entries = report_crawling.deserialize_report_from_url(
        report_url=report_url,
        sf_sid=_load_sf_sid()
    )
    for entry in report_entries:
        try:
            task = Task.from_dict(entry)
        except ValueError as ve:
            pass
        else:
            tasks.append(task)
            click.echo(task)

    num_opps = len(tasks)
    print(f"Found {num_opps} Tasks.\n")


@cli.command()
@click.option('--url', default=None, help="Custom URL of the Accounts report to crawl.")
def crawl_accounts(url):
    """
    Crawl an Accounts report using a provided or default URL.
    """
    report_url = url or "https://redhatcrm.lightning.force.com/lightning/r/Report/00O6e000009fZ2xEAE/view"
    click.echo(f"Crawling Accounts report from URL: \n{report_url}\n")
    accounts = list()
    report_entries = report_crawling.deserialize_report_from_url(
        report_url=report_url,
        sf_sid=_load_sf_sid()
    )
    for entry in report_entries:
        try:
            account = Account.from_dict(entry)
        except ValueError as ve:
            pass
        else:
            accounts.append(account)
            # click.echo(account)

    num_opps = len(accounts)
    print(f"Found {num_opps} Accounts.\n")





if __name__ == '__main__':
    cli()