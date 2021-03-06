from app.models import *

def test_create_new_session_step_0(app, db_session, client):
    """
    A new user has a session id created for them and stored
    """
    form_payload = {
        "name_first": "foo",
        "name_last": "bar",
        "dob":"01/01/2000",
        "email":"foo@example.com",
        "zip": "12345",
    }
    with client.session_transaction() as http_session:
        assert http_session.get('session_id') == None
    response = client.post('/', data=form_payload, follow_redirects=False)
    with client.session_transaction() as http_session:
        assert http_session.get('session_id') != None
        registrant = Registrant.query.filter(Registrant.session_id == http_session.get('session_id')).first()
        assert registrant.reg_lookup_complete == True

def test_update_name_step_0_session_exists_already(app, db_session, client):
    """
    A returning user with a session id updates the existing registrant model.
    """
    # if active session exists update step 0 records
    registrant_data = {
        "name_first": "foo",
        "name_last": "bar",
        "dob": "01-01-2018",
        "email": "foo@bar.com",
        "phone": "555-555-5555"
    }
    #registration value should be automatically encrypted and decrypted
    new_registrant = Registrant(
        lang='en',
        county="Johnson",
        registration_value = registrant_data,
    )
    db_session.add(new_registrant)
    db_session.commit()

    with client.session_transaction() as http_session:
        http_session['session_id'] = str(new_registrant.session_id)
        current_registrant = Registrant.query.filter(Registrant.session_id == http_session.get('session_id')).first()

        assert current_registrant.registration_value.get('name_first') == 'foo'

        name_update = {
            "name_first": "baz",
            "zip": "12345",
        }
        current_registrant.update(name_update)
        db_session.commit()

        current_registrant_updated = Registrant.query.filter(Registrant.session_id == http_session.get('session_id')).first()
        assert current_registrant_updated.registration_value.get('name_first') == 'baz'
        assert current_registrant_updated.id == current_registrant.id


def test_registered_voter_input_returns_redirect_change_or_apply(app, db_session, client):
    """
    An already registered voter returns a redirect to change-or-apply endpoint
    """
    form_payload = {
        "name_first": "Kris",
        "name_last": "Kobach",
        "dob":"03/26/1966",
        "email":"foo@example.com",
        "zip": "66044",
    }
    with client.session_transaction() as http_session:
        assert http_session.get('session_id') == None

    response = client.post('/', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert ('/change-or-apply' in redirect_data) == True

def test_skip_sos_check_vr_only_returns_redirect_step_1(app, db_session, client):
    form_payload = {
        "name_first": "foo",
        "name_last": "bar",
        "dob": "02/02/1999",
        "email": "foo@example.com",
        "zip": "12345",
        "skip-sos": 'true',
    }
    app.config['ENABLE_AB'] = False
    response = client.post('/', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert ('/vr/citizenship' in redirect_data) == True

def test_unregistered_voter_input_returns_redirect_step_1(app, db_session, client):
    form_payload = {
        "name_first": "foo",
        "name_last": "bar",
        "dob":"02/02/1999",
        "email":"foo@example.com",
        "zip": "12345",
    }
    response = client.post('/', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert ('/change-or-apply' in redirect_data) == True

def test_dob_all_digits(app, db_session, client):
    form_payload = {
        "name_first": "foo",
        "name_last": "bar",
        "dob":"07071999",
        "email":"foo@example.com",
        "zip": "12345",
    }
    response = client.post('/', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert ('/change-or-apply' in redirect_data) == True

def test_dob_invalid_digits(app, db_session, client):
    form_payload = {
        "name_first": "foo",
        "name_last": "bar",
        "dob":"0707199",
        "email":"foo@example.com",
        "zip": "12345",
    }
    response = client.post('/', data=form_payload, follow_redirects=False)
    assert response.status_code != 302
