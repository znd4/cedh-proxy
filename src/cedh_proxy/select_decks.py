from enum import Enum

import httpx
import more_itertools as mi
import typer
from pydantic import BaseModel, Field
from typing_extensions import Annotated

CEDH_DECKLIST_DATABASE_LIST = "https://raw.githubusercontent.com/AverageDragon/cEDH-Decklist-Database/master/_data/database.json"


class Commander(BaseModel):
    name: str
    image_url: str = Field(alias="link")


class Decklist(BaseModel):
    link: str
    title: str
    primer: bool


class Deck(BaseModel):
    name: str
    decklists: list[Decklist]
    commanders: list[Commander]
    url: str


class OutputFormat(str, Enum):
    csv = "csv"


# ruff: noqa: B008
def select_decks(
    ddb: bool = typer.Option(
        False,
        "--ddb",
        "--cedh-decklist-database",
        help="Use the cEDH Decklist Database as the source for decklists.",
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        "-l",
        help="Limit the number of decklists to view.\n"
        "Defaults to all when piped to a file, or paginates when displayed in a terminal.",
    ),
    format: Annotated[
        OutputFormat, typer.Option(case_sensitive=False, help="What output format should we use?")
    ] = OutputFormat.csv,
) -> int:
    """Select decks to proxy."""
    if ddb:
        databases = load_from_cedh_decklist_database()
    else:
        raise NotImplementedError("Have not implemented default deck sources yet.")

    if limit is not None:
        databases = mi.take(limit, databases)

    if format == OutputFormat.csv:
        raise NotImplementedError("Have not implemented CSV output yet.")
    else:
        raise NotImplementedError(f"Do not recognize output format {format}.")

    return 1


def load_from_cedh_decklist_database() -> list[Decklist]:
    response = httpx.get(CEDH_DECKLIST_DATABASE_LIST)
    response.raise_for_status()
    return [Decklist(**decklist) for decklist in response.json()]
