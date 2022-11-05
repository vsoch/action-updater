# Action Updater

[![PyPI version](https://badge.fury.io/py/action-updater.svg)](https://badge.fury.io/py/action-updater)
[![main](https://github.com/vsoch/action-updater/actions/workflows/main.yml/badge.svg)](https://github.com/vsoch/action-updater/actions/workflows/main.yml)

![docs/assets/img/logo/action-updater-small.png](docs/assets/img/logo/action-updater-small.png)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->


The actions updater will make it easy to update actions:

 - 🥑 updated syntax and commands
 - 🥑 versions of actions, either for releases or commits
 - 🥑 preview, write to new file, or write in place!
 - 🥑 run as a GitHub action workflow for annual checks!

You can see the [⭐️ Documentation ⭐️](https://vsoch.github.io/action-updater) for complete details!

## ⭐️ Quick Start ⭐️

### Installation

The module is available in pypi as [action-updater](https://pypi.org/project/action-updater/),
and to install we first recommend some kind of virtual environment:

```bash
$ python -m venv env
$ source env/bin/activate
```

And then install from pypi using pip:

```bash
$ pip install action-updater
```

### Usage

For all commands below, the actions updater can accept a directory with yaml files,
or a single yaml file that matches the GitHub actions schema.

View updaters available (and descriptions)

```bash
$ action-updater list-updaters
```
You should likely detect (to preview) before you write the changes to file.

```bash
# Run all updaters
$ action-updater detect .github/workfows/main.yaml

# Only detect for the setoutput updater
$ action-updater detect -u setoutput .github/workfows/main.yaml
```
And finally, write updates to file!

```bash
$ action-updater update .github/workfows/main.yaml
```

### 🎨 Screenshots 🎨

If a file has updates, it will print to the terminal the updated file for preview.

![docs/assets/img/detect.png](docs/assets/img/detect.png)

And after you run `update` (described below) you will see all green!

![docs/assets/img/clean.png](docs/assets/img/clean.png)

Running across many files:

![docs/assets/img/updates.png](docs/assets/img/updates.png)

And that's it! The action comes with several [updaters](https://vsoch.github.io/action-updater/developer-guide.html#updaters) that will look
for particular aspects to lint or update. If you have a request for a new updated, please
[open an issue](https://github.com/vsoch/action-updater/issues).

### Feature Ideas

This could be fairly easy to extend to allow for more "linting" style actions to reflect preferences in style, e.g:

```bash
$ action-updater lint .github/workflows/main.yaml
```

If this sounds interesting to you, please [open an issue](https://github.com/vsoch/action-updater) to discuss further!
We currently do some basic linting, as the yaml loading library has preferences for saving with respect to spacing, etc.

## 😁️ Contributors 😁️

We use the [all-contributors](https://github.com/all-contributors/all-contributors)
tool to generate a contributors graphic below.

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://vsoch.github.io"><img src="https://avatars.githubusercontent.com/u/814322?v=4?s=100" width="100px;" alt="Vanessasaurus"/><br /><sub><b>Vanessasaurus</b></sub></a><br /><a href="https://github.com/vsoch/action-updater/commits?author=vsoch" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.henrymike.com/"><img src="https://avatars.githubusercontent.com/u/11765982?v=4?s=100" width="100px;" alt="Mike Henry"/><br /><sub><b>Mike Henry</b></sub></a><br /><a href="https://github.com/vsoch/action-updater/commits?author=mikemhenry" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## License

This code is licensed under the MPL 2.0 [LICENSE](LICENSE).
