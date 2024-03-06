#   Copyright [2024] [GustavoSchip]
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from os.path import exists
from pathlib import Path as PLPath
from sys import argv, exit
from typing import Literal

from click import Path, command, echo, open_file, option, style
from flask import Flask
from server import invoke_server
from yaml import safe_load

app_handler = Flask("Gustav-Engine")
VERSION = "v0.0.1"


@command()
@option("--verbose", "-v", is_flag=True, help="Enable verbose logging.")
@option("--address", "-a", default="127.0.0.1", type=str, show_default=True, help="Specify the host address.")
@option("--port", "-p", default=80, type=int, show_default=True, help="Specify the host port.")
@option(
    "--config",
    "-p",
    default="config.yml",
    type=Path(exists=True, readable=True, file_okay=True, dir_okay=False, resolve_path=True, path_type=PLPath),
    help="Specify the config file.",
)
def cli(verbose: Literal[False] | Literal[True], address: str, port: int, config: PLPath) -> None:
    """Gustav-Engine

    Attempt at a DnD 5e Character builder inspired by Aurora Builder.
    """
    echo(style(text="Gustav-Engine: Running version '{VERSION}' on {system()} {version()}.\n", fg="magenta"))
    if verbose:
        echo(style(text="Warning: Verbose logging enabled!", fg="yellow"))
    if exists(str(config)):
        with open_file(str(config)) as f:
            config = safe_load(f.read())
    else:
        echo(style(text="No config file found! Exiting...", fg="red"))
        exit(1)

    if verbose:
        echo(style(text="Verbose: Invoking server...", fg="cyan"))
    invoke_server(
        verbose=verbose,
        address=address,
        port=port,
        config=config,  # type: ignore[arg-type]
        app_handler=app_handler,
    )
    return


if __name__ == "__main__":  # pragma: no cover
    if len(argv) == 1:
        cli.main(["--help"])
    else:
        cli()