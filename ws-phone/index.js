const server = require('http').createServer()
const WebSocketServer = require('ws').Server
const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const wss = new WebSocketServer({ server: server })

// Inbound number for display
const inbound_number = process.env.INBOUND_NUMBER || '-'

app.use(express.static('static'))
app.enable('trust proxy')

app.get('/answer_old', (req, res) => {
  console.log(' got answer!!!!')
  const input_url =
    (req.secure ? 'https' : 'http') + '://' +
    req.headers.host + '/input'
  console.log(' answering, sending dtmf ncco')
  res.send([
    {
      action: 'talk',
      text: 'Enter that code on your screen now'
    },
    {
      action: 'input',
      eventUrl: [input_url],
      timeOut: 30,
      maxDigits: 4
    }
  ])

})

app.get('/answer', (req, res) => {

  var from = req.query.from;
  var to = req.query.to;
  var uuid = req.query.uuid
  var direction = req.query.direction

  activekey = ''
  for (var key of activepins.keys()) {
    console.log(key);
    activekey = key
    status = activepins.get(key)
    if (status === 'available') {
      activepins.delete(activekey)
      break
    } else {
      continue
    }
  }
  
  console.log(`connecting to ${activekey}`)
  
  const ws_url =
    (req.secure ? 'wss' : 'ws') + '://' +
    req.headers.host + '/server/' + activekey


  if(pins.has(activekey)) {
    console.log("Found available agent")
    res.send([
      {
        action: 'talk',
        text: 'Thank you for calling'
      },
      {
        'action': 'connect',
        'endpoint': [
          {
            'type': 'websocket',
            'uri': ws_url,
            'content-type': 'audio/l16;rate=16000',
            'headers': {
                'from': from,
                'to': to,
                'uuid': uuid,
                'direction': direction 
            }
          }
        ]
      }
    ])
  } else {
    console.log("no agents available")
    res.send([
      {
        action: 'talk',
        text: 'All agents are currently unavailable, sorry'
      }
    ])

  }

})

app.get('/agents', (req, res) => {
  
  result = ''
  for (var key of pins.keys()) {
    console.log(key);
    wsocket = pins.get(key)
    if (result === '') {
      result = key
    } else {
      result = result + "|" + key
    }
  }
  res.send([
   {
     agents: result
   }
  ])
  

})

app.get('/getavailable', (req, res) => {
 
  activekey = ''

  for (var key of activepins.keys()) {
    activekey = key
    status = activepins.get(key)
    if (status === 'available') {
      break
    } else {
      continue
    }
  }
  res.send([
   {
     agents: activekey
   }
  ])


})

app.get('/agentstatus', (req, res) => {

  result = ''
  for (var key of activepins.keys()) {
    console.log(key);
    status = activepins.get(key)
    if (result === '') {
      result = key + ":" + status
    } else {
      result = result + "|" + key + ":" + status
    }
  }
  res.send([
   {
     agents: result
   }
  ])

})


app.post('/event', bodyParser.json(), (req, res) => {
  console.log('event>', req.body)
  res.sendStatus(200)
})


app.post('/input', bodyParser.json(), (req, res) => {

  console.log(`connecting ${req.body.uuid} to ${req.body.dtmf}`)

  const ws_url =
    (req.secure ? 'wss' : 'ws') + '://' +
    req.headers.host + '/server/' + req.body.dtmf


  if(pins.has(req.body.dtmf)) {
    res.send([
      {
        action: 'talk',
        text: 'connecting you'
      },
      {
        'action': 'connect',
        'endpoint': [
          {
            'type': 'websocket',
            'uri': ws_url,
            'content-type': 'audio/l16;rate=16000',
            'headers': {}
          }
        ]
      }
    ])
  } else {

    res.send([
      {
        action: 'talk',
        text: 'Couldn\'t find a matching call, sorry'
      }
    ])

  }

})


app.post('/', function(req, res){
    console.log(req.query.agent);
    res.send('Response send to client::'+req.query.agent);

});


// keep track of who is talking to who
const connections = new Map
const pins = new Map
const activepins = new Map
const availablepins = new Map


const generatePIN = () => {
  for (var i = 0; i < 3; i++) {
    const attempt = Math.random().toString().substr(2,4)

    if(!pins.has(attempt)) return attempt
  }
  return 'nope'
}



wss.on('connection', ws => {
  const url = ws.upgradeReq.url
  const serverRE = /^\/server\/(\d{4})$/

  if(url == '/browser') {

    var pin = generatePIN()

    ws.send(JSON.stringify({ pin, inbound_number }))

    pins.set(pin, ws)
    activepins.set(pin, 'available')

    ws.on('close', () => {
      pins.delete(pin)
      activepins.delete(pin)
    })

  } else

  if(url.match(serverRE)) {

    const digits = url.match(serverRE)[1]

    const client = pins.get(digits)
    const pinstatus = activepins.get(digits)
    if(client) {
        console.log('found client!!')
        connections.set(ws, client)
        connections.set(client, ws)
    }
  }

  ws.on('message', data => {
    const other = connections.get(ws)

    if(other && other.readyState == ws.OPEN) {
      other.send(data)

      console.log('proxy: ', ws.upgradeReq.url, '  ---->  ', other.upgradeReq.url)
    }

  })

  ws.on('close', () => {
    console.log('closing')
    connections.delete(ws)
  })


})


server.on('request', app)

server.listen(process.env.PORT || 3000, () => {
  console.log('Listening on ' + server.address().port)
})
