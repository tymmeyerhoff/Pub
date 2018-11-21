const Nexmo = require('nexmo');
const nexmo = new Nexmo({
  apiKey: '---',
  apiSecret: '----'
});

nexmo.message.sendSms(
  '12525629514', '17327880638', 'yo',
    (err, responseData) => {
      if (err) {
        console.log(err);
      } else {
        console.dir(responseData);
      }
    }
);

