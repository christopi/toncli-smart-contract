<p align="center">
   <a href="https://disintar.io/">
       <img
        src="https://raw.githubusercontent.com/disintar/toncli/master/docs/images/logo.png"
        alt="Superset"
        height="150"
      />
   </a>
</p>

# toncli

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://badge.fury.io/py/toncli.svg)](https://github.com/disintar/toncli)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8f4acbbba3a743f992062c377c48c675)](https://www.codacy.com/gh/disintar/toncli/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=disintar/toncli&amp;utm_campaign=Badge_Grade)
[![TON](https://img.shields.io/badge/%F0%9F%92%8E-TON-green)](https://ton.org)

TON smart contract command line interface

## State

Not working, in active development

## Installation and Configuration

1. Compile `fift`, `func`, `lite-client` from [TON](https://github.com/newton-blockchain/ton)
    1. For Arch Linux we have [AUR package](https://aur.archlinux.org/packages/ton-git/) of ton
    2. For Apple computers on M1 we have a guide "How to compile them from official repo" [Apple M1 Guide](./docs/apple_m1_compile_fix.md)
2. Add these 3 packages to `PATH` env-variable
   or move them to `/usr/bin`, docs can be founded [here](https://ton.org/docs/#/howto/getting-started)
   1. `cp bild/crypto/fift /usr/bin/`
   2. `cp bild/crypto/func /usr/bin/`
   3. `cp bild/lite-client/lite-client /usr/bin/`
3. `pip install toncli`

Now you can access `CLI` tool by typing in terminal `toncli`

### Usage example

```
toncli start wallet -n my-wallet
cd my-wallet
toncli deploy
```

## Contributor Guide

Interested in contributing? Feel free to create issues and pull requests.

There is two main tasks and many TODOs.

Main tasks are - not to use lite-client / fift / func. All can be done with python.

There is many TODOs in code - feel free to fix them and create PRs

## Features and status

| Feature                                                                                         | Status |
|-------------------------------------------------------------------------------------------------|--------|
| `fift` / `func` / `lite-server` usage                                                           | ✅      |
| Easy bootstrap project samples `wallet`                                                         | ✅      |
| Deploy-wallet for auto send TON to contracts and tests                                          | ✅      |
| Compile func to `build/` from `func/` with `files.yaml`                                         | ✅      |
| Auto send TON to init contract address                                                          | ✅      |
| Deploy to mainnet / testnet                                                                     | ✅      |
| Project interact after deploy: easily send messages, run getmethods                             | ✅      |
| Load from hard project structure (example: `src/projects/wallet`)                               | ✅      |
| Run remote contracts locally (get cells from chain and run locally to get error / debug / etc.) | ✅      |
| Get contract address by `toncli address`                                                         | ❌      |
| Gas auto calculation for store & deploy                                                         | ❌      |
| Add more project samples with advanced usage                                                    | ❌      |
| Project tests with `runvmcode`                                                                  | ❌      |
| Project debug                                                                                   | ❌      |
| Library support                                                                                 | ❌      |
| Init Message support  (with signature)                                                          | ❌      |
| Docs for contract creation for beginners                                                        | ❌      |
| Advanced user-friendly docs on `fift`, `func`                                                   | ❌      |

## Commands

All commands could be fined in [docs/commands.md](https://github.com/disintar/toncli/blob/master/docs/commands.md)

### Configuration

Config folder will create on first deploy, all fift / func libs will copy to it, also deploy wallet contract will be
created

### Deploy process (how it's actually work)

1. Check network (testnet, mainnet) configuration locally (in config user folder)
    1. If no config found - download from URL in config.ini
2. Check deploy wallet locally (in config user folder)
    1. If it's first time - simple wallet will be created in config folder
    2. Message with wallet address and tips will be displayed (user need to send some TON coin on it)
    3. If there is no TON in deploy contract - script will exit and notify user to update deployer balance
3. Will run tests on `fift/data.fif` / `fift/message.fif` (if exist) / `fift/lib.fif` (if exist)  before creating deploy
   message
    1. This will check all files are correct
    2. Also, you can run custom logic - for example create keys in build/
4. Will calculate address of contract and display it to user
5. Will send money from deploy wallet
6. Will deploy your contract
    1. [External message](https://gist.github.com/tvorogme/fdb174ac0740b6a52d1dbdf85f4ddc63#file-generate-fif-L113) will
       be created
    2. Boc will generated
    3. Will invoke sendfile in lite-client (TODO: use native python lib, not lite-client)

## Development

```
git clone git@github.com:disintar/toncli.git
cd toncli && pip install -e .
```

