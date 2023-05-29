from trello_cli.utils.trello_api import BoardInfo, LabelInfo, CardInfo
from trello_cli.utils.exceptions import *


def test_mock_get_board_data(mocker, trello_api) -> None:
    """
    Mocked test for the method get_board_data from the TrelloAPI.
    """
    # mocks the expected api response for this call
    mocked_call_api_value = {'id': '423142342hbu3h421',
                             'name': 'Canonical_test',
                             'desc': '',
                             'descData': None,
                             'idOrganization': '34124bj2h4bj2',
                             'idEnterprise': None,
                             'pinned': False,
                             'url': 'https://trello.com/b/fasdfadf/canonicaltest',
                             'shortUrl': 'https://trello.com/b/ffiasdbna',
                             'prefs': {'background': '32523452342'},
                             'labelNames': {'black': ",'black_dark:"}}
    mocker.patch('trello_cli.utils.trello_api.TrelloAPI.call_api',
                 return_value=mocked_call_api_value)

    # creates the dataclass from the api response
    mocked_dataclass = BoardInfo.from_dict(mocked_call_api_value)

    # calls the method using the mocked data and compares it to the expected result
    actual_mock_response = trello_api.get_board_data(board_url='https://trello.com/b/zQFa6vj2/canonicaltest')
    assert mocked_dataclass == actual_mock_response


def test_mock_get_desired_list_id(mocker, trello_api) -> None:
    """
    Mocked test for the method get_desired_list_id from the TrelloAPI.
    """
    # mocks the expected api response for this call
    mocked_call_api_value = [{'id': '423142342hbu3h421',
                              'name': 'Column 1',
                              'closed': False,
                              'idBoard': 'f542hb5564h5jn',
                              'pos': 65535,
                              'subscribed': False,
                              'softLimit': None,
                              'status': None},
                             {'id': '34234h2ihbj4hu2n3',
                              'name': 'Column 2',
                              'closed': False,
                              'idBoard': 'f542hb5564h5jn',
                              'pos': 65534,
                              'subscribed': False,
                              'softLimit': None,
                              'status': None}]
    mocker.patch('trello_cli.utils.trello_api.TrelloAPI.call_api',
                 return_value=mocked_call_api_value)

    # calls the method using the mocked data and compares it to the expected existing result
    actual_mock_response = trello_api.get_desired_list_id(board_id='f542hb5564h5jn',
                                                          list_name='Column 2')

    assert '34234h2ihbj4hu2n3' == actual_mock_response

    # calls the method using the mocked data and compares it to the expected NOT existing result
    try:
        _ = trello_api.get_desired_list_id(board_id='f542hb5564h5jn',
                                           list_name='Column 3')
        assert False
    except ListNotFoundException:
        assert True


def test_mock_get_label_from_board(mocker, trello_api) -> None:
    """
    Mocked test for the method get_label_from_board from the TrelloAPI.
    """
    # mocks the expected api response for this call
    mocked_call_api_value = [{'id': '423142342hbu3h421',
                              'name': 'Custom Label',
                              'idBoard': 'f542hb5564h5jn',
                              'color': None},
                             {'id': '34234h2ihbj4hu2n3',
                              'name': 'Custom Label 2',
                              'idBoard': 'f542hb5564h5jn',
                              'color': None}]
    mocker.patch('trello_cli.utils.trello_api.TrelloAPI.call_api',
                 return_value=mocked_call_api_value)

    # calls the method using the mocked data and compares it to the expected existing result
    actual_mock_response = trello_api.get_label_from_board(board_id='f542hb5564h5jn',
                                                           label_name='Custom Label')

    assert '423142342hbu3h421' == actual_mock_response.id

    # calls the method using the mocked data and compares it to the expected NOT existing result
    try:
        _ = trello_api.get_label_from_board(board_id='f542hb5564h5jn',
                                            label_name='Custom Label 3')
        assert False
    except LabelNotFoundException:
        assert True


def test_mock_create_label(mocker, trello_api) -> None:
    """
    Mocked test for the method create_label from the TrelloAPI.
    """
    # mocks the expected api response for this call
    mocked_call_api_value = {'id': '423142342hbu3h421',
                             'idBoard': 'f542hb5564h5jn',
                             'name': 'Custom Label',
                             'color': None}
    mocker.patch('trello_cli.utils.trello_api.TrelloAPI.call_api',
                 return_value=mocked_call_api_value)

    # creates the dataclass from the api response
    mocked_dataclass = LabelInfo.from_dict(mocked_call_api_value)

    # calls the method using the mocked data and compares it to the expected result
    actual_mock_response = trello_api.create_label(board_id='f542hb5564h5jn',
                                                   label_name='Custom Label')
    assert mocked_dataclass == actual_mock_response


def test_mock_create_card(mocker, trello_api) -> None:
    """
    Mocked test for the method create_card from the TrelloAPI.
    """
    # mocks the expected api response for this call
    mocked_call_api_value = {'id': '423142342hbu3h421',
                             'url': 'https://trello.com/b/fasdfadf/canonicaltest',
                             'idBoard': 'f542hb5564h5jn',
                             'idList': 'f43bn5j34b65j2k3',
                             'idLabels': ['7j5nbj6km4b64'],
                             'name': 'New Card',
                             'desc': 'New card description'}
    mocker.patch('trello_cli.utils.trello_api.TrelloAPI.call_api',
                 return_value=mocked_call_api_value)

    # creates the dataclass from the api response
    mocked_dataclass = CardInfo.from_dict(mocked_call_api_value)

    # calls the method using the mocked data and compares it to the expected result
    actual_mock_response = trello_api.create_card(board_list_id='f43bn5j34b65j2k3',
                                                  label_id='7j5nbj6km4b64',
                                                  card_name='New Card',
                                                  card_description='New card description')
    assert mocked_dataclass == actual_mock_response


def test_mock_create_card_comment(mocker, trello_api) -> None:
    """
    Mocked test for the method create_card_comment from the TrelloAPI.
    """
    # mocks the expected api response for this call
    mocked_call_api_value = {'id': '423142342hbu3h421',
                             'idMemberCreator': '8b5jn6k34jn53jk'}
    mocker.patch('trello_cli.utils.trello_api.TrelloAPI.call_api',
                 return_value=mocked_call_api_value)

    # calls the method using the mocked data and compares it to the expected result
    actual_mock_response = trello_api.create_card_comment(card_id='7j5nbj6km4b64',
                                                          comment='This is a comment for the new card')

    assert '423142342hbu3h421' == actual_mock_response

