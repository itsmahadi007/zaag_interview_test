# Content
- Work summary
- Webscraper 
- Django with docker
#
Here's a summary of my work:
- Created a web scraper that downloads samples from cosmodis.com and which will directly place the files in the `downloads` directory under the `webscraper` folder.
- Implemented a script named `get_all_the_col.py` to extract all unique table headers from the downloaded files (available in the `webscraper` folder).
- Set up a Django application with a PostgreSQL database, and added a script to read the files from the `downloads` directory and store their content in the database, which can be triggered by `python manage.py load_cosmos_data`.
- For database optimization, data was first stored in memory and then inserted into PostgreSQL in a single batch.
- The data can be accessed via the `via the api` endpoint (please check below code).
- The Django application has been containerized using Docker for easy deployment.


# Web Scraper

Web Scraper is available in `webscraper` folder, it's independent form the django project.
first go to `webscraper` folder,

### Step 1: Create a Virtual Environment

To create a virtual environment, run:

```sh
python -m venv venv
```

### Step 2: Activate the Virtual Environment

- On **Windows**:
  ```sh
  venv\Scripts\activate
  ```
- On **Linux/macOS**:
  ```sh
  source venv/bin/activate
  ```

### Step 3: Install Requirements

With the virtual environment activated, install the required dependencies:

```sh
pip install -r requirements.txt
```

### Step 4: Run the Scraper

To run the scraper, execute:

```sh
python main.py
```

## Notes

- Make sure you have Python installed (preferably version 3.10 or above).

# Django 

## To run the django in docker 
```bash
 bash scripts/live_server_deploy.sh 

#  or

docker compose build
docker compose run django python manage.py makemigrations
docker compose run django python manage.py migrate
docker compose run django python manage.py collectstatic --noinput
docker compose run django python manage.py sample
docker compose run django python manage.py load_cosmos_data
docker compose up -d
```

## API Documentation for Cosmos Application

## User Authentication

### Login

To log in a user, use the following endpoint:

```bash
curl --location 'http://127.0.0.1:8000/api/users/login/' \
--header 'Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>' \
--form 'password="<password>"' \
--form 'username="<username>"'
```

- **Method**: POST
- **Parameters**:
  - `username`: The username of the user.
  - `password`: The password of the user.
- **Headers**:
  - `Cookie`: Include `csrftoken` and `sessionid` for CSRF protection.

### Token Refresh

To refresh the authentication token, use the following endpoint:

```bash
curl --location 'http://127.0.0.1:8000/api/users/token-refresh/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>' \
--data '{
    "refresh":"<refresh_token>"
}'
```

- **Method**: POST
- **Headers**:
  - `Content-Type`: application/json
  - `Cookie`: Include `csrftoken` and `sessionid`.
- **Body**:
  - `refresh`: The refresh token obtained during login.

### Register

To register a new user, use the following endpoint:

```bash
curl --location 'http://127.0.0.1:8000/api/users/register/' \
--header 'Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>' \
--form 'username="<username>"' \
--form 'email="<email>"' \
--form 'password1="<password1>"' \
--form 'password2="<password2>"'
```

- **Method**: POST
- **Parameters**:
  - `username`: Desired username.
  - `email`: User's email address.
  - `password1`: Password.
  - `password2`: Confirm password.
- **Headers**:
  - `Cookie`: Include `csrftoken` and `sessionid`.

## Check below url for data-models, results, root-samples, sub-samples, taxonomy apis
```bash
http://127.0.0.1:8000/api_doc_v1/
and 
http://127.0.0.1:8000/api_doc_v2/

```

### Example of Get Data Models with Authorization Token

To retrieve data models, use the following endpoint:

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/cosmos/data-models/' \
--header 'Authorization: Bearer <access_token>' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=<csrftoken>' \
--data '{
    "name": "<name>"
}'
```

- **Method**: GET
- **Headers**:
  - `Authorization`: Bearer token for authentication.
  - `Content-Type`: application/json
  - `Cookie`: Include `csrftoken`.
- **Body**:
  - `name`: Name of the data model to retrieve.

## Notes
- Ensure that the server is running and accessible at `http://127.0.0.1:8000`.

### For better understanding please contact me, I can help you to understand the project.