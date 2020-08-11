import unittest
from unittest.mock import patch, Mock

from tests.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):

    def test_mock_getting_user_response_ok(self):
        mock_get_patcher = patch(
            'src.auth.utils.is_valid_github_token'
        )
        mock_get = mock_get_patcher.start()
        mock_get.return_value = Mock(status_code=200)


if __name__ == '__main__':
    unittest.main()
