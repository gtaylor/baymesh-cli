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
brew install gtaylor/baymesh/baymesh
```

Or PyPi:

```shell
pypi install baymesh
```

## Usage

### Setting your node up to work with the Bay Mesh

To run your node through a guided setup flow, connect it via USB and run:

```shell
baymesh setup
```

This will leave you with a set of reasonable defaults applied to your node.

### Validating your node's configs

If you'd like to make sure that your node is compliant with the [Bay Mesh Recommended Settings](https://bayme.sh/docs/getting-started/recommended-settings/), connect it via USB and run:

```shell
baymesh validate
```

The CLI will recommend settings changes if it finds anything out of spec.

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