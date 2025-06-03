import traceback

import click

from git_export import PathSpec


def main(filename: str) -> int:
    """prints all files which are matched by the given pathspec file."""

    spec = PathSpec.from_file(filename)

    for file in spec:
        click.echo(file)

    return 0


@click.command()
@click.argument(
    "filename",
    type=click.Path(exists=True, dir_okay=False),
    default=".gitexport",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Prints the full traceback in case of an error.",
)
@click.version_option(
    prog_name="git-export",
)
def cli(verbose: bool, **kwargs) -> None:
    """
    Prints all files matched by the given pathspec file.

    The default pathspec file is '.gitexport'.
    """

    try:
        exitcode = main(**kwargs)
    except Exception as e:
        exitcode = 1

        if verbose:
            message = traceback.format_exc()
        else:
            message = repr(e)

        click.echo(message, err=True)
    finally:
        raise SystemExit(exitcode)


if __name__ == "__main__":
    cli()
