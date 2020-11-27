# Introduction

# Getting Started

# Resource Endpoint Library

## Questions
Questions are the main component of the trivia app. Each Question has a unique id, question , difficulty, and category attributes

> Endpoints\
> __POST__  /questions\
> __GET__   /questions\
> __POST__  /questions\
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
#### current_category _
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