from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

import requests

from .authentication import TrelloAuthenticationFromEnv
from .exceptions import APIRequestException, ListNotFoundException, LabelNotFoundException


class RequestType(Enum):
    """
    Enum class for RequestType containing 2 values - GET, POST
    """
    GET = "GET"
    POST = "POST"


@dataclass
class CardInfo:
    id: str
    url: str

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "CardInfo":
        return cls(id=data["id"],
                   url=data["url"])


@dataclass
class BoardInfo:
    id: str
    name: str

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "BoardInfo":
        return cls(id=data["id"],
                   name=data["name"])


@dataclass
class LabelInfo:
    id: str
    name: str

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "LabelInfo":
        return cls(id=data["id"],
                   name=data["name"])


class TrelloAPI:
    """
    Add a card to a Trello board with label and comment.
    """

    def __init__(self) -> None:
        # get authentication
        authentication = TrelloAuthenticationFromEnv()
        self.query = {"key": authentication.API_KEY,
                      "token": authentication.API_TOKEN}

        self.headers = {"Accept": "application/json"}

        # default urls to be used
        self.boards_list_url = "https://api.trello.com/1/boards/{}/lists"
        self.board_labels = "https://api.trello.com/1/boards/{}/labels"
        self.cards_url = "https://api.trello.com/1/cards"
        self.create_label_url = "https://api.trello.com/1/boards/{}/labels"
        self.add_comment_url = "https://api.trello.com/1/cards/{}/actions/comments"

    def call_api(self, request_type: RequestType,
                 endpoint: str,
                 payload: Optional[Union[dict[str, str], str]]) -> dict[str, str] | list[dict[str, str]] | None:
        """
        Function to call the Trello API via the Requests Library

        :param request_type: (RequestType) Type of Request. Supported Values - GET, POST
        :param endpoint: (str) API Endpoint.
        :param payload: (dict or str) API Request Parameters or Query String.

        :return: (dict, list[dict] or None) Response.
        """
        try:
            response = {}
            if request_type == RequestType.GET:
                response = requests.get(endpoint,
                                        timeout=30,
                                        headers=self.headers,
                                        params=payload)
            elif request_type == RequestType.POST:
                response = requests.post(endpoint,
                                         headers=self.headers,
                                         timeout=30,
                                         json=payload)

            if response.status_code in (200, 201):
                return response.json()

            response.raise_for_status()

            return None

        except requests.exceptions.HTTPError as errh:
            raise APIRequestException(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            raise APIRequestException(errc) from errc
        except requests.exceptions.Timeout as errt:
            raise APIRequestException(errt) from errt
        except requests.exceptions.RequestException as err:
            raise APIRequestException(err) from err

    def get_board_data(self, board_url: str) -> BoardInfo:
        """
        Gets from Trello's API general data from the provided board url and returns the board's ID and Name in a dict.
        The Trello's API documentation doesn't explain about this route, but using the URL for the board and adding
        '.json' at the end of it, will return the desired outcome.

        :param board_url: (str) the board url

        :return: (BoardInfo) Found board dataclass.
        """

        response = self.call_api(RequestType.GET, f"{board_url}.json", self.query)

        board_data = BoardInfo.from_dict(response)

        return board_data

    def get_desired_list_id(self, board_id: str,
                            list_name: str) -> str:
        """
        Gets from Trello's API the ID for the requested list in the provided board.

        See: https://developer.atlassian.com/cloud/trello/rest/api-group-boards/#api-boards-id-lists-get

        :raises ListNotFoundException: raised when the requested list could not be found.

        :param board_id: (str) id of the board to search the list
        :param list_name: (str) desired list's name

        :return: (str) ID of the found list.
        """
        board_lists = self.call_api(RequestType.GET, self.boards_list_url.format(board_id), self.query)

        for current_list in board_lists:
            if current_list['name'] == list_name:
                return current_list['id']

        raise ListNotFoundException(list_name)

    def get_label_from_board(self, board_id: str,
                             label_name: str) -> LabelInfo:
        """
        Gets from Trello's API the ID for the requested label in the provided board.

        See: https://developer.atlassian.com/cloud/trello/rest/api-group-boards/#api-boards-id-labels-get

        :raises LabelNotFoundException: raised when the requested label could not be found.

        :param board_id: (str) id of the board to search the label or create the new one
        :param label_name: (str) name of the label to be searched for.

        :return: (LabelInfo) Dataclass of the found label
        """

        labels = self.call_api(RequestType.GET, self.board_labels.format(board_id), self.query)

        for board_label in labels:
            if board_label["name"] == label_name:
                found_label = {'id': board_label['id'], 'name': board_label['name']}
                return LabelInfo.from_dict(found_label)

        raise LabelNotFoundException(label_name)

    def create_label(self, board_id: str,
                     label_name: str) -> LabelInfo:
        """
        Creates a new label with no color and the given name in the provided board id.

        See: https://developer.atlassian.com/cloud/trello/rest/api-group-boards/#api-boards-id-labels-post

        :param board_id: (str) id of the board to create the label in.
        :param label_name: (str) text to be used as label name.

        :return: (LabelInfo) New label dataclass.
        """

        additional_params = {'name': label_name,
                             'color': 'null'}

        response = self.call_api(RequestType.POST,
                                 self.create_label_url.format(board_id),
                                 {**self.query, **additional_params})

        new_label = LabelInfo.from_dict(response)

        return new_label

    def create_card(self, board_list_id: str,
                    label_id: str,
                    card_name: str,
                    card_description: str) -> CardInfo:
        """
        Creates a new card in the list id provided with name and description and applies the given label to it.

        See: https://developer.atlassian.com/cloud/trello/rest/api-group-cards/#api-cards-post

        :param board_list_id: (str) ID of the list that the card will be created on.
        :param label_id: (str) ID of the label to be applied to the card
        :param card_name: (str) Card's title.
        :param card_description: (str) Card's description

        :return: (CardInfo) New card dataclass.
        """
        additional_params = {"idList": board_list_id,
                             "name": card_name,
                             "idLabels": label_id,
                             "desc": card_description}

        response = self.call_api(RequestType.POST,
                                 self.cards_url,
                                 {**self.query, **additional_params})

        new_card = CardInfo.from_dict(response)

        return new_card

    def create_card_comment(self, card_id: str,
                            comment: str) -> str:
        """
        Creates a new comment in the provided card_id.

        See: https://developer.atlassian.com/cloud/trello/rest/api-group-cards/#api-cards-id-actions-comments-post

        :param card_id: (str) ID of the card to create the comment on.
        :param comment: (str) text of the comment to be created

        :return: (str) New comment's ID
        """

        additional_params = {'text': comment}

        response = self.call_api(RequestType.POST,
                                 self.add_comment_url.format(card_id),
                                 {**self.query, **additional_params})

        return response['id']
