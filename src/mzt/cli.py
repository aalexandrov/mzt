# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

from typing import Any, IO, Optional
import click


# Click CLI Application
# ---------------------


@click.group()
@click.option("--debug", is_flag=True, default=False)
def command(debug: bool) -> None:
    if debug:
        import logging

        logging.basicConfig(
            encoding="utf-8",
            level=logging.DEBUG,
            format=r"- %(asctime)s %(levelname)s %(message)s",
            datefmt=r"%m/%d/%Y %I:%M:%S %p",
        )


# Base Options & Args
# -------------------


class BaseOpt:
    DB_PORT = dict(
        default=6875,
        help="DB connection port.",
        envvar="MZT_DB_PORT",
    )

    DB_HOST = dict(
        default="localhost",
        help="DB connection host.",
        envvar="MZT_DB_HOST",
    )

    DB_NAME = dict(
        default="materialize",
        help="DB connection database.",
        envvar="MZT_DB_NAME",
    )

    DB_USER = dict(
        default="materialize",
        help="DB connection user.",
        envvar="MZT_DB_USER",
    )

    DB_PASS = dict(
        default=None,
        help="DB connection password.",
        envvar="MZT_DB_PASS",
    )

    DB_REQUIRE_SSL = dict(
        is_flag=True,
        help="DB connection requires SSL.",
        envvar="MZT_DB_REQUIRE_SSL",
    )


# Utility methods
# ---------------


def is_documented_by(original: Any) -> Any:
    def wrapper(target):
        target.__doc__ = original.__doc__
        return target

    return wrapper


def info(msg: str, fg: str = "green", file: Optional[IO] = None) -> None:
    click.secho(msg, fg=fg, file=file)


def err(msg: str, fg: str = "red", file: Optional[IO] = None) -> None:
    click.secho(msg, fg=fg, err=True, file=file)


class MztException(click.ClickException):
    def show(self, file: Optional[IO] = None) -> None:
        err(f"Error: {self.format_message()}", file=file)
