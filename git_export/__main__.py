import click

from git_export import PathSpec


class TypeTuple(click.ParamType):
    """A custom type for click that accepts a tuple of two strings."""

    name = "type_tuple"

    def convert(self, value, param, ctx):

        try:
            suffix, directory = value.split()

            if suffix.startswith("."):
                return suffix, directory

        except Exception:
            pass

        self.fail(repr(value), param, ctx)


@click.command()
@click.option(
    "--filename",
    type=click.Path(exists=True, dir_okay=False),
    default=".gitignore",
)
@click.version_option(
    prog_name="git-export",
)
@click.option(
    "--type",
    type=TypeTuple(),
)
def main(filename, type):
    """prints all files which are matched by the given pathspec file."""

    print(type)

    spec = PathSpec.from_file(filename)

    return
    for file in spec:
        click.echo(file)


if __name__ == "__main__":
    main()
