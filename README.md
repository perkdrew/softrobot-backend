# SoftRobot

An HTTP-based mini game backend server that allows users to login, register game scores, and retrieve a list of high scores for the levels

## General Plan

The original plan was to use Starlette or another lightweight async framework as I was under the impression that there was more flexibility with the tools we could use. However, after looking at the tasks in detail, it seemed like a more equitable choice to stick with a bare implementation of the server and endpoints. I began by thoroughly reviewing the documentation for the Python standard library, specifically http.server. The plan was to follow as closely to the Python standard library, with the exception of installing Black for code formatting and Pytest for the test suite. I spent the time available during Saturday and Sunday to complete the main functionalities and conduct some light testing. I used Saturday to read through documentation, refresh certain concepts, and plan out the structure for the code, whereas Sunday was spent on the larger development. If I had more time, I would continue with the testing I had only started to structure, and rather, plan with TDD in mind.

To handle multiple threads, I added a class with mix-in from the the http.server settings. For general responses, I set the LRU cache that comes with Python.

## Login

For basic authentication, I used a dictionary to refer to a simple session store for users. In the Python standard library, there was secrets, but I found that using random and string could suffice for what was in the example. The expiration is set to 10 minutes. In other circumstances, I often go with JWT authentication. If more time was allotted and larger data was used, I would have potentially used collections in Python for more nuanced data structures.

## Posting Scores

In posting scores, I check if the levels exist in a list that I am using as the data store. I chose a list with dictionaries. It would be easy to go between list comprehensions, generator expressions, lambda functions, filters, sorts, etc. Of course, lists are slower than dictionaries or sets but we are working with 15 entries at a time.

For the 1st constraint, I reset scores for a user if they already exist in the level. If the level doesn't exist, all relevant data will be added. For the 2nd constraint, I have a rank/delete function for limiting 15 top entries per level and removing the entries that were no longer highest.

## Getting High Score List

For the high score list, I queried for only user and score, and organized the list as I had in the previous task.

## Conclusion

I really enjoyed this test, particularly because by setting limitations for what I could use, I was able to really get under the surface of those abstractions layered on web development frameworks. Particularly, one can take for granted Werkzeug with Flask or Django's ORM. The biggest pause I took in the work was the implementation of request pathways. The http.server documentation for keywords and request bodies was not as clear; it was hard to set the data types that one can put in and the parsing of the paths could be refactored into something more general. If I were to develop this with any tech stack, I would have used FastAPI and Docker. If I had more experience with Go, that would have also been considered.
