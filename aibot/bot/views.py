from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests, os
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation
from .chat import user,handle,aimlHandle
import aiml
#Display recent 3 python questions which are not answered

def Home(request):
    return render(request, "aibot/home.html", {'home': 'active', 'chat': 'chat'})


@csrf_exempt
def Post(request):
    skipQuery = False
    try:
        if user[request.COOKIES['sessionID']] is None:
            pass
    except KeyError:
        kernel = aiml.Kernel()
        kernel.learn("/media/root/a9a409ac-aad4-4a06-b8b7-57e7e410b952/aibot/bot/start_aiml.xml")
        kernel.respond("LOAD AIML B")
        kernel.setBotPredicate("name", "AIbot")
        kernel.setBotPredicate("botmaster", "Nitesh")
        kernel.setBotPredicate("master", "Nitesh")
        kernel.setPredicate("email", "niteshdangi02@gmail.com")
        user[request.COOKIES['sessionID']]= {"conversation":{"general":[],"drafts":[]},"issued":[],"returned":[],"this":"","kernel":kernel}
    try:
        chat = user[request.COOKIES['sessionID']]
    except:
        return HttpResponse("")
    # print(chat)
    while len(chat['conversation']["general"])<2:
       chat['conversation']["general"].append('initiate')
    if request.method == "POST":
        query = request.POST.get('msgbox', None)
        if query is not None:
            query = query.strip()
            if query.startswith("%%"):
                skipQuery=True
            user[request.COOKIES['sessionID']] = chat
            response = handle(query.lower(),request)
            chat = user[request.COOKIES['sessionID']]
            if response is None:
                response=aimlHandle(query,request)
            # print(response)
            if skipQuery:
                query="Operation : "+query[2:]
                chat['conversation']["general"].append('<br>'+'<br>'.join(['<b>ME'+'&nbsp;'*7+':</b> <i>Option Selected</i>', '<b>AIBOT&nbsp;:</b> '+response[0]]))
            else:
                chat['conversation']["general"].append('<br>'+'<br>'.join(['<b>ME'+'&nbsp;'*7+':</b> '+query, '<b>AIBOT&nbsp;:</b> '+response[0]]))
            if query.lower() in ['bye', 'quit', 'bbye', 'seeya', 'goodbye']:
                chat_saved = chat['conversation']["general"][2:]
                response = ['<script>ended=true;</script><h3>Chat Summary:</h3><br/>' + '<br/><br/>'.join(chat_saved)]
                chat['conversation']["general"] = []
                user[request.COOKIES['sessionID']] = chat
                return JsonResponse({'response': response, 'query': query})
            #c = Conversation(query=query, response=response)
            user[request.COOKIES['sessionID']] = chat
            return JsonResponse({'response': response, 'query': query})
        else:
            if request.POST.get('getMessages',None) is not None:
                chat_saved = chat['conversation']["general"][2:]
                response = ""
                if len(chat_saved)>0:
                    response = '''<h3>Current Session Summary:</h3><h4>Books Issued: </h4>
                                '''+str(', '.join([x["name"].capitalize() for x in chat['issued']])+'')+'<h4>Books Returned: </h4>'+'''
                                '''+str(', '.join([x["name"].capitalize() for x in chat['returned']])+'')+'<h4>Chat History: </h4>'+'''
                                '''+''.join(chat_saved)
                # chat['conversation']["general"] = []
                # user[request.COOKIES['sessionID']] = chat
                if response == "":
                    response = "Hi, How may I help you!"
                return JsonResponse({'response': [response], 'query': ""})
            else:
                # user[request.COOKIES['sessionID']] = chat
                return  HttpResponse('Invalid Request')
    else:
        user[request.COOKIES['sessionID']] = chat
        return HttpResponse('Request must be POST.')

