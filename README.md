## For the webscraper see web_scraper folder's README.MD

Here's a summary of my work:
- Created a web scraper that downloads samples from cosmodis.com and then placed them in the `downloaded_files` directory under the `webscraper` folder.
- Implemented a script named `get_all_the_col.py` to extract all unique table headers from the downloaded files (available in the `webscraper` folder).
- Set up a Django application with a PostgreSQL database, and added a script to read the files from the `downloaded_files` directory and store their content in the database, which can be triggered by `python manage.py load_cosmos_data`.
- For database optimization, data was first stored in memory and then inserted into PostgreSQL in a single batch.
- The data can be accessed via the `/api/cosmos/` endpoint (please refer to the root `README.md` file for further details).
- The Django application has been containerized using Docker for easy deployment.


# To run the django in docker 
```bash
 bash scripts/live_server_deploy.sh 
```

## API Documentation for Cosmos Application

### Check API doc of redoc and swagger
```bash
http://127.0.0.1:8000/api_doc_v1/
and 
http://127.0.0.1:8000/api_doc_v2/

```

### Login Endpoint

#### Endpoint
`POST /api/login/`

#### Request Example (cURL)
```sh
curl --location 'http://127.0.0.1:8000/api/login/' \
--header 'Cookie: csrftoken=S8jQQrO1mh5p15aqHBb6L5O4Dn59eRyd; sessionid=4pzizh0de4wajbwk975w1wcdevx78j59' \
--form 'username="admin"' \
--form 'password="1516"'
```


#### Parameters
- `username` (required): The username of the user.
- `password` (required): The password of the user.

#### Headers
- `Cookie`: Required to send CSRF token and session information.

#### Response
- `200 OK`: Login successful. Returns a session token for further requests.
- `401 Unauthorized`: Invalid credentials provided.

#### Notes
- This endpoint requires valid CSRF tokens and cookies to be sent along with the request.


## Cosmos API

### Cosmos Model ViewSet

The Cosmos Model ViewSet provides CRUD operations on the `CosmosModel` along with filtering, searching, and pagination features.

#### Endpoint
- `GET /api/cosmos/`
- `POST /api/cosmos/`
- `GET /api/cosmos/{id}/`
- `PUT /api/cosmos/{id}/`
- `PATCH /api/cosmos/{id}/`
- `DELETE /api/cosmos/{id}/`

#### Authentication
- Authentication is required for all operations (`IsAuthenticated` permission class).

#### Parameters

**Query Parameters** for Filtering:
- `tax_id`: Filter by `tax_id`.
- `id`: Filter by `id`.
- `name`: Filter by `name` (case-insensitive).
- `relative_abundance_range`: Filter by range of `relative_abundance`. The format is `min_value,max_value`.
- `file_name`: Filter by `file_name` (case-insensitive).

#### Pagination
- The results are paginated using `CustomPagination`.
- Default page size is `10`.
- You can set the page size by using the query parameter `page_size`.
- The current page can be accessed via the `current_page` field in the response.

#### Response Structure for Paginated Response
```json
{
  "next": "<URL to next page>",
  "previous": "<URL to previous page>",
  "count": "<Total number of items>",
  "total_pages": "<Total number of pages>",
  "current_page": "<Current page number>",
  "results": [
    {
      "primary_key": "<Primary Key>",
      "id": "<ID>",
      "name": "<Name>",
      "tax_id": "<Tax ID>",
      "file_name": "<File Name>",
      "...": "(other fields)"
    }
  ]
}
```

#### Examples

**GET Cosmos Items (cURL)**

- **With Filter Options and Pagination**

```sh
curl --location --request GET 'http://127.0.0.1:8000/api/cosmos/?name=alpha&tax_id=123&page_size=5&page=2' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <your_access_token>'
```

**POST New Cosmos Item (cURL)**

```sh
curl --location --request POST 'http://127.0.0.1:8000/api/cosmos/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <your_access_token>' \
--data-raw '{
    "name": "Sample Cosmos",
    "tax_id": 123,
    "accession_id": "ACC001",
    "relative_abundance": 0.76
}'
```

**PATCH Update Cosmos Item (cURL)**

```sh
curl --location --request PATCH 'http://127.0.0.1:8000/api/cosmos/{primary_key}/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <your_access_token>' \
--data-raw '{
    "name": "Updated Cosmos Name"
}'
```

**DELETE Cosmos Item (cURL)**

```sh
curl --location --request DELETE 'http://127.0.0.1:8000/api/cosmos/{primary_key}/' \
--header 'Authorization: Bearer <your_access_token>'
```

#### Notes
- All fields in `CosmosModel` are optional except `primary_key`.
- The `relative_abundance_range` filter must be provided in `min_value,max_value` format (e.g., `0.1,0.5`).
- Fields such as `class_field`, `unique_matches`, and `total_matches` are renamed to avoid conflicts with Python keywords or improve readability.

---

### Error Codes
- `400 Bad Request`: Incorrect parameters or validation errors.
- `404 Not Found`: Resource not found.
- `500 Internal Server Error`: Server-side error occurred.



### For better understanding please contact me, I can help you to understand the project.