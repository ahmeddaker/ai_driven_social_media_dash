import json
import urllib.parse
import boto3
import uuid

print('Loading function')

s3 = boto3.client('s3')
comprehend = boto3.client("comprehend", region_name="us-east-1")
firehose = boto3.client('firehose')


def analysisWithComprehend(text, id):
    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    retrObject = {}
    retrObject["uuid"] = id
    retrObject["Sentiment"] = response['Sentiment']
    retrObject["SentimentScore"] = response['SentimentScore']
    return retrObject


def stringfyJson(jsonArr):
    '''
    arguments : jsonArr
    return string of jsonDumb
    '''
    strJson = ''
    for item in jsonArr:
        strJson += str(json.dumps(item)+'\n')
    # print(strJson)
    return strJson


def putRecordsOnStream(sentimentAnalysisData):
    recordsOfString = stringfyJson(sentimentAnalysisData)

    response = firehose.put_record(DeliveryStreamName='LAMBDA_STREAMS_S3', Record={
        'Data': recordsOfString
    })
    print(json.dumps(response))


def lambda_handler(event, context):

    # Get the object from the event and show its content type
    fileObj = event['Records'][0]
    fileName = fileObj['s3']['bucket']['name']

    # set up the key
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print(key)
    try:
        fileObj = s3.get_object(Bucket=fileName, Key=key)
        fileContent = fileObj['Body'].read().decode('UTF-8')
        jsonFileContentString = fileContent.split(
            '\n')  # json.loads(s) for s in
        jsonFileContent = []
        try:
            for js in jsonFileContentString:
                jsonFileContent.append(eval(js))
        except:
            pass
        print("len is:", len(jsonFileContent))
        # print(jsonFileContent[0]['text'])
        # print(analysisWithComprehend(jsonFileContent[0]['text']))

        sentimentAnalysisData = []

        for item in jsonFileContent:
            sentimentAnalysisData.append(
                analysisWithComprehend(item["text"], item["uuid"]))

        print(len(sentimentAnalysisData))
        # print(sentimentAnalysisData[4])
        putRecordsOnStream(sentimentAnalysisData)

        print("CONTENT TYPE: " + fileObj['ContentType'])
        return fileObj['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, fileName))
        raise e
