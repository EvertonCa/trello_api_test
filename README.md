# Trello CLI

Using the Trello's RestAPI, create a new card to a specific board and list, with its title, description 
and a comment with it.

## Installation

This program is structured as a Python package, so it needs to be installed before being used.

- create a new virtual environment, using conda, miniconda, pyenv or any other of your liking. This example is for
using conda/miniconda:
  - if you do not have conda installed in your system, follow this tutorial: [Conda tutorial](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
  - create a new conda environment
    ```sh
    conda create -n trello_cli_env python=3.10
    ```
  - activate the newly create environment
    ```sh
    conda activate trello_cli_env
    ```


- To install only the program (without tests), run the following command inside the repository directory:

  ```sh
  pip install -e .
  ```
  
- To install the program with the necessary dependencies for running tests, run the following command inside the repository directory:

  ```sh
  pip install -e .[test]
  ```

### Providing credentials

The package expects credentials information to be provided through environment variables. 

Add the following snippet to one of your startup scripts (e.g. `~/.profile`, `~/.bashrc`, `~/.zshrc`) and fill the variables to provide authentication powers to the API.

```sh
# Trello's authentication variables
export TRELLO_API_KEY='' 
export TRELLO_API_TOKEN='' 
```

You may need to restart your terminal session after this.

This credentials can be obtained by following this tutorial: [Trello's authentication](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#authentication-and-authorization)

## Usage

In order to use this program, you can run this command from the root directory :

```sh
  python3 src/trello_cli/trello_cli.py --board_url "https:<board_url>" --list_name "<list name>" --card_name "<New Card>" 
  --card_description "<New card description>" --card_comment "<New card comment>" 
  --label_name "<Custom Label>"
```

Where:

- `--board_url`: https url of the desired board to create de new card on.
- `--list_name`: list (or column) name where the card will be created.
- `--card_name`: card title.
- `--card_description`: text that will be used as description of the card.
- `--card_comment`: text that will be used in the comment created in the newly created card.
- `--label_name`: label title that will be used in the card. If the label does not exist, a new one will be created will no color information.

Note that all arguments are required to run the program.

## Testing

In order to unit test this program, you must have installed the optional flag `test` (explained above) when installing this package with pip.

### Linting

To perform a linter verification, run the following commands from the root directory:

- using flake8, perform a check if there are Python syntax errors or undefined names
  ```sh
  flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
  ```

- using PyLint, check for linting problems
    
  ```sh
  pylint src/
  ```

### Unit testing

To perform a unit test on the TrelloAPI and trello_cli script, run the following command from the root directory:

```sh
python3 -m pytest
 ```

Tests performed on the TrelloAPI will be mocked (will not actually communicate with the Trello's RestAPI), but tests
performed on the trello_cli will actually test the execution of the actions performed, which means that the actions performed
 will reflect on the current test Trello environment.


## Next steps

Possible next steps for this project would be: 
- allowing the creation of new comments on cards that were previously created.
- allow the user to choose a color for the created label, when the label did not exist before.
- following the feature described above, allow the creation of cards without comments on it
- improving the test suite with a standard test environment (trello board made for tests) were the trello_cli unit tests would run on.
- allow editing and removal of cards, lists and labels


## Disclaimer

This program was created by Everton Cardoso Acchetta on April 2023 as a performance assessment for Python Software Engineer.