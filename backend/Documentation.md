# Introduction
Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, and verbs.

# Resource Endpoint Library

## Questions
Questions are the main component of the trivia app. Each Question has a unique id, question , difficulty, and category attributes

> Endpoints\
> __POST__  /questions\
> __GET__   /questions\
> __POST__  /questions/search\
> __DELETE__/questions/:id

## Question Object
```json
{
    "id" : 1,
    "question" : "this is a sting question?",
    "answer" : "string answer",
    "category" : 2,
    "difficulty" : 3
}
```

### atributes

#### id _integer_
unique identifier of the question
#### question _string_
this is the question statement
#### answer _string_
the answer of the question
#### category _integer_
it the id of category object "Foreign Key"
#### difficulty _integer_
1 is the easiest 3 is the hardest

## Create Question
create new question object

> Endpoint\
> __POST__ /questions

### Request Parameters
#### question _string_ __REQUIRED__
The question"s statement, meant to be displayable to the player in the question list or during quiz playing. 
#### answer _string_ __REQUIRED__
preferrably to be one or two words
#### category _integer_ 
used to filter the questions by category for quiz or listing
#### difficulty _integer_ 
1 is the easiest 3 is the hardest
### Response
```json
{
    "id" : 1,
    "question" : "this is a sting question?",
    "answer" : "string answer",
    "category" : 2,
    "difficulty" : 3,
    "success" : true
}
```

## Retrieve Questions
this request gets 10 questions per page
> Endpoints\
>__GET__ /questions

### Request Parameters
#### page __URL query parameter__ _OPTIONAL_
if not supplied it is defaulted to 1\
`http://127.0.0.1:5000/questions?page=2`

### Response
if success, return is JSON object contains
#### success _Boolean_
true by default
#### questions _ARRAY_
array of questions objects. 10 questions per page
#### total_questions _Integer_
the total count of the ALL questions in the database
#### categories _JSON_
object of key value pairs of categories. Key is the id. Value is the category name
#### current_category 
null by default. 

```json
{
      "success" : true,
      "questions" : [{},{}],
      "total_questions" : 20,
      "categories" : {},
      "current_category": null
}
```

## Search Questions
this endpoint retrieve questions search results according to the submitted string
> Endpoints\
>__POST__ /questions/search

### Request Parameters
#### searchTerm _String_ __REQUIRED__
it is the string required to search
```json
{
    "searchTerm": "String"
}
```

### Response
if success, return is JSON object contains
#### success _Boolean_
true by default
#### questions _ARRAY_
array of questions objects. 10 questions per page
#### total_questions _Integer_
the total count of the ALL questions in the database

```json
{
      "success" : true,
      "questions" : [{},{}],
      "total_questions" : 20
}
```

## Delete Question
this endpoint deletes a specified question by its unique id
> Endpoints\
>__DELETE__ /questions/:id

### Request Parameters
#### :id _Integer_ __REQUIRED__
the id of the question to be deleted
### Response
if success, return is JSON object contains
#### success _Boolean_
true by default
#### deleted _Integer_
id of the question which is successfuly deleted
#### total_questions _Integer_
the total count of the ALL remaining questions in the database

```json
    {
      "success": true,
      "deleted" : 1,
      "total_questions": 19
    }
```

## Category
Category is the mean of questions classification according to the knowledge area

> Endpoints\
> __GET__   /categories\
> __GET__   /categories/:id/questions

## Category Object
```json
{
    "id" : 1,
    "type" : "category name"
}
```

### atributes

#### id _integer_
unique identifier of the category
#### type _string_
this is the category name

## Retrieve categories
this request gets all categories in the database
> Endpoints\
>__GET__ /categories

### Request Parameters
None
### Response
if success, return is JSON object contains
#### success _Boolean_
true by default
#### categories _JSON_
a key value pairs of categories where the key is the category id and the value is the category type

```json
{
      "success" : true,
      "categories" : {
          "1" : "category type",
          "2" : "another type"
      }
}
```

## Filter questions by category
this request gets all question of a specified category
> Endpoints\
>__GET__ /categories/:id/questions

### Request Parameters
#### :id _Integer_ __REQUIRED__
the id of the category to be used to filter the questions
### Response
if success, return is JSON object contains
#### success _Boolean_
true by default
#### categories _JSON_
a key value pairs of categories where the key is the category id and the value is the category type
#### questions _ARRAY_
array of questions objects. 10 questions per page
#### total_questions _Integer_
the total count of the ALL questions in the database
#### current_category _Category Object_
the category object that the questions are filtered by
```json
    {
      "success":true,
      "questions": ["<question_object>","<question_object>"],
      "total_questions": 20,
      "current_category": "<category_object>"
      }
```
## Quiz
This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 

> Endpoints\
>__POST__ /quizzes

### Request Parameters
a JSON object that contains
#### previous_questions _ARRAY_
array of integers. this array hold the IDs of the previous questions
#### quiz_category
array of integers. this array hold the ID of quiz questions category. if 0 all questions are retrieved
#### sample request body
```json
{
    "previous_questions": [1,23],
    "quiz_category": 5
}
```
### Response
if success, return is JSON object. if the quiz requires questions more than the questions query of a specified category, it will return question attribute to be null
#### success _Boolean_
true by default
#### question _Question Object_
the randomly retrieved question object not found in the previous_question array

```json
    {
      "success":true,
      "question": "<question_object>"
    }
```

# ERRORS

conventional HTTP response codes to indicate the success or failure of an API request. In general: Codes in the 2xx range indicate success. Codes in the 4xx range indicate an error that failed given the information provided (e.g., a required parameter was omitted). Codes in the 5xx range indicate an error with the server.

## Expected Errors

1. __400__ bad request
2. __404__ resource not found
3. __405__ method not allowed
4. __422__ unprocessable
5. __500__ server error

## ERROR attributes
### success _Boolean_
will be always false in case of error
### error _Integer_
the standard error code
### message _String_
a breif description of the error
### sample error JSON

```json
    {
      "success" : false,
      "error" : 400,
      "message" : "Bad Request"
    }

```