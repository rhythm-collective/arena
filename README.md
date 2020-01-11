# Arena

Connected arena.

## Table of Contents <!-- omit in toc -->

- [Arena](#arena)
  - [Setup](#setup)
  - [Mongodb Registration and Setup](#mongodb-registration-and-setup)
  - [Adding Entrypoints](#adding-entrypoints)
  - [Mongodb Samples](#mongodb-samples)
  - [NNG Samples](#nng-samples)

## Setup

1. Run `pip install -e` from root.
2. Run `arena` to start arena. *(This currently does nothing.)*
3. Run `pytest` to execute full test suite.

## Mongodb Registration and Setup

*If this is your first time registering, please validate and update these instructions to match your experience.*

1. Navigate to [User Registration](https://cloud.mongodb.com/user#/atlas/register/accountProfile) and register for an atlas account.
2. Create an Organization.
3. Create a Project.
4. Create a free tier cluster.
5. Create a new user account, as instructed, save the password into your .env file.
6. Add your IP, as instructed, to the whitelist.
7. Good to go! Run the Mongodb Sample with `arena_mongo`.

## Adding Entrypoints

1. Modify `setup.py:setup.entry_points.console_scripts`.
2. Add a new entrypoint to the `arena/__main__.py` file to match.
3. Run `pip install -e .` to compile the entrypoint.

## Mongodb Samples

Note that MongoDB sample will fail unless you have set up an atlas instance.

1. Run `arena_mongo` to trigger the mongo sample path.

## NNG Samples

1. Run `arena_nng` to trigger the nng sample path.

