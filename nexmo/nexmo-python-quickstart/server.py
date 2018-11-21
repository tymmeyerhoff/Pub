from flask import Flask, jsonify, request

app = Flask(__name__)
app.config.from_pyfile('.env')

import sms
import voice
import nexmo
import time

@app.route("/sms/send")
def sms_send():
    return jsonify(sms.send(app.config))

@app.route("/voice/call")
def call():
    return jsonify(voice.call(app.config))


@app.route("/hangup")
def hangup_call():
    try:
      uuid = request.args.get('uuid')
    except:
      return "Invalid Args", 500
    else:
      return jsonify(voice.hangup(app.config, uuid))
    

@app.route("/inbound/sms", methods=['POST'])
def inboundsms():
    data = request.get_json(silent=True)
    print data
    return "success"


@app.route("/event", methods=['POST'])
def voiceevent():
    data = request.get_json(silent=True)
    print data
    return "success"


@app.route("/wspin")
def wspin():
    print "processing answer from ws call"
    for param_key, param_value in request.args.items():
        print("{}: {}".format(param_key, param_value))

    try:
      from_ = request.args.get('from')
      to_ = request.args.get('to')
      uuid_ = request.args.get('conversation_uuid')
      status_ = request.args.get('status')
    except:
      return "Invalid Args", 500
    else:
        ncco = [
            {
                "action": "connect",
                "timeout": "60",
                "from": "17322681124",
                "eventUrl": ["http://18.210.138.152:3001/event"],
                "endpoint": [
                 {
                   "type": "phone",
                   "number": from_,
                 }
               ]
            }
        ]
        return jsonify(ncco)


@app.route("/wsanswer")
def ws_answer():

    ncco = [
        {
            "action": "connect",
            "timeout": "60",
            "from": "17327880638",
            "eventUrl": ["http://18.210.138.152:3001/event"],
            "endpoint": [
             {
               "type": "phone",
               "number": "17322681124",
               "dtmfAnswer": "pp3029"
             }
           ]
        }

    ]
    print "sending! "
    print jsonify(ncco)
    return jsonify(ncco)


@app.route("/answer")
def answer_call():

    ncco = [
        {
            "action": "talk",
            "text": "Thank you for calling from yourself this is a test",
            "voiceName": "Amy"
        },
        {
            "action": "input",
            "submitOnHash": "true",
            "eventUrl": ["http://18.210.138.152:3000/event"]
        }

    ]
    print "sending! "
    print jsonify(ncco)
    return jsonify(ncco)

@app.route("/wstopstn")
def place_call():
    for param_key, param_value in request.args.items():
        print("{}: {}".format(param_key, param_value))
    try:
      from_ = request.args.get('from')
      uuid_ = request.args.get('uuid')
      direction_ = request.args.get('direction')
      to_ = request.args.get('to')
      key_ = request.args.get('key')
      pin_ = request.args.get('pin')
    except:
      return "Invalid Args", 500
    else:
      if to_ and from_ and key_ == "NexMoOrLess":
	print "got password! calling " + to_ + " from " + from_
	return jsonify(voice.wscall(app.config, to_, from_, pin_, uuid_, direction_))
      else:
        return "Forbidden", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
