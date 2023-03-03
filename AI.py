from datetime import datetime 
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia 
import wolframalpha

#speech engine initialization
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id) # 0 = male, 1 = female
activationWord = "blue" #single word

#config browser
#set to path
msbrowser_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge"
webbrowser.register("msbrowser", None, webbrowser.BackgroundBrowser(msbrowser_path))

#wolfram alpha client
appId = "GQ6AWQ-3PEU97K5WR"
wolframClient = wolframalpha.Client(appId)


def speak(text, rate = 120) :
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()

def search_wikipedia(query = "") :
    searchResults = wikipedia.search(query)
    if not searchResults :
        print ("No wikipedia results")
        return "No results received"
    try :
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error :
        wikiPage = wikipedia.error(error.options[0])
    print (wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def ListOrDict(var) :
    if isinstance(var, list) :
        return var[0]["plaintext"]
    else :
        return var["plaintext"]

def search_wolframAlpha(query = "") :
    response = wolframClient.query(query)
    #@success : Wolfram Alpha  able to resolve the query
    #@numpod : Number of results returned
    #pod = list of results, this can also contains subpods
    if response["@success"] == "false" :
        speak ("The data could not found")
    else :
        result = ""
        #question
        pod0 = response["pod"][0]
        pod1 = response["pod"][1]
        #may contain the answer, has the highest confidence value
        #if it's primary or has the title of the result or definition then it's an official results
        if (("result") in pod1["@title"].lower()) or (pod1.get("@primary", "false") == "true") or ("definition" in pod1["@title"].lower()):
            #get the results
            result = ListOrDict(pod1["subpod"])
        #remove bracket results
            return result.split ("(")[0]
        else :
            question = ListOrDict(pod0["subpod"])
            #remove bracket results
            return question.split("(")[0]
            #search in wikipedia
            #speak ("Searching failed, gathering in wikipedia")
            #return search_wikipedia(question)

def parseCommand() :
    listener = sr.Recognizer()
    print ("Listening for a command")
    with sr.Microphone() as source :
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    try :
        print ("recognizing voice...")
        query = listener.recognize_google(input_speech, language="en_gb")
        print (f"the print input speech was : {query}")
    except Exception as exception :
        print ("i did not catch that")
        speak ("i did not catch that")
        print (exception)
        return "none"
    return query

#main loop
if __name__ == "__main__" :
    speak ("all system nominal")

    while True :
        #parse as a list
        query = parseCommand().lower().split()

        if query[0] == activationWord :
            query.pop(0)
            
            #list command
            if query[0] == "say" :
                if "hello" in query :
                    speak ("Greetings, all.")
                else :
                    query.pop(0) #remove say
                    speech = " ".join(query)
                    speak (speech)
            #website navigation
            if query[0] == "go" and query[1] == "to" : 
                speak("Opening...")
                query = " ".join(query[2:])
                webbrowser.get("msbrowser").open_new(query)

            #wikipedia

            if query[0] == "open" and query[1] == "wikipedia" :
                query = " ".join(query[2:])
                speak ("Reading wikipedia")
                speak (search_wikipedia(query))

            #wolfram alpha
            if query [0] == "compute" :#r query [0] == "computer" :
                query = " ".join(query[1:])
                speak ("Searching...")
                try :
                    result = search_wolframAlpha(query)
                    speak (result)
                    print (result)
                except :
                    speak ("Unable to get the data")

            if query[0] == "dated" and query[1] == "notes" :
                speak ("Ready to write your words")
                newNote = parseCommand().lower() 
                now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                with open("note_%s.txt" % now, "w") as newFile :
                    newFile.write(newNote)
                speak ("Note has been written")
            
            if query[0] == "single" and query[1] == "notes" :
                speak ("Ready to write your words")
                newNote = parseCommand().lower() 
                with open("single notes.txt", "w") as File :
                    File.write(newNote)
                speak ("Note has been written")
            
            if query [0] == "open" and query[1] == "notes" :
                query = " ".join(query[2:])
                speak ("opening your notes")
                with open("single notes.txt", "r") as File :
                    Notes = File.read()
                print (Notes)
            
            if query[0] == "exit" :
                speak ("Exiting")
                break