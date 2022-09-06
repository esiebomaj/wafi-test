# Wafi code challenge

## Technologies

- Python
- Django and Django rest framework

## Development Set up

- Clone repo `fit clone https://github.com/esiebomaj/wafi-test.git`
- create virtual enviroment `python3 -m venv /path/to/new/virtual/environment`
- activate virtual env `path\to\venv\Scripts\Activate`
- Install requirements `pip install -r requirements.txt`
- start django server `python manage.py runserver`

## Endpoint

- `api/add_user` to add a user to the system
- `api/deposit` deposit money into a users wallet
- `api/withdraw` withdraw money into a users wallet
- `api/transfer` transfer money from one user to another

## Some Considerations

- I used serializers in drf (to be able to quickly validate request body)
- I used drf function views so that we can clearly visuaize the logic, since this is a test
- To achieve an _InMemory_ solution, I used a dictionary to represent the users db. In a real world senario this would be table of a relational db

### Open to talking more about other implementation details
