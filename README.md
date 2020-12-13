# AIbot
Chatbot for Library Management
#### Features
  1. Can issue books
  2. Can return the issued books
  3. Can search books via book name, department name, course code
  4. Can count books
  5. Miscellaneous Chat

### Architecture

![alt text](https://github.com/nitteshdangi/AIbot/blob/main/architecture.png?raw=true)

### AIbot is handled via 2 files others are for django server
1. File 1 : /AIbot/bot/view.py
2. File 2 : /AIbot/bot/chat.py

#### Requirements
  1. nltk
  2. django
  3. aiml

### Books Available In Library
Math, Rice, OS, mth102
### Departments Available In Library
CSE, Agriculture
## TODO
To Add expand Library just add more in /AIbot/bot/library.py
