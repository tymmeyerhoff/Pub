import os
import nexmo


def hangup(config,UUID):
    API_KEY = config['API_KEY']
    API_SECRET = config['API_SECRET']
    APPLICATION_ID = config['APPLICATION_ID']
    PRIVATE_KEY = open(config['PRIVATE_KEY'], 'r').read()
    TO_NUMBER = config['TO_NUMBER']
    FROM_NUMBER = config['FROM_NUMBER']

    client = nexmo.Client(
        key=API_KEY,
        secret=API_SECRET,
        application_id=APPLICATION_ID,
        private_key=PRIVATE_KEY
    )

    response = client.update_call(UUID, action='hangup')

    return response

def call(config):
    API_KEY = config['API_KEY']
    API_SECRET = config['API_SECRET']
    APPLICATION_ID = config['APPLICATION_ID']
    PRIVATE_KEY = open(config['PRIVATE_KEY'], 'r').read()
    TO_NUMBER = config['TO_NUMBER']
    FROM_NUMBER = config['FROM_NUMBER']
    
    client = nexmo.Client(
        key=API_KEY,
        secret=API_SECRET,
        application_id=APPLICATION_ID,
        private_key=PRIVATE_KEY
    )

    response = client.create_call({
      'to': [{'type': 'phone', 'number': TO_NUMBER}],
      'from': {'type': 'phone', 'number': FROM_NUMBER},
      'answer_url': ['https://nexmo-community.github.io/ncco-examples/first_call_talk.json']
    })

    return response


def obcall(config,TO_NUMBER,FROM_NUMBER):
    API_KEY = config['API_KEY']
    API_SECRET = config['API_SECRET']
    APPLICATION_ID = config['APPLICATION_ID']
    PRIVATE_KEY = open(config['PRIVATE_KEY'], 'r').read()

    client = nexmo.Client(
        key=API_KEY,
        secret=API_SECRET,
        application_id=APPLICATION_ID,
        private_key=PRIVATE_KEY
    )

    response = client.create_call({
        'to': [{'type': 'websocket', 'uri': 'ws://18.210.138.152:3000/server/9579'}],
      'from': {'type': 'phone', 'number': FROM_NUMBER},
      'answer_url': ['http://18.210.138.152:3001/wsanswer']
    })

    return response

def wscall(config,TO_NUMBER,FROM_NUMBER,PIN,UUID,DIRECTION):
    API_KEY = config['API_KEY']
    API_SECRET = config['API_SECRET']
    APPLICATION_ID = config['APPLICATION_ID']
    PRIVATE_KEY = open(config['PRIVATE_KEY'], 'r').read()
    CALLER_ID = '17327880638'
    client = nexmo.Client(
        key=API_KEY,
        secret=API_SECRET,
        application_id=APPLICATION_ID,
        private_key=PRIVATE_KEY
    )

    websocket = 'ws://18.210.138.152:3000/server/' + PIN
    response = client.create_call({
      'to': [{'type': 'websocket', 'uri': websocket }],
      'from': {'type': 'phone', 'number': TO_NUMBER},
      'answer_url': ['http://18.210.138.152:3001/wspin'],
    })
    print "GOT ws call"
    print str(response)
    print "AND!!!"
    print response['uuid']
    return response

