import click


@click.command()
def main():
    """CLI entrypoint."""
    click.echo("Hello World!")


if __name__ == "__main__":
    main()
