# Baymesh CLI and Python library

A WIP and unofficial [baymesh](http://bayme.sh) CLI and Python library for validating nodes that are a part of the [Meshtastic Bay Area Group's](https://bayme.sh/) mesh network. It's most useful as a way to doublecheck your work after following the [Bayme.sh Getting Started Guide](https://bayme.sh/docs/getting-started/), since the settings can be fiddly and easy to get wrong.

## Status

This project is in an experimental state. No support is offered yet!

## Requirements

* Python 3.11+
* macOS, Linux, or Windows

## Installing

To install the `baymesh` CLI, install via Homebrew:

```shell
brew install gtaylor/baymesh
```

Or PyPi:

```shell
pypi install baymesh
```

## Usage

Connect your node via USB and run:

```shell
baymesh validate
```

Your node will be checked against the [Bay Mesh Recommended Settings](https://bayme.sh/docs/getting-started/recommended-settings/).

## Contributing

To get your environment set up, you'll need the `uv` package manager. See [Installing uv](https://docs.astral.sh/uv/getting-started/installation/). Once `uv` is installed, do the following:

```shell
git clone git@github.com:gtaylor/baymesh-cli.git
cd baymesh-cli
make setup-dev
# Do your dev work here and run linters and tests afterwards:
make
```

## License

The contents of this repository are licensed under the GPLv3. A copy of the license may be found in the [LICENSE](./LICENSE) file in the repo root.