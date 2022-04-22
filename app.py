# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 20:34:26 2021

@author: pandy
"""

from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory,render_template
from pymongo import MongoClient
from pywebio.input import *
from pywebio.output import *
from pywebio.session import set_env
import pymongo
app=Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('inner.html')


def model():
    tpl = '''
    <!DOCTYPE html>
<html>
<head>
	<title>Interview Performance Estimator</title>

	<style type="text/css">
		
		body{
			background-image:url('https://www.tcs.com/content/dam/tcs/images/discover-tcs/about-us/news/rajesh-gopinathan-ceo-and-md-tcs-interview-forbes-india-web.jpg');
			background-size: cover;
			background-attachment: fixed;
            padding:0px 350px;
		}

		.content{
			background: white;
			width: 50%;
			padding: 40px;
			margin: 100px auto;
			font-family: calibri;
			border-radius: 10px;
		}

		p{
			font-size: 25px;
			color: black;
		}

	</style>
</head>

</html>
    '''
    put_widget(tpl, {
    "open": True,})
    set_env(title='Interview Performance Estimator', output_animation=True,input_panel_fixed=False)  
    style(put_markdown('Interview Performance Estimator'), "text-align:center;color:white; color:#484848; font-size: 60px; font-style:italic; font-weight: 900")
    #put_image('https://i.ibb.co/TWxRhng/im-removebg-preview-1.png', width='1000px',height='300px',position=-1)
    style(put_text('RUN AS ONE'),"text-align:center;color:white; color:#f3ad51; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
    style(put_text('Software That Puts People To Work'),"text-align:center;color:white; color:white; font-size: 32px; font-style:italic; font-weight: 900")
    style(put_text('Unify The Teams,Systems, and data that drive your Recruiting Buisness'),"text-align:center;color:white; color:white; font-size: 32px; font-style:italic; font-weight: 900")
    Domain=input('Please Enter The Specific Domain For Which Interview is Being Conducted')
    Domain=Domain.replace(" ", "_")
    Domain=Domain.capitalize()
    dbs = MongoClient().database_names()
    import pandas as pd
    modelname ='deepset/xlm-roberta-large-squad2'
    if Domain not in dbs:
        client = MongoClient()
        db = client[Domain]  # use a database called "test_database"
        collection = db.corpus   # and inside that DB, a collection called "files"
        text =file_upload("Select a Corpus For a Specified Domain(Accepted format is .txt)", accept=".txt")
        text=text['content']
        text=text.decode('utf-8')
        text_file_doc = {"first11": "test.txt", "contents" : text }
        collection.insert(text_file_doc)
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[Domain]
        col = db["corpus"]
        x = col.find()
        for string in x:
            print(string)
        string=string['contents']
        db = client[Domain] # use a database called "test_database"
        collection = db.question   # and inside that DB, a collection called "files"
        text = file_upload("Upload Interview questions for a given corpus(Accepted format is .txt and Please Use Commar as a Seperator)", accept=".txt")
        text=text['content']
        text=text.decode('utf-8')
        text_file_doc = {"question": "question.txt", "contents" : text }
        collection.insert(text_file_doc)
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[Domain]
        col = db["question"]
        y = col.find() 
        for question in y:
            print(question)
        interviewer_quest=question['contents']
        interviewer_quest=interviewer_quest.split(',')
        interviewer_question=[]
        for i in range(len(interviewer_quest)):
            interviewer_quest[i]=" ".join(interviewer_quest[i].split())
            interviewer_question.append(interviewer_quest[i])
        with put_loading(shape='border', color='success'):
            import re
            context=string.lower().strip()
            context = re.sub('[^a-zA-Z0-9\s\.]', ' ', string)
            context = ' '.join(context.split())
            import pandas as pd
            from transformers import AutoTokenizer, AutoModelForQuestionAnswering
            model =AutoModelForQuestionAnswering.from_pretrained(modelname)
            tokenizer = AutoTokenizer.from_pretrained(modelname)
            from transformers import pipeline
            nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
            model_answer=[]
            question=[]
            for questions in interviewer_question:
                ans=nlp({'question':questions,'context': context})
                start=ans['start']
                end=ans['end']
                answer=context[start:end+400] #increasing the length of the answer accordingly because model answers it in a summarized form
                model_answers=answer
                model_answers = model_answers.split('.') #restricting the answer when the sentence end 
                model_answers = model_answers[0]#Taking the best answerfrom the model
                model_answer.append(model_answers)
                question.append(questions)
            db = client[Domain] # use a database called "test_database"
            collection = db.modelanswer   # and inside that DB, a collection called "files"
            modelanswer = model_answer
            text_file_doc = {"modelanswer": "modelanswer.txt", "contents" : modelanswer }
            collection.insert(text_file_doc)
            db = client[Domain] # use a database called "test_database"
            collection = db.modelname # and inside that DB, a collection called "files"
            model_name = modelname
            text_file_doc = {"model_name": "model_name.txt", "contents" : model_name }
            collection.insert(text_file_doc)
    else:
        track=actions('Domain Already Exist You Want to Replace',['Yes','No'])
        track=track.lower()
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        if track=='yes':
            db = client[Domain]
            col = db["modelname"]
            zp = col.find()
            for modelnamed in zp:
                print(modelnamed)
            modelpre=modelnamed['contents']
            db = client[Domain]
            col = db["modelanswer"]
            zp = col.find()
            for modelanswer in zp:
                print(modelanswer)
            modelans=modelanswer['contents']
            client = MongoClient()
            import pymongo
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client[Domain]
            col = db["corpus"]
            U = col.find()
            for strings in U:
                print(strings)
            strings=strings['contents']
            db = client[Domain]
            col = db["question"]
            j = col.find() 
            for questions in j:
                print(questions)
            interviewer_quests=questions['contents']
            interviewer_quests=interviewer_quests.split(',')
            interviewer_questions=[]
            for i in range(len(interviewer_quests)):
                interviewer_quests[i]=" ".join(interviewer_quests[i].split())
                interviewer_questions.append(interviewer_quests[i])
            #client.drop_database(Domain)
            db = client[Domain]  # use a database called "test_database"
            collection = db.corpus   # and inside that DB, a collection called "files"
            text =file_upload("Select a Corpus For a Specified Domain(Accepted format is .txt)", accept=".txt")
            text=text['content']
            text=text.decode('utf-8')
            text_file_doc = {"first11": "test.txt", "contents" : text }
            collection.insert(text_file_doc)
            import pymongo
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client[Domain]
            col = db["corpus"]
            x = col.find()
            for string in x: 
                print(string)
            string=string['contents']
            db = client[Domain] # use a database called "test_database"
            collection = db.question   # and inside that DB, a collection called "files"
            text = file_upload("Upload Interview questions for a given corpus(Accepted format is .txt and Please Use Commar as a Seperator)", accept=".txt")
            text=text['content']
            text=text.decode('utf-8')
            text_file_doc = {"question": "question.txt", "contents" : text }
            collection.insert(text_file_doc)
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client[Domain]
            col = db["question"]
            y = col.find() 
            for question in y:
                print(question)
            interviewer_quest=question['contents']
            interviewer_quest=interviewer_quest.split(',')
            interviewer_question=[]
            for i in range(len(interviewer_quest)):
                interviewer_quest[i]=" ".join(interviewer_quest[i].split())
                interviewer_question.append(interviewer_quest[i])
            if interviewer_question==interviewer_questions and strings==string and modelpre==modelname:
                model_answer=modelans
            else:
                with put_loading(shape='border', color='success'):
                    import re
                    context=string.lower().strip()
                    context = re.sub('[^a-zA-Z0-9\s\.]', ' ', string)
                    context = ' '.join(context.split())
                    import pandas as pd
                    from transformers import AutoTokenizer, AutoModelForQuestionAnswering
                    model =AutoModelForQuestionAnswering.from_pretrained(modelname)
                    tokenizer = AutoTokenizer.from_pretrained(modelname)
                    from transformers import pipeline
                    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
                    model_answer=[]
                    question=[]
                    for questions in interviewer_question:
                        ans=nlp({'question':questions,'context': context})
                        start=ans['start']
                        end=ans['end']
                        answer=context[start:end+400] #increasing the length of the answer accordingly because model answers it in a summarized form
                        model_answers=answer
                        model_answers = model_answers.split('.') #restricting the answer when the sentence end 
                        model_answers = model_answers[0]#Taking the best answerfrom the model
                        model_answer.append(model_answers)
                        question.append(questions)
                    db = client[Domain] # use a database called "test_database"
                    collection = db.modelanswer   # and inside that DB, a collection called "files"
                    modelanswer = model_answer
                    text_file_doc = {"modelanswer": "modelanswer.txt", "contents" : modelanswer }
                    collection.insert(text_file_doc)
                    db = client[Domain] # use a database called "test_database"
                    collection = db.modelname # and inside that DB, a collection called "files"
                    model_name = modelname
                    text_file_doc = {"model_name": "model_name.txt", "contents" : model_name }
                    collection.insert(text_file_doc)
        elif track=='no':
            import pymongo
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client[Domain]
            col = db["corpus"]
            x = col.find()
            for string in x: 
                print(string)
            string=string['contents']
            db = client[Domain]
            col = db["modelname"]
            zp = col.find()
            for modelnamed in zp:
                print(modelnamed)
            modelpre=modelnamed['contents']
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client[Domain]
            col = db["question"]
            j = col.find() 
            for questions in j:
                print(questions)
            interviewer_quest=questions['contents']
            interviewer_quest=interviewer_quest.split(',')
            interviewer_question=[]
            for i in range(len(interviewer_quest)):
                interviewer_quest[i]=" ".join(interviewer_quest[i].split())
                interviewer_question.append(interviewer_quest[i])
            db = client[Domain]
            col = db["modelanswer"]
            zp = col.find()
            for modelanswer in zp:
                print(modelanswer)
            modelans=modelanswer['contents']
            if modelpre==modelname:
                 model_answer=modelans
            elif modelpre!=modelname:
                with put_loading(shape='border', color='success'):
                    import re
                    context=string.lower().strip()
                    context = re.sub('[^a-zA-Z0-9\s\.]', ' ', string)
                    context = ' '.join(context.split())
                    import pandas as pd
                    from transformers import AutoTokenizer, AutoModelForQuestionAnswering
                    model =AutoModelForQuestionAnswering.from_pretrained(modelname)
                    tokenizer = AutoTokenizer.from_pretrained(modelname)
                    from transformers import pipeline
                    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
                    model_answer=[]
                    question=[]
                    for questions in interviewer_question:
                        ans=nlp({'question':questions,'context': context})
                        start=ans['start']
                        end=ans['end']
                        answer=context[start:end+400] #increasing the length of the answer accordingly because model answers it in a summarized form
                        model_answers=answer
                        model_answers = model_answers.split('.') #restricting the answer when the sentence end 
                        model_answers = model_answers[0]#Taking the best answerfrom the model
                        model_answer.append(model_answers)
                        question.append(questions)
                    db = client[Domain] # use a database called "test_database"
                    collection = db.modelanswer   # and inside that DB, a collection called "files"
                    modelanswer = model_answer
                    text_file_doc = {"modelanswer": "modelanswer.txt", "contents" : modelanswer }
                    collection.insert(text_file_doc)
                    db = client[Domain] # use a database called "test_database"
                    collection = db.modelname # and inside that DB, a collection called "files"
                    model_name = modelname
                    text_file_doc = {"model_name": "model_name.txt", "contents" : model_name }
                    collection.insert(text_file_doc)
    Candidate_First=input("Enter Applicant First Name")
    Candidate_Second=input('Enter Applicant Last Name')
    moss=Candidate_First +'_' + Candidate_Second+'_'+Domain
    moss=moss.capitalize()
    if moss not in dbs:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[moss] # use a database called "test_database"
        collection = db.question   # and inside that DB, a collection called "files"
        text = file_upload("Upload Interview questions(Accepted format is .txt and Please Use Commar as a Seperator)", accept=".txt")
        text=text['content']
        text=text.decode('utf-8')
        text_file_doc = {"question": "question.txt", "contents" : text }
        collection.insert(text_file_doc)
        db = client[moss] # use a database called "test_database"
        collection = db.applicant   # and inside that DB, a collection called "files"
        text = file_upload("Upload Applicant Answers(Accepted format is .txt and Please Use Commar as a Seperator)", accept=".txt")
        text=text['content']
        text=text.decode('utf-8')
        text_file_doc = {"applicant": "applicant.txt", "contents" : text }
        collection.insert(text_file_doc)
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[moss]
        col = db["question"]
        y = col.find() 
        for question in y:
            print(question)
        evaluater_quest=question['contents']
        evaluater_quest=evaluater_quest.split(',')
        evaluater_question=[]
        for i in range(len(evaluater_quest)):
            evaluater_quest[i]=" ".join(evaluater_quest[i].split())
            evaluater_question.append(evaluater_quest[i])
        modelansw=[]
        for questions in evaluater_question:
            t=model_answer[interviewer_question.index(questions)]
            modelansw.append(t) 
        model_answer=modelansw
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[moss]
        col = db["applicant"]
        z = col.find()
        for answer in z:
            print(answer)
        applicant_answer=answer['contents']
        applicant_answer=applicant_answer.split(',')
        num=int(input('Number of Interviewer questions'))
        with put_loading(shape='border', color='success'):
            from sentence_transformers import SentenceTransformer
            from sklearn.metrics.pairwise import cosine_similarity
            model = SentenceTransformer('paraphrase-distilroberta-base-v2')
            result=[]
            score=[]
            for i in range(num):
                sentences=[model_answer[i],applicant_answer[i]]
                sentence_embeddings = model.encode(sentences)
                scores=cosine_similarity([sentence_embeddings[0]],sentence_embeddings[1:])*100
                if scores>35:
                    results='correct answer'
                else:
                    results='incorrect answer'
                result.append(results)
                score.append(scores)
            result=pd.Series(score)
            scored=result.loc[:].mean()
            if scored>35:
                style(put_text('WELL\nDONE!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
            else:
                style(put_text('Better Luck\nNext Time!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
            if scored>35:
                status='congratulations you have cleared the interview'
            else:
                status='sorry you have not cleared the interview'
            db = client[moss] # use a database called "test_database"
            collection = db.score   # and inside that DB, a collection called "files"
            text = scored[0,0]
            text=str(text)
            text_file_doc = {"score": "score.txt", "contents" : text }
            collection.insert(text_file_doc)
            db = client[moss] # use a database called "test_database"
            collection = db.numb   # and inside that DB, a collection called "files"
            numb = num
            numb=str(numb)
            text_file_doc = {"numb": "numb.txt", "contents" : numb }
            collection.insert(text_file_doc)
            style(put_text('your score is ' + str(scored[0,0]) +'% and '+ status), 'color:white; font-size: 30px; font-family: "Lucida Console"; font-weight: bold')
    else:
        trace=actions('Applicant name Already Exist You Want to Replace',['Yes','No'])
        trace=trace.lower()
        if trace=='yes':     
            import pymongo
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            database = client[moss]
            collection = database.collection_names(include_system_collections=False)
            if "numb" and "score"  in collection:
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client[moss]
                col = db["question"]
                j = col.find() 
                for questions in j:
                    print(questions)
                evaluater_quests=questions['contents']
                evaluater_quests=evaluater_quests.split(',')
                evaluater_questions=[]
                for i in range(len(evaluater_quests)):
                    evaluater_quests[i]=" ".join(evaluater_quests[i].split())
                    evaluater_questions.append(evaluater_quests[i])
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client[moss]
                col = db["applicant"]
                zo = col.find()
                for answers in zo:
                    print(answers)
                applicant_answers=answers['contents']
                applicant_answers=applicant_answers.split(',')
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client[moss]
                col = db["numb"]
                t = col.find() 
                for numb in t:
                    print(numb)
                numb=numb['contents'] 
                numb=int(numb)
                db = client[moss]
                col = db["score"]
                z = col.find()
                for score in z:
                    print(score)
                scoring=score['contents']
                scoring=float(scoring)
                num=int(input('Number of Interviewer questions'))
                #client.drop_database(moss)
                db = client[moss] # use a database called "test_database"
                collection = db.question   # and inside that DB, a collection called "files"
                text = file_upload("Upload Interview questions(Accepted format is .txt and Please Use Commar as a Seperator)", accept=".txt")
                text=text['content']
                text=text.decode('utf-8')
                text_file_doc = {"question": "question.txt", "contents" : text }
                collection.insert(text_file_doc)
                db = client[moss] # use a database called "test_database"
                collection = db.applicant   # and inside that DB, a collection called "files"
                text = file_upload("Upload Applicant Answers(Accepted format is .txt and Please Use Commar as a Seperator)", accept=".txt")
                text=text['content']
                text=text.decode('utf-8')
                text_file_doc = {"applicant": "applicant.txt", "contents" : text }
                collection.insert(text_file_doc)
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client[moss]
                col = db["question"]
                y = col.find() 
                for question in y:
                    print(question)
                evaluater_quest=question['contents']
                evaluater_quest=evaluater_quest.split(',')
                evaluater_question=[]
                for i in range(len(evaluater_quest)):
                    evaluater_quest[i]=" ".join(evaluater_quest[i].split())
                    evaluater_question.append(evaluater_quest[i])
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client[moss]
                col = db["applicant"]
                z = col.find()
                for answer in z:
                    print(answer)
                applicant_answer=answer['contents']
                applicant_answer=applicant_answer.split(',')
                if applicant_answer==applicant_answers and evaluater_question==evaluater_questions and modelpre==modelname:
                    if numb==num:
                        if scoring>35:  
                            style(put_text('WELL\nDONE!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                        else:
                            style(put_text('Better Luck\nNext Time!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                        if scoring>35:
                            status='congratulations you have cleared the interview'
                        else:
                            status='sorry you have not cleared the interview'
                        db = client[moss] # use a database called "test_database"
                        collection = db.score   # and inside that DB, a collection called "files"
                        text = scoring
                        text=str(text)
                        text_file_doc = {"score": "score.txt", "contents" : text }
                        collection.insert(text_file_doc)    
                        db = client[moss] # use a database called "test_database"
                        collection = db.numb   # and inside that DB, a collection called "files"
                        numb = num
                        numb=str(numb)
                        text_file_doc = {"numb": "numb.txt", "contents" : numb }
                        collection.insert(text_file_doc)
                        style(put_text('your score is ' + str(scoring) +'% and '+ status), 'color:white; font-size: 30px; font-family: "Lucida Console"; font-weight: bold')
                    elif numb!=num:
                        modelansw=[]
                        for questions in evaluater_question:
                            t=model_answer[interviewer_question.index(questions)]
                            modelansw.append(t) 
                        model_answer=modelansw
                        from sentence_transformers import SentenceTransformer
                        from sklearn.metrics.pairwise import cosine_similarity
                        model = SentenceTransformer('paraphrase-distilroberta-base-v2')
                        result=[]
                        score=[]
                        for i in range(num):
                            sentences=[model_answer[i],applicant_answer[i]]
                            sentence_embeddings = model.encode(sentences)
                            scores=cosine_similarity([sentence_embeddings[0]],sentence_embeddings[1:])*100
                            if scores>35:
                                results='correct answer'
                            else:
                                results='incorrect answer'
                            result.append(results)
                            score.append(scores)
                        result=pd.Series(score)
                        scored=result.loc[:].mean()
                        if scored>35:  
                            style(put_text('WELL\nDONE!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                        else:
                            style(put_text('Better Luck\nNext Time!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                        if scored>35:
                            status='congratulations you have cleared the interview'
                        else:
                            status='sorry you have not cleared the interview'
                        db = client[moss] # use a database called "test_database"
                        collection = db.score   # and inside that DB, a collection called "files"
                        text = scored[0,0]
                        text=str(text)
                        text_file_doc = {"score": "score.txt", "contents" : text }
                        collection.insert(text_file_doc)
                        db = client[moss] # use a database called "test_database"
                        collection = db.numb   # and inside that DB, a collection called "files"
                        numb = num
                        numb=str(numb)
                        text_file_doc = {"numb": "numb.txt", "contents" : numb }
                        collection.insert(text_file_doc)
                        style(put_text('your score is ' + str(scored[0,0]) +'% and '+ status), 'color:white; font-size: 30px; font-family: "Lucida Console"; font-weight: bold')
                elif applicant_answer!=applicant_answers and evaluater_question==evaluater_questions:
                    modelansw=[]
                    for questions in evaluater_question:
                        t=model_answer[interviewer_question.index(questions)]
                        modelansw.append(t) 
                    model_answer=modelansw
                    from sentence_transformers import SentenceTransformer
                    from sklearn.metrics.pairwise import cosine_similarity
                    model = SentenceTransformer('paraphrase-distilroberta-base-v2')
                    result=[]
                    score=[]
                    for i in range(num):
                        sentences=[model_answer[i],applicant_answer[i]]
                        sentence_embeddings = model.encode(sentences)
                        scores=cosine_similarity([sentence_embeddings[0]],sentence_embeddings[1:])*100
                        if scores>35:
                            results='correct answer'
                        else:
                            results='incorrect answer'
                        result.append(results)
                        score.append(scores)
                    result=pd.Series(score)
                    scored=result.loc[:].mean()
                    if scored>35:  
                        style(put_text('WELL\nDONE!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                    else:
                        style(put_text('Better Luck\nNext Time!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                    if scored>35:
                        status='congratulations you have cleared the interview'
                    else:
                        status='sorry you have not cleared the interview'
                    db = client[moss] # use a database called "test_database"
                    collection = db.score   # and inside that DB, a collection called "files"
                    text = scored[0,0]
                    text=str(text)
                    text_file_doc = {"score": "score.txt", "contents" : text }
                    collection.insert(text_file_doc)
                    db = client[moss] # use a database called "test_database"
                    collection = db.numb   # and inside that DB, a collection called "files"
                    numb = num
                    numb=str(numb)
                    text_file_doc = {"numb": "numb.txt", "contents" : numb }
                    collection.insert(text_file_doc)
                    style(put_text('your score is ' + str(scored[0,0]) +'% and '+ status), 'color:white; font-size: 30px; font-family: "Lucida Console"; font-weight: bold')
                elif applicant_answer!=applicant_answers and evaluater_question!=evaluater_questions:
                    with put_loading(shape='border', color='success'):
                        modelansw=[]
                        for questions in evaluater_question:
                            t=model_answer[interviewer_question.index(questions)]
                            modelansw.append(t) 
                        model_answer=modelansw
                        from sentence_transformers import SentenceTransformer
                        from sklearn.metrics.pairwise import cosine_similarity
                        model = SentenceTransformer('paraphrase-distilroberta-base-v2')
                        result=[]
                        score=[]
                        for i in range(num):
                            sentences=[model_answer[i],applicant_answer[i]]
                            sentence_embeddings = model.encode(sentences)
                            scores=cosine_similarity([sentence_embeddings[0]],sentence_embeddings[1:])*100
                            if scores>35:
                                results='correct answer'
                            else:
                                results='incorrect answer'
                            result.append(results)
                            score.append(scores)
                        result=pd.Series(score)
                        scored=result.loc[:].mean()
                        if scored>35:  
                            style(put_text('WELL\nDONE!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                        else:
                            style(put_text('Better Luck\nNext Time!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                        if scored>35:
                            status='congratulations you have cleared the interview'
                        else:
                            status='sorry you have not cleared the interview'
                        db = client[moss] # use a database called "test_database"
                        collection = db.score   # and inside that DB, a collection called "files"
                        text = scored[0,0]
                        text=str(text)
                        text_file_doc = {"score": "score.txt", "contents" : text }
                        collection.insert(text_file_doc)
                        db = client[moss] # use a database called "test_database"
                        collection = db.numb   # and inside that DB, a collection called "files"
                        numb = num
                        numb=str(numb)
                        text_file_doc = {"numb": "numb.txt", "contents" : numb }
                        collection.insert(text_file_doc)
                        style(put_text('your score is ' + str(scored[0,0]) +'% and '+ status), 'color:white; font-size: 30px; font-family: "Lucida Console"; font-weight: bold')
                else:    
                    with put_loading(shape='border', color='success'):
                        modelansw=[]
                        for questions in evaluater_question:
                            t=model_answer[interviewer_question.index(questions)]
                            modelansw.append(t) 
                        model_answer=modelansw
                        from sentence_transformers import SentenceTransformer
                        from sklearn.metrics.pairwise import cosine_similarity
                        model = SentenceTransformer('paraphrase-distilroberta-base-v2')
                        result=[]
                        score=[]
                        for i in range(num):
                            sentences=[model_answer[i],applicant_answer[i]]
                            sentence_embeddings = model.encode(sentences)
                            scores=cosine_similarity([sentence_embeddings[0]],sentence_embeddings[1:])*100
                            if scores>35:
                                results='correct answer'
                            else:
                                results='incorrect answer'
                            result.append(results)
                            score.append(scores)
                        result=pd.Series(score)
                        scored=result.loc[:].mean()
                        if scored>35:  
                            style(put_text('WELL\nDONE!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                        else:
                            style(put_text('Better Luck\nNext Time!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                        if scored>35:
                            status='congratulations you have cleared the interview'
                        else:
                            status='sorry you have not cleared the interview'
                        db = client[moss] # use a database called "test_database"
                        collection = db.score   # and inside that DB, a collection called "files"
                        text = scored[0,0]
                        text=str(text)
                        text_file_doc = {"score": "score.txt", "contents" : text }
                        collection.insert(text_file_doc)
                        db = client[moss] # use a database called "test_database"
                        collection = db.numb   # and inside that DB, a collection called "files"
                        numb = num
                        numb=str(numb)
                        text_file_doc = {"numb": "numb.txt", "contents" : numb }
                        collection.insert(text_file_doc)
                        style(put_text('your score is ' + str(scored[0,0]) +'% and '+ status), 'color:white; font-size: 30px; font-family: "Lucida Console"; font-weight: bold')
            elif "numb" and "score"  not in collection:
                db = client[moss] # use a database called "test_database"
                collection = db.question   # and inside that DB, a collection called "files"
                text = file_upload("Upload Interview questions(Accepted format is .txt and Please Use Commar as a Seperator)", accept=".txt")
                text=text['content']
                text=text.decode('utf-8')
                text_file_doc = {"question": "question.txt", "contents" : text }
                collection.insert(text_file_doc)
                db = client[moss] # use a database called "test_database"
                collection = db.applicant   # and inside that DB, a collection called "files"
                text = file_upload("Upload Applicant Answers(Accepted format is .txt and Please Use Commar as a Seperator)", accept=".txt")
                text=text['content']
                text=text.decode('utf-8')
                text_file_doc = {"applicant": "applicant.txt", "contents" : text }
                collection.insert(text_file_doc)
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client[moss]
                col = db["question"]
                y = col.find() 
                for question in y:
                    print(question)
                evaluater_quest=question['contents']
                evaluater_quest=evaluater_quest.split(',')
                evaluater_question=[]
                for i in range(len(evaluater_quest)):
                    evaluater_quest[i]=" ".join(evaluater_quest[i].split())
                    evaluater_question.append(evaluater_quest[i])
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client[moss]
                col = db["applicant"]
                z = col.find()
                for answer in z:
                    print(answer)
                applicant_answer=answer['contents']
                applicant_answer=applicant_answer.split(',')
                num=int(input('Number of Interviewer questions'))
                with put_loading(shape='border', color='success'):
                    modelansw=[]
                    for questions in evaluater_question:
                        t=model_answer[interviewer_question.index(questions)]
                        modelansw.append(t) 
                    model_answer=modelansw
                    from sentence_transformers import SentenceTransformer
                    from sklearn.metrics.pairwise import cosine_similarity
                    model = SentenceTransformer('paraphrase-distilroberta-base-v2')
                    result=[]
                    score=[]
                    for i in range(num):
                        sentences=[model_answer[i],applicant_answer[i]]
                        sentence_embeddings = model.encode(sentences)
                        scores=cosine_similarity([sentence_embeddings[0]],sentence_embeddings[1:])*100
                        if scores>35:
                            results='correct answer'
                        else:
                            results='incorrect answer'
                        result.append(results)
                        score.append(scores)
                    result=pd.Series(score)
                    scored=result.loc[:].mean()
                    if scored>35:
                        style(put_text('WELL\nDONE!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                    else:
                        style(put_text('Better Luck\nNext Time!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                    if scored>35:
                        status='congratulations you have cleared the interview'
                    else:
                        status='sorry you have not cleared the interview'
                    db = client[moss] # use a database called "test_database"
                    collection = db.score   # and inside that DB, a collection called "files"
                    text = scored[0,0]
                    text=str(text)
                    text_file_doc = {"score": "score.txt", "contents" : text }
                    collection.insert(text_file_doc)
                    db = client[moss] # use a database called "test_database"
                    collection = db.numb   # and inside that DB, a collection called "files"
                    numb = num
                    numb=str(numb)
                    text_file_doc = {"numb": "numb.txt", "contents" : numb }
                    collection.insert(text_file_doc)
                    style(put_text('your score is ' + str(scored[0,0]) +'% and '+ status), 'color:white; font-size: 30px; font-family: "Lucida Console"; font-weight: bold')
        elif trace=='no':
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            database = client[moss]
            collection = database.collection_names(include_system_collections=False)
            num=int(input('Number of Interviewer questions'))
            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client[moss]
            col = db["question"]
            y = col.find() 
            for question in y:
                print(question)
            evaluater_quest=question['contents']
            evaluater_quest=evaluater_quest.split(',')
            evaluater_question=[]
            for i in range(len(evaluater_quest)):
                evaluater_quest[i]=" ".join(evaluater_quest[i].split())
                evaluater_question.append(evaluater_quest[i])
            if "numb" and "score"  in collection:
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client[moss]
                col = db["applicant"]
                z = col.find()
                for answer in z:
                    print(answer)
                applicant_answer=answer['contents']
                applicant_answer=applicant_answer.split(',')
                db = client[moss]
                col = db["numb"]
                t = col.find() 
                for numb in t:
                    print(numb)
                numb=numb['contents'] 
                numb=int(numb)
                db = client[moss]
                col = db["score"]
                z = col.find()
                for score in z:
                    print(score)
                scoring=score['contents']
                scoring=float(scoring)
                if numb==num and  modelpre==modelname:
                    if scoring>35:  
                        style(put_text('WELL\nDone!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                    else:
                        style(put_text('Better Luck\nNext Time!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                    if scoring>35:
                        status='congratulations you have cleared the interview'
                    else:
                        status='sorry you have not cleared the interview'
                    db = client[moss] # use a database called "test_database"
                    collection = db.score   # and inside that DB, a collection called "files"
                    text = scoring
                    text=str(text)
                    text_file_doc = {"score": "score.txt", "contents" : text }
                    collection.insert(text_file_doc)    
                    db = client[moss] # use a database called "test_database"
                    collection = db.numb   # and inside that DB, a collection called "files"
                    numb = num
                    numb=str(numb)
                    text_file_doc = {"numb": "numb.txt", "contents" : numb }
                    collection.insert(text_file_doc)
                    style(put_text('your score is ' + str(scoring) +'% and '+ status), 'color:white; font-size: 30px; font-family: "Lucida Console"; font-weight: bold')
                elif numb!=num:
                    modelansw=[]
                    for questions in evaluater_question:
                        t=model_answer[interviewer_question.index(questions)]
                        modelansw.append(t) 
                    model_answer=modelansw
                    from sentence_transformers import SentenceTransformer
                    from sklearn.metrics.pairwise import cosine_similarity
                    model = SentenceTransformer('paraphrase-distilroberta-base-v2')
                    result=[]
                    score=[]
                    for i in range(num):
                        sentences=[model_answer[i],applicant_answer[i]]
                        sentence_embeddings = model.encode(sentences)
                        scores=cosine_similarity([sentence_embeddings[0]],sentence_embeddings[1:])*100
                        if scores>35:
                            results='correct answer'
                        else:
                            results='incorrect answer'
                        result.append(results)
                        score.append(scores)
                    result=pd.Series(score)
                    scored=result.loc[:].mean()
                    if scored>35:  
                        style(put_text('WELL\nDONE!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                    else:
                        style(put_text('Better Luck\nNext Time!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                    if scored>35:
                        status='congratulations you have cleared the interview'
                    else:
                        status='sorry you have not cleared the interview'
                    db = client[moss] # use a database called "test_database"
                    collection = db.score   # and inside that DB, a collection called "files"
                    text = scored[0,0]
                    text=str(text)
                    text_file_doc = {"score": "score.txt", "contents" : text }
                    collection.insert(text_file_doc)
                    db = client[moss] # use a database called "test_database"
                    collection = db.numb   # and inside that DB, a collection called "files"
                    numb = num
                    numb=str(numb)
                    text_file_doc = {"numb": "numb.txt", "contents" : numb }
                    collection.insert(text_file_doc)
                    style(put_text('your score is ' + str(scored[0,0]) +'% and '+ status), 'color:white; font-size: 30px; font-family: "Lucida Console"; font-weight: bold')
                else:
                    client = pymongo.MongoClient("mongodb://localhost:27017/")
                    db = client[moss]
                    col = db["question"]
                    y = col.find() 
                    for question in y:
                        print(question)
                    evaluater_quest=question['contents']
                    evaluater_quest=evaluater_quest.split(',')
                    evaluater_question=[]
                    for i in range(len(evaluater_quest)):
                        evaluater_quest[i]=" ".join(evaluater_quest[i].split())
                        evaluater_question.append(evaluater_quest[i])
                    client = pymongo.MongoClient("mongodb://localhost:27017/")
                    db = client[moss]
                    col = db["applicant"]
                    z = col.find()
                    for answer in z:
                        print(answer)
                    applicant_answer=answer['contents']
                    applicant_answer=applicant_answer.split(',')
                    with put_loading(shape='border', color='success'):
                        modelansw=[]
                        for questions in evaluater_question:
                            t=model_answer[interviewer_question.index(questions)]
                            modelansw.append(t) 
                        model_answer=modelansw
                        from sentence_transformers import SentenceTransformer
                        from sklearn.metrics.pairwise import cosine_similarity
                        model = SentenceTransformer('paraphrase-distilroberta-base-v2')
                        result=[]
                        score=[]
                        for i in range(num):
                            sentences=[model_answer[i],applicant_answer[i]]
                            sentence_embeddings = model.encode(sentences)
                            scores=cosine_similarity([sentence_embeddings[0]],sentence_embeddings[1:])*100
                            if scores>35:
                                results='correct answer'
                            else:
                                results='incorrect answer'
                            result.append(results)
                            score.append(scores)
                        result=pd.Series(score)
                        scored=result.loc[:].mean()
                        if scored>35:
                            style(put_text('WELL\nDONE!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                        else:
                            style(put_text('Better Luck\nNext Time!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                        if scored>35:
                            status='congratulations you have cleared the interview'
                        else:
                            status='sorry you have not cleared the interview'
                        db = client[moss] # use a database called "test_database"
                        collection = db.score   # and inside that DB, a collection called "files"
                        text = scored[0,0]
                        text=str(text)
                        text_file_doc = {"score": "score.txt", "contents" : text }
                        collection.insert(text_file_doc)
                        db = client[moss] # use a database called "test_database"
                        collection = db.numb   # and inside that DB, a collection called "files"
                        numb = num
                        numb=str(numb)
                        text_file_doc = {"numb": "numb.txt", "contents" : numb }
                        collection.insert(text_file_doc)
                        style(put_text('your score is ' + str(scored[0,0]) +'% and '+ status), 'color:white; font-size: 30px; font-family: "Lucida Console"; font-weight: bold')
            elif "numb" and "score" not in collection:
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client[moss]
                col = db["question"]
                y = col.find() 
                for question in y:
                    print(question)
                evaluater_quest=question['contents']
                evaluater_quest=evaluater_quest.split(',')
                evaluater_question=[]
                for i in range(len(evaluater_quest)):
                    evaluater_quest[i]=" ".join(evaluater_quest[i].split())
                    evaluater_question.append(evaluater_quest[i])
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client[moss]
                col = db["applicant"]
                z = col.find()
                for answer in z:
                    print(answer)
                applicant_answer=answer['contents']
                applicant_answer=applicant_answer.split(',')
                with put_loading(shape='border', color='success'):
                    modelansw=[]
                    for questions in evaluater_question:
                        t=model_answer[interviewer_question.index(questions)]
                        modelansw.append(t) 
                    model_answer=modelansw
                    from sentence_transformers import SentenceTransformer
                    from sklearn.metrics.pairwise import cosine_similarity
                    model = SentenceTransformer('paraphrase-distilroberta-base-v2')
                    result=[]
                    score=[]
                    for i in range(num):
                        sentences=[model_answer[i],applicant_answer[i]]
                        sentence_embeddings = model.encode(sentences)
                        scores=cosine_similarity([sentence_embeddings[0]],sentence_embeddings[1:])*100
                        if scores>35:
                            results='correct answer'
                        else:
                            results='incorrect answer'
                        result.append(results)
                        score.append(scores)
                    result=pd.Series(score)
                    scored=result.loc[:].mean()
                    if scored>35:
                        style(put_text('WELL\nDONE!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                    else:
                        style(put_text('Better Luck\nNext Time!'),"text-align:center;color:white; color:#f61620; font-size: 52px; padding: 4px 200px;font-style:italic; font-weight: 900")
                    if scored>35:
                        status='congratulations you have cleared the interview'
                    else:
                        status='sorry you have not cleared the interview'
                    db = client[moss] # use a database called "test_database"
                    collection = db.score   # and inside that DB, a collection called "files"
                    text = scored[0,0]
                    text=str(text)
                    text_file_doc = {"score": "score.txt", "contents" : text }
                    collection.insert(text_file_doc)
                    db = client[moss] # use a database called "test_database"
                    collection = db.numb   # and inside that DB, a collection called "files"
                    numb = num
                    numb=str(numb)
                    text_file_doc = {"numb": "numb.txt", "contents" : numb }
                    collection.insert(text_file_doc)
                    style(put_text('your score is ' + str(scored[0,0]) +'% and '+ status), 'color:white; font-size: 30px; font-family: "Lucida Console"; font-weight: bold')
        

#model()
app.add_url_rule('/tool','webio_view',webio_view(model),methods=['GET','POST','OPTIONS'])

app.run(host='127.0.0.1',port=8000)
