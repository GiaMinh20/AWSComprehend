import  tkinter as tk
from tkinter import ttk
from tkinter import *
import boto3
import pandas as pd
import  datetime
root = tk.Tk()
root.geometry("830x830")
root.title("Sentiment Analysis")
root.iconbitmap("icons8-align-text-left-48.ico")
root.configure(bg='#b0bec5')

labelRequest =Label(root,bg='#b0bec5',text="Write your text", font=("Arial", 16))
labelRequest.place(x=10,y=10)
textInput = tk.Text(root,height=9, width=75)
textInput.place(x=200,y=10)

labbelSentimentTitle = Label(root,bg='#b0bec5', text="LanguageCode: ", font=("Arial", 16))
labbelSentimentTitle.place(x=10, y=170)

labbelSentimentTitle = Label(root,bg='#b0bec5', text="Sentiment: ", font=("Arial", 16))
labbelSentimentTitle.place(x=10, y=200)
labbelSentimentTitle = Label(root,bg='#b0bec5', text="Sentiment Score: ", font=("Arial", 16))
labbelSentimentTitle.place(x=10, y=230)

labbelKeyPhrasesTitle = Label(root,bg='#b0bec5', text="Key phrases: ", font=("Arial", 16))
labbelKeyPhrasesTitle.place(x=10, y=400)
treeKey = ttk.Treeview(root, column=("c1", "c2", "c3"), show='headings', height=5)
treeKey.column("# 1", anchor=CENTER, width=400)
treeKey.heading("# 1", text="Key phrases")
treeKey.column("# 2", anchor=CENTER, width=100)
treeKey.heading("# 2", text="BeginOffset")
treeKey.column("# 3", anchor=CENTER, width=100)
treeKey.heading("# 3", text="EndOffset")
treeKey.place(x=200,y=400)

labbelSyntaxTitle = Label(root,bg='#b0bec5', text="Syntax: ", font=("Arial", 16))
labbelSyntaxTitle.place(x=10, y=680)
treeSyntax = ttk.Treeview(root, column=("c1", "c2", "c3","c4"), show='headings', height=5)
treeSyntax.column("# 1", anchor=CENTER, width=200)
treeSyntax.heading("# 1", text="Word")
treeSyntax.column("# 2", anchor=CENTER, width=200)
treeSyntax.heading("# 2", text="Part of speech")
treeSyntax.column("# 3", anchor=CENTER, width=100)
treeSyntax.heading("# 3", text="BeginOffset")
treeSyntax.column("# 4", anchor=CENTER, width=100)
treeSyntax.heading("# 4", text="EndOffset")
treeSyntax.place(x=200,y=680)

labbelPIITitle = Label(root,bg='#b0bec5', text="PII: ", font=("Arial", 16))
labbelPIITitle.place(x=10, y=540)
treePII = ttk.Treeview(root, column=("c1", "c2", "c3"), show='headings', height=5)
treePII.column("# 1", anchor=CENTER, width=400)
treePII.heading("# 1", text="Type")
treePII.column("# 2", anchor=CENTER, width=100)
treePII.heading("# 2", text="BeginOffset")
treePII.column("# 3", anchor=CENTER, width=100)
treePII.heading("# 3", text="EndOffset")
treePII.place(x=200,y=540)

labbelEntityTitle = Label(root,bg='#b0bec5', text="Entities: ", font=("Arial", 16))
labbelEntityTitle.place(x=10, y=260)
treeEntity = ttk.Treeview(root, column=("c1", "c2", "c3","c4"), show='headings', height=5)
treeEntity.column("# 1", anchor=CENTER, width=300)
treeEntity.heading("# 1", text="Entity")
treeEntity.column("# 2", anchor=CENTER, width=100)
treeEntity.heading("# 2", text="Type")
treeEntity.column("# 3", anchor=CENTER, width=100)
treeEntity.heading("# 3", text="BeginOffset")
treeEntity.column("# 4", anchor=CENTER, width=100)
treeEntity.heading("# 4", text="EndOffset")
treeEntity.place(x=200,y=260)

pd.set_option('display.max_rows', None)
def Insert_row(row_number, df, row_value):
    # Starting value of upper half
    start_upper = 0
    # End value of upper half
    end_upper = row_number
    # Start value of lower half
    start_lower = row_number
    # End value of lower half
    end_lower = df.shape[0]
    # Create a list of upper_half index
    upper_half = [*range(start_upper, end_upper, 1)]
    # Create a list of lower_half index
    lower_half = [*range(start_lower, end_lower, 1)]
    # Increment the value of lower half by 1
    lower_half = [x.__add__(1) for x in lower_half]
    # Combine the two lists
    index_ = upper_half + lower_half
    # Update the index of the dataframe
    df.index = index_
    # Insert a row at the end
    df.loc[row_number] = row_value
    # Sort the index labels
    df = df.sort_index()
    # return the dataframe
    return df

