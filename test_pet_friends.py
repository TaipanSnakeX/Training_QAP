from tests.api import PetFriends
from tests.settings import valid_email, valid_password, invalid_password, invalid_email, empty_email, empty_password
import os

pf = PetFriends()


# Позитивные тесты

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_all_pets_with_valid_key(filter=""):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet(name='Taipan', animal_type='Snake', age='99', pet_photo='images/Taipan.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_update_pet_info(name='Kaa', animal_type='Snake', age=999):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('Create a new pet first')


def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Taipan", "Snake", '99', "images/Taipan.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_add_new_pet_with_cyrillic_symb_in_data(name='Тайпан', animal_type='Змей', age='99', pet_photo='images/Taipan'
                                                                                                       '.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_update_pet_photo(pet_photo='images/Taipan_2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.update_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200
    assert 'pet_photo' in result


# Негативные тесты

def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Forbidden' in result


def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Forbidden' in result


def test_get_api_key_for_empty_auth_data(email=empty_email, password=empty_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Forbidden' in result


def test_add_new_pet_with_symb_in_age(name='Taipan', animal_type='Snake', age='One', pet_photo='images/Taipan.jpg'):
    """Очевидно это баг. Данный тест успешно добавляет питомца с
    символами в поле "Возраст", что не предусмотрено формой"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200


def test_get_all_pets_with_incorrect_auth_key(filter=''):
    auth_key = {'key': 'ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae728'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert 'Forbidden' in result


def test_delete_pet_with_empty_pet_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Taipan', 'Snake', '99', 'images/Taipan.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = ''
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 404
    assert pet_id not in my_pets.values()


def test_get_list_of_pets_with_incorrect_filter_data(filter='pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500
    assert 'Internal Server Error' in result


def test_get_list_of_pets_with_symbols_in_auth_key(filter=''):
    auth_key = {'key': '&*^*)(*&)(&%$^%#)_(_(+)*&&^*&%%'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert 'Forbidden' in result


def test_get_my_pets_with_cyrillic_char_in_filter(filter='Мои питомцы'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500
    assert 'Internal Server Error' in result
