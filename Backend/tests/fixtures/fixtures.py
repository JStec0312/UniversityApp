import pytest 
from tests.fixtures.scenarios import *

@pytest.fixture
def sc_no_users(db_session):
    return scenario_no_users(db_session)

@pytest.fixture
def sc_with_verified_user_student(db_session):
    return scenario_with_verified_user_student(db_session)