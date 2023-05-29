from trello_cli.trello_cli import main


def test_trello_cli(capsys) -> None:
    """
    Test for the trello cli program.

    This test will actually make the calls and completely run program in order to test all the pipeline. Note that this
    means that calls to the Trello API will be made and actions will be performed in the test Trello environment.

    The args used in this test are directed to a test board in trello and the correct authentication for it must be
    provided.
    """

    main(["--board_url", "https://trello.com/b/zQFa6vj2/canonicaltest",
          "--list_name", "coluna 1",
          "--card_name", "New Card",
          "--card_description", "New card description",
          "--card_comment", "This is a comment for the new card",
          "--label_name", "Custom Label"])
    captured = capsys.readouterr()
    output = captured.out
    url_created = output.split('Url: ')[1].split('\n')[0]
    assert output == f"""[CHECKPOINT] Board ID found.
[CHECKPOINT] List ID found.
[CHECKPOINT] Label not found. Created a new one.
[CHECKPOINT] Card created. Url: {url_created}
[FINISH] Comment created.
"""
