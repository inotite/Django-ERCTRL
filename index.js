var express = require('express');  
var app = express();  
var server = require('http').createServer(app);  
var io = require('socket.io')(server);
// var Cacher = require("cacher");
// debugger
// var cacher = new Cacher()
// console.log(Cacher);

// console.log(cacher);


app.use(express.static(__dirname + '/node_modules'));  

server.listen(4200);
// server.listen(4993);

var numUsers = 0;

app.get('/', function(req, res){
  res.send("connected");
});

io.on('connection', function (client) {
  var addedUser = false;
  // when the client emits 'new message', this listens and executes
  client.on('messages', function (data) {
    console.log(data);
    io.emit('respond', {
      room: data.roomId,
      type: data.type,
      msg: data.msg,
      markup: data.markup,
      amount: data.amount,
      // btn_name: data.btnName,
      // update_min: data.updateMin,
      // clue_update_text:data.clueUpdateText,
      // lock_number : data.lockNumber,
      // current_class : data.currClass,
      // next_class : data.nextClass,
      status: data.status,
    });
  });
});