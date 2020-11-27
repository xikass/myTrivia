# Introduction

# Getting Started

# Resource Endpoint Library

## Questions
Questions are the main component of the trivia app. Each Question has a unique id, question , difficulty, and category attributes

> Endpoints\
> __GET__   /questions\
> __POST__  /questions\
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
The question's statement, meant to be displayable to the player in the question list or during quiz playing. 
#### answer _string_ __REQUIRED__
preferrably to be one or two words
#### category _integer_ __OPTIONAL__
used to filter the questions by category for quiz or listing
#### difficulty _integer_ __OPTIONAL__
1 is the easiest 3 is the hardest

### Response


## Retrieve Model

> Endpoints
>

### Request Parameters

### Response