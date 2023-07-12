from django.test import TestCase

# Create your tests here.
import pytest
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from .models import Language
from .serializers import LanguageSerializer
from .views import Language_CUD_APIView


@pytest.fixture
def view():
    return Language_CUD_APIView()


@pytest.fixture
def valid_language_data():
    return {
        "name": "English",
        "code": "en"
    }


@pytest.fixture
def invalid_language_data():
    return {
        "name": "Invalid Language"
    }


@pytest.fixture
def existing_language():
    return Language.objects.create(name="French", code="fr")


def test_post_with_valid_data(view, valid_language_data, mocker):
    # Mock the necessary dependencies and setup
    request = mocker.Mock()
    request.user = mocker.Mock()
    request.data = valid_language_data
    view.check_user_permissions = mocker.Mock(return_value=True)
    view.serializer_class = LanguageSerializer
    view.send_response = mocker.Mock()

    # Call the view method
    response = view.post(request)

    # Assertions
    view.check_user_permissions.assert_called_once_with(
        user=request.user, groups=['Admin'], perms=['Contribs.add_language']
    )
    view.serializer_class.assert_called_once_with(data=valid_language_data)
    view.serializer_class.return_value.is_valid.assert_called_once()
    view.serializer_class.return_value.save.assert_called_once()
    view.send_response.assert_called_once_with(
        view.serializer_class.return_value.data,
        "Language registered successfully",
        HTTP_201_CREATED
    )
    assert response == view.send_response.return_value


def test_post_with_invalid_data(view, invalid_language_data, mocker):
    # Mock the necessary dependencies and setup
    request = mocker.Mock()
    request.user = mocker.Mock()
    request.data = invalid_language_data
    view.check_user_permissions = mocker.Mock(return_value=True)
    view.serializer_class = LanguageSerializer
    view.BadRequest = mocker.Mock(side_effect=ValueError("Invalid data"))

    # Call the view method and expect an exception
    with pytest.raises(ValueError, match="Invalid data"):
        view.post(request)

    # Assertions
    view.check_user_permissions.assert_called_once_with(
        user=request.user, groups=['Admin'], perms=['Contribs.add_language']
    )
    view.serializer_class.assert_called_once_with(data=invalid_language_data)
    view.serializer_class.return_value.is_valid.assert_called_once()
    view.BadRequest.assert_called_once_with(view.serializer_class.return_value.errors)


def test_post_without_permission(view, valid_language_data, mocker):
    # Mock the necessary dependencies and setup
    request = mocker.Mock()
    request.user = mocker.Mock()
    request.data = valid_language_data
    view.check_user_permissions = mocker.Mock(return_value=False)
    view.PermissionDenied = mocker.Mock(side_effect=PermissionDenied("You don't have permission"))

    # Call the view method and expect a PermissionDenied exception
    with pytest.raises(PermissionDenied, match="You don't have permission"):
        view.post(request)

    # Assertions
    view.check_user_permissions.assert_called_once_with(
        user=request.user, groups=['Admin'], perms=['Contribs.add_language']
    )
    view.PermissionDenied.assert_called_once_with("You don't have permission")


def test_patch_with_valid_data(view, existing_language, mocker):
    # Mock the necessary dependencies and setup
    request = mocker.Mock()
    request.user = mocker.Mock()
    request.data = {'id': existing_language.id, 'name': 'Updated Language'}
    view.check_user_permissions = mocker.Mock(return_value=True)
    view.serializer_class = LanguageSerializer
    view.send_response = mocker.Mock()

    # Call the view method
    response = view.patch(request)

    # Assertions
    view.check_user_permissions.assert_called_once_with(
        user=request.user, groups=['Admin'], perms=['Contribs.change_language']
    )
    Language.objects.get.assert_called_once_with(id=existing_language.id)
    view.serializer_class.assert_called_once_with(
        instance=Language.objects.get.return_value,
        data=request.data,
        partial=True
    )
    view.serializer_class.return_value.is_valid.assert_called_once()
    view.serializer_class.return_value.save.assert_called_once()
    view.send_response.assert_called_once_with(
        view.serializer_class.return_value.data,
        "Language updated successfully"
    )
    assert response == view.send_response.return_value


# Write similar tests for other methods (e.g., test_patch_with_invalid_data, test_patch_without_permission, test_delete, etc.)

