# Challenge 

## Goal

The goal of this challenge is to create a microservice providing an API to work with word definitions/translations taken from Google Translate. 

## Start the project
docker-compose up -d
- Please see also deploy folder structure
 
## Endpoints
Base endpoint http://127.0.0.1:8000/api/translate
****
- Get the details about the given word.
****
GET **/search?word=challenge**
  
  The response shall include definitions, synonyms, translations and examples taken from the corresponding Google Translate page (e.g. 
[challenge word translation](https://translate.google.com/?sl=en&tl=ru&text=challenge&op=translate)).
  
  Data fetched from Google Translate has to be saved in the DB. When a request arrives to the endpoint, the handler has to look for the word in 
the DB first and fall back to Google Translate only if it is not there.
****
- Get the list of the words stored in the database. 
****

GET **/**

**params**
- limit
- offset
- search
- projection


  Pagination, sorting and filtering by word is required. Partial match has to be used for filtering. Definitions, synonyms and translations 
shall not be included in the response by default but can be enabled by providing corresponding query parameters.
****
- Delete a word from the database.
****
DELETE **/{word}/**

## Implementation

- `Python 3.10` with `FastAPI` web framework have used.

- `Dockerfile` and `docker-compose.yml` are included.

- Database is MySQL as a test, but the recommended way for this task is to use Elastic. 
- Or maybe just modify table with fks for now.

- I have developed some ideal solution that is ready to scale. 

- Approaches that I have used are very deep, and shows many solutions that fit to today's challenges. The up to bottom 
- layer of abstraction demonstrated by dependency injector and the project's structure is simple and comprehensive.

- Also some preparation work for dev ops was shown in project.

## Enjoy high-level coding example