def getText():
    clear()
    time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

    aws_mag_console = boto3.session.Session(profile_name="GiaMinh")
    client= aws_mag_console.client(service_name='comprehend', region_name="us-east-2")

    f = open(f"Document_{time}.txt", "w+")
    result = textInput.get("1.0", "end")
    print(result, file=f)
    f.close()
    response = client.detect_dominant_language(
        Text=result
    )

    for lg in response['Languages']:
        languageCode = lg['LanguageCode']
    labbelLanguageCode = Label(root, bg='#b0bec5', text=languageCode, font=("Arial", 13))
    labbelLanguageCode.place(x=200, y=170)

    response1 = client.detect_sentiment(
        Text=result,
        LanguageCode=languageCode
    )
    dataSentiment =[]
    dfSentiment = pd.DataFrame.from_records(dataSentiment, columns=['LanguageCode', 'Sentiment', 'Posivite', 'Negative', 'Neutral', 'Mixed'])
    sentiment = response1['Sentiment']
    scoreAll = response1['SentimentScore']
    inputSentiment = [languageCode, sentiment, scoreAll['Positive'], scoreAll['Negative'], scoreAll['Neutral'], scoreAll['Mixed']]
    dfSentiment = Insert_row(0,dfSentiment,inputSentiment)
    dfSentiment.to_csv(rf'Sentiment_{time}.csv', index = False,header=True)

    if sentiment == "NEUTRAL":
        labbelSentiment = Label(root, bg='#b0bec5', text=sentiment, font=("Arial", 13), fg="yellow")
        score = scoreAll['Neutral']
    elif sentiment == "POSITIVE":
        labbelSentiment = Label(root, bg='#b0bec5', text=sentiment, font=("Arial", 13), fg="green")
        score = scoreAll['Positive']
    elif sentiment == "NEGATIVE":
        labbelSentiment = Label(root, bg='#b0bec5', text=sentiment, font=("Arial", 13), fg="red")
        score = scoreAll['Negative']
    elif sentiment == "MIXED":
        labbelSentiment = Label(root, bg='#b0bec5', text=sentiment, font=("Arial", 13), fg="purple")
        score = scoreAll['Mixed']
    labbelSentiment.place(x=200,y=200)
    labbelSentimentScore = Label(root,bg='#b0bec5', text=score, font=("Arial", 13))
    labbelSentimentScore.place(x=200, y=230)

    response2 = client.detect_key_phrases(
    Text=result,
    LanguageCode=languageCode
    )

    dataKeyPhrases = []
    dfKeyPhrases = pd.DataFrame.from_records(dataKeyPhrases, columns=['Text', 'BeginOffset', 'EndOffset'])
    for ph in response2['KeyPhrases']:
        treeKey.insert('', 'end', text="1", values=(ph['Text'], ph['BeginOffset'],ph['EndOffset']))
        inputKeyPhrases = [ph['Text'], ph['BeginOffset'],ph['EndOffset']]
        dfKeyPhrases = Insert_row(0, dfKeyPhrases, inputKeyPhrases)

    dfKeyPhrases.to_csv(rf'KeyPhrases_{time}.csv', index = False,header=True)

    response3 = client.detect_syntax(
    Text=result,
    LanguageCode=languageCode
    )

    dataSyntax = []
    dfSyntax = pd.DataFrame.from_records(dataSyntax, columns=['Text','Tag', 'BeginOffset', 'EndOffset'])
    for st in response3['SyntaxTokens']:
        partOfSpeech = st['PartOfSpeech']
        treeSyntax.insert('', 'end', text="1", values=(st['Text'],partOfSpeech['Tag'] ,st['BeginOffset'],st['EndOffset']))
        inputSyntax = [st['Text'],partOfSpeech['Tag'] ,st['BeginOffset'],st['EndOffset']]
        dfSyntax = Insert_row(0, dfSyntax, inputSyntax)

    dfSyntax.to_csv(rf'Syntax_{time}.csv', index = False,header=True)

    response4 = client.detect_pii_entities(
    Text=result,
    LanguageCode=languageCode
    )
    dataPII=[]
    dfPII = pd.DataFrame.from_records(dataPII, columns=['Type', 'BeginOffset', 'EndOffset'])
    for pii in response4['Entities']:
        treePII.insert('', 'end', text="1", values=(pii['Type'], pii['BeginOffset'],pii['EndOffset']))
        inputPII = [pii['Type'], pii['BeginOffset'], pii['EndOffset']]
        dfPII = Insert_row(0,dfPII,inputPII)

    dfPII.to_csv(rf'PII_{time}.csv', index = False,header=True)

    dataEntities = []
    dfEntities = pd.DataFrame.from_records(dataEntities, columns=['Text','Type', 'BeginOffset', 'EndOffset'])
    response5 = client.detect_entities(
    Text=result,
    LanguageCode=languageCode
    )

    for entity in response5['Entities']:
        treeEntity.insert('', 'end', text="1", values=(entity['Text'], entity['Type'], entity['BeginOffset'], entity['EndOffset']))
        inputEntity = [entity['Text'], entity['Type'], entity['BeginOffset'], entity['EndOffset']]
        dfEntities = Insert_row(0, dfEntities, inputEntity)
    dfEntities.to_csv(rf'Entities_{time}.csv', index = False,header=True)

    s3 = aws_mag_console.client(service_name='s3', region_name="us-east-2")
    s3.upload_file(f'Document_{time}.txt','comprehend2021-2022',f'Document_date_{time}.txt')
    s3.upload_file(f'Entities_{time}.csv', 'comprehend2021-2022', f'Entities_date_{time}.csv')
    s3.upload_file(f'Sentiment_{time}.csv', 'comprehend2021-2022', f'Sentiment_date_{time}.csv')
    s3.upload_file(f'PII_{time}.csv', 'comprehend2021-2022', f'PII_date_{time}.csv')
    s3.upload_file(f'Syntax_{time}.csv', 'comprehend2021-2022', f'Syntax_date_{time}.csv')
    s3.upload_file(f'KeyPhrases_{time}.csv', 'comprehend2021-2022', f'KeyPhrases_date_{time}.csv')

def clear():
    for i in treePII.get_children():
        treePII.delete(i)
    for ii in treeKey.get_children():
        treeKey.delete(ii)
    for iii in treeEntity.get_children():
        treeEntity.delete(iii)
    for iiii in treeSyntax.get_children():
        treeSyntax.delete(iiii)


btnRead = tk.Button(root, height=1, width=10, text="Analyze", command= getText)
btnRead.place(x=10,y=50)
root.mainloop()