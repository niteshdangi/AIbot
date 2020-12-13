import random
import difflib
import nltk
import aiml
from .library import library
# nltk.data.path.append("/media/root/a9a409ac-aad4-4a06-b8b7-57e7e410b952/nltk_data")

user = {}

book_names = [x['name'].lower() for x in library]
dept_names = [x['dept'].lower() for x in library]
book_codes = [x['code'].lower() for x in library]
issued = []


def aimlHandle(query, request):
    return [user[request.COOKIES['sessionID']]['kernel'].respond(query)]


def handle(query, request):
    aimlHandler = False
    # tokens = nltk.word_tokenize(query)
    # tag = nltk.pos_tag(tokens)
    # print(tag)
    crr = str(random.randint(11111111, 99999999))
    if query.startswith("can you") or query.startswith("can i"):
        reflection = "I"
        if query.startswith("can i"):
            reflection = "You"
        if "search" in query:
            return ["Yes "+reflection+" can search any book in the library", "<div class='msg-btn' id=\"search-book-con\"><input type=\"text\" id=\"search-book\" placeholder='Enter name of book' name=\"chat-msg\"  class=\"form-control\"/><script>"+'''
			$('#search-book').on('keyup',function(e) {
    if(e.keyCode == 13) {
        $('#chat-msg').val("%% search "+$('#search-book').val());
        $('#chat-form').submit();
        $('#search-book').val('Searching...');
        $('#search-book').attr("disabled","disabled");
    }
});'''+"</script></div>"]
        elif "issue" in query:
            return ["Yes "+reflection+" can issue any book available in the library", "<div class='msg-btn' id=\"search-book-con\" ><input type=\"text\" id=\"search-book\" placeholder='Enter name of book' name=\"chat-msg\" class=\"form-control\"/></div>"]
        elif "return" in query:
            iss = ["<div class='btn msg-btn btn-primary' id=\"tmp_funct_con_%s\" onclick='tmp_funct_%s()'><script>function tmp_funct_%s(){$(\"#send\").removeAttr(\"disabled\");$(\"#chat-msg\").val(\"%%%% return %s\");$(\"#send\").click();$(\"#tmp_funct_con_%s\").attr(\"disabled\",\"disabled\");}</script>Return %s Book</div>" % (
                crr+i["name"], crr+i["name"], crr+i["name"], i["name"], crr+i["name"], i["name"].capitalize()) for i in user[request.COOKIES['sessionID']]['issued']]
            # print(iss)
            return ["Yes "+reflection+" can return books issued by you"]+iss
    elif "about" in query:
        about = False
        if query.startswith("tell"):
            if "you" in query:
                about = True
        else:
            about = True
        if about:
            return ["I am AIbot a Chatbot for Library Management", "<ul class='ownerList'><li><img src='/static/nitesh.jpg'>Nitesh Kumar</li><li><img src='/static/img2.png'>Aditya</li><li><img src='/static/img3.png'>Abhishek</li><li><img src='/static/img4.jpg'>Kasuni</li></ul>"]
    elif query == "help":
        return ["Features Available:<br>1.) issue books<br>2.) return books<br>3.) search books by department,book and course code name<br>4.) ask questions related to commands<br>5.) count books<br>6.) about<br>7.) Miscellaneous commands<br>"]
    else:
        _issue, _return, _search, _count, _book, _dept, _ccode = False, False, False, False, False, False, False
        _query = ""
        tokens = nltk.word_tokenize(query)
        tag = nltk.pos_tag(tokens)
        grammar = "NP: {<WRB>?<JJ>?<VB>?<NNS>*<NN>*}"
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(tag)
        for subtree in result.subtrees(filter=lambda t: t.label() == 'NP'):
            for leave in subtree.leaves():
                if leave[0] == "many":
                    _count = True
                if leave[0] == "count":
                    _count = True
                if leave[0] == "total":
                    _count = True
                elif leave[0] == "issue":
                    _issue = True
                elif leave[0] == "return":
                    _return = True
                elif leave[0] == "search":
                    _search = True
                elif leave[0] == "find":
                    _search = True
                elif leave[0] == "where":
                    _search = True
                elif leave[0] in ["book", "books"]:
                    _book = True
                elif leave[0] == ["department", "dept"]:
                    _dept = True
                elif leave[0] in ["course", "code"]:
                    _ccode = True
                elif leave[1] in ['NN', "NNS"] and len(leave[0]) > 2 and leave[0] not in ["name"]:
                    _query += " "+leave[0]
        _query = _query.strip()
        if _query == "" and (_book or _issue or _return or _dept or _search or _ccode or _count):
            _query = user[request.COOKIES['sessionID']]['this']
        elif _book or _issue or _return or _dept or _search or _ccode or _count:
            user[request.COOKIES['sessionID']]['this'] = _query
        if "this" in _query:
            _query = _query.replace(
                "this", user[request.COOKIES['sessionID']]['this'])
        if _search:
            if _query == "":
                return ["Please Specify What you want to search!"]
            book_name = _query.replace("library", "").strip()
            response = [
                "I cant find any book or Department with name %s " % (book_name)]
            if len(book_name.split(" ")) > 0:
                if not _book and not _ccode and not _dept:
                    _book, _ccode, _dept = True, True, True
                match = difflib.get_close_matches(
                    book_name.strip(), book_names)
                if len(match) >= 1 and _book:
                    for book in library:
                        if book['name'].lower() == match[0].strip():
                            response = ["This Book is available in %s Department on floor %s" % (book['dept'], str(
                                book['floor'])), "<div class='btn msg-btn btn-primary' id=\"tmp_funct_con_%s\" onclick='tmp_funct_%s()'><script>function tmp_funct_%s(){$(\"#send\").removeAttr(\"disabled\");$(\"#chat-msg\").val(\"%%%% issue %s\");$(\"#send\").click();$(\"#tmp_funct_con_%s\").attr(\"disabled\",\"disabled\");}</script>Issue %s Book</div>" % (crr, crr, crr, book_name, crr, book_name.capitalize())]
                            break
                match = difflib.get_close_matches(book_name, book_codes)
                if len(match) >= 1 and _ccode:
                    for book in library:
                        if book['code'].lower() == match[0].strip():
                            response = ["Books with this Course Code is available in %s Department on %s floor" % (
                                book['dept'], str(book['floor']))]
                            break
                match = difflib.get_close_matches(book_name, dept_names)
                if len(match) >= 1 and _dept:
                    for book in library:
                        if book['dept'].lower() == match[0].strip():
                            response = ["Books of this Department is available on %s floor" % (
                                str(book['floor']))]
                            break
            return response
        elif _issue:
            if _query == "":
                return ["Please Specify Which book you want to issue."]
            response = ["Which book do you want to issue"]
            match = []
            for book in library:
                if book['name'].lower() == _query:
                    match.append(book['name'])
            if len(match) == 0:
                match = difflib.get_close_matches(_query, book_names)
            # print(match)
            if "id" in query:
                for book in library:
                    if str(book['id']) == query.split("id")[1].strip():
                        match = [book['name']]
            if len(match) == 1:
                i = 0
                for book in library:
                    if book['name'].lower() == match[0].strip():
                        if book not in user[request.COOKIES['sessionID']]['issued'] and book['available'] > 0:
                            user[request.COOKIES['sessionID']
                                 ]['issued'].append(book)
                            if book in user[request.COOKIES['sessionID']]['returned']:
                                user[request.COOKIES['sessionID']
                                     ]['returned'].remove(book)
                            book['available'] -= 1
                            library[i] = book
                            response = ["%s Book issued!" % (book["name"].capitalize(
                            )), "<div class='btn msg-btn btn-primary' id=\"tmp_funct_con_%s\" onclick='tmp_funct_%s()'><script>function tmp_funct_%s(){$(\"#send\").removeAttr(\"disabled\");$(\"#chat-msg\").val(\"%%%% return %s\");$(\"#send\").click();$(\"#tmp_funct_con_%s\").attr(\"disabled\",\"disabled\");}</script>Return this Book</div>" % (crr, crr, crr, book['name'], crr)]
                        elif book['available'] == 0:
                            response = [
                                "This books is unavailable for issuing"]
                        else:
                            response = [
                                "Book cant be issued as You have already issued this book"]
                        break
                    i += 1
            elif len(match) > 1:
                iss = []
                for book in match:
                    for i in library:
                        if i['name'].lower() == book.lower():
                            iss.append("<div style='margin:0;padding:0;' class='drt6t87ygh btn msg-btn' id=\"tmp_funct_con_%s\" onclick='tmp_funct_%s()'><script>function tmp_funct_%s(){$(\"#send\").removeAttr(\"disabled\");$(\"#chat-msg\").val(\" %%%% issue id %d\");$(\"#send\").click();$(\"#tmp_funct_con_%s\").attr(\"disabled\",\"disabled\");}</script>%s in %s (%s)</div>" % (
                                crr+i["name"], crr+i["name"], crr+i["name"], i["id"], crr+i["name"], i["name"].capitalize(), i["dept"].capitalize(), i['code'].upper()))
                response = ["I found %d books with name '%s'" % (len(
                    match), _query), "Click on the book name you want to issue:<ul><li>"+'<li>'.join(iss)+'</ul>']
            else:
                response = ["Book not found"]

            return response
        elif _return:
            if _query == "":
                return ["Please Specify Which book you want to return!"]
            response = ["Which book do you want to return"]
            _book_names = [x['name'].lower()
                           for x in user[request.COOKIES['sessionID']]['issued']]
            match = difflib.get_close_matches(_query, _book_names)
            if len(match) >= 1:
                i = 0
                for book in library:
                    if book['name'].lower() == match[0].strip():
                        if True:
                            if book in user[request.COOKIES['sessionID']]['issued']:
                                user[request.COOKIES['sessionID']
                                     ]['issued'].remove(book)
                            user[request.COOKIES['sessionID']
                                 ]['returned'].append(book)
                            book['available'] += 1
                            library[i] = book
                            response = ["%s Book Returned!" % (book["name"].capitalize(
                            )), "<div class='btn msg-btn btn-primary' id=\"tmp_funct_con_%s\" onclick='tmp_funct_%s()'><script>function tmp_funct_%s(){$(\"#send\").removeAttr(\"disabled\");$(\"#chat-msg\").val(\"%%%% issue %s\");$(\"#send\").click();$(\"#tmp_funct_con_%s\").attr(\"disabled\",\"disabled\");}</script>Issue this book Again</div>" % (crr, crr, crr, book['name'], crr)]
                        break
                    i += 1
            else:
                response = ["You might not issued this book"]

            return response
        elif _count:
            if _query == "":
                return ["Please Specify What you want to count!"]
            response = []
            dcount = 0
            bcount = 0
            ccount = 0
            _book = False
            if "name" in query:
                _book = True
                _query = _query.replace("name", "").strip()
            if not _book and not _ccode and not _dept:
                _book, _ccode, _dept = True, True, True
            if "in" in query:
                _book, _ccode, _dept = False, True, True
            for book in library:
                if _query in book['dept'].lower():
                    dcount += 1
                if _query in book['name'].lower():
                    bcount += 1
                if _query in book['code'].lower():
                    ccount += 1
            if dcount != 0 and _dept:
                response.append(
                    "There are %s books available in Department %s" % (str(dcount), _query))
            if bcount != 0 and _book:
                response.append(
                    "There are %s books available with name %s" % (str(bcount), _query))
            if ccount != 0 and _ccode:
                response.append(
                    "There are %s books available with Course Code %s" % (str(ccount), _query))
            if dcount == 0 and bcount == 0 and ccount == 0:
                response = ["I couldn't find anything with '%s'" % (_query)]
            if len(response) == 0 and "name" in query:
                response = [
                    "I couldn't find any book with name '%s'" % (_query)]
            return response
        elif _query != "":
            qt = ""
            if len(difflib.get_close_matches(_query, book_names, cutoff=0.7)) > 0:
                qt += "book"
            if len(difflib.get_close_matches(_query, book_codes, cutoff=0.7)) > 0:
                qt += "/course code"
            if len(difflib.get_close_matches(_query, dept_names, cutoff=0.7)) > 0:
                qt += "/department"
            response = [
                "What do you want to do with '%s'<br>I have this as a %s name" % (_query, qt)]
            if qt == "":
                response = aimlHandle(query, request)
            return response
        else:
            aimlHandler = True
    if aimlHandler:
        return aimlHandle(query, request)
