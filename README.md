# Arena

Connected arena.

## Table of Contents <!-- omit in toc -->

- [Arena](#arena)
  - [Setup](#setup)
  - [Adding Entrypoints](#adding-entrypoints)
  - [Mongodb Samples](#mongodb-samples)
  - [NNG Samples](#nng-samples)

## Setup

1. Run `pip install -e` from root.
2. Run `arena` to start arena. *(This currently does nothing.)*
3. Run `pytest` to execute full test suite.

## Adding Entrypoints

1. Modify `setup.py:setup.entry_points.console_scripts`.
2. Add a new entrypoint to the `arena/__main__.py` file to match.
3. Run `pip install -e .` to compile the entrypoint.

## Mongodb Samples

Note that MongoDB sample will fail unless you have set up an atlas instance.

1. Run `arena_mongo` to trigger the mongo sample path.

## NNG Samples

1. Run `arena_nng` to trigger the nng sample path.

