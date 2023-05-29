import sys
import argparse
import logging
from typing import Optional

from utils.trello_api import TrelloAPI
from utils.exceptions import APIRequestException, ListNotFoundException, LabelNotFoundException

# Set Logging
logging.basicConfig(level=logging.INFO)


def main(argv: Optional[list[str]] = None) -> None:
    """
    Runs the Trello API with the user provided args, creating a card on Trello, on the desired board and list, with
    the requested label (will create the label if not found) and card title, description and a comment.

    Example usage:
    --board_url "https:<board_url>" --list_name "TO DO" --card_name "New Card"
    --card_description "New card description" --card_comment "This is a comment for the new card"
    --label_name "Custom Label"
    """

    parser = argparse.ArgumentParser(description="App to create a Trello card using Trello's RestAPI. "
                                                 "This app was made as technical assessment by Everton "
                                                 "Cardoso Acchetta on April 23",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--board_url",
                        type=str,
                        action="store",
                        help="URL of the board that you wish to create the card on",
                        required=True)
    parser.add_argument("--list_name",
                        type=str,
                        action="store",
                        help="Name of the list (column) to create the card on.",
                        required=True)
    parser.add_argument("--card_name",
                        type=str,
                        action="store",
                        help="Title of the card to be created.",
                        required=True)
    parser.add_argument("--card_description",
                        type=str,
                        action="store",
                        help="Description of the card to be created.",
                        required=True)
    parser.add_argument("--card_comment",
                        type=str,
                        action="store",
                        help="Comment to be created with the card.",
                        required=True)
    parser.add_argument("--label_name",
                        type=str,
                        action="store",
                        help="Name of the label to apply to the card. If the label does not exists, "
                             "it will be created.",
                        required=True)

    # parse all the args
    try:
        args = parser.parse_args(argv)
    except ValueError as e:
        parser.print_help()
        logging.error(e)
        sys.exit(-1)

    parser_args = {"board_url": args.board_url,
                   "list_name": args.list_name,
                   "card_name": args.card_name,
                   "card_description": args.card_description,
                   "card_comment": args.card_comment,
                   "label_name": args.label_name}

    # creates the trello instance
    trello = TrelloAPI()

    try:
        # gets the necessary board data from the provided board URL
        board_data = trello.get_board_data(args.board_url)
        print("[CHECKPOINT] Board ID found.")

        # gets the list id from the provided list name
        list_id = trello.get_desired_list_id(board_data.id, args.list_name)
        print("[CHECKPOINT] List ID found.")

    except (APIRequestException, ListNotFoundException) as e:
        logging.error(e)
        logging.debug(parser_args)
        sys.exit(-1)

    # gets the label id from the provided label_name. If the label does not exist, a new one will be created
    try:
        label_id = trello.get_label_from_board(board_data.id, args.label_name)
        print("[CHECKPOINT] Label ID found.")
    except LabelNotFoundException:
        try:
            label_id = trello.create_label(board_data.id, args.label_name)
            print("[CHECKPOINT] Label not found. Created a new one.")
        except APIRequestException as e:
            logging.error(e)
            logging.debug(parser_args)
            sys.exit(-1)
    except APIRequestException as e:
        logging.error(e)
        logging.debug(parser_args)
        sys.exit(-1)

    try:
        # creates the card
        card_data = trello.create_card(list_id, label_id.id, args.card_name, args.card_description)
        print(f"[CHECKPOINT] Card created. Url: {card_data.url}")

        # creates the comment in the new card
        _ = trello.create_card_comment(card_data.id, args.card_comment)
        print("[FINISH] Comment created.")

    except APIRequestException as e:
        logging.error(e)
        logging.debug(parser_args)
        sys.exit(-1)


if __name__ == "__main__":
    main()
