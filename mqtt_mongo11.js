#!/usr/bin/node

var mqtt=require('/usr/lib/node_modules/mqtt')
var mongodb=require('/usr/lib/node_modules/mongodb');
var request = require('/usr/lib/node_modules/request')

var mongodbClient=mongodb.MongoClient;
// set YOUR mongodb username (mqtt) and password (password) here
var mongodbURI='mongodb://mqtt:password@127.0.0.1:27017/data'
var client = new Object();

// for debugging
function showit(topic,payload) {
  console.log(payload); 
  console.log(topic); }

function insertEvent(topic,payload) {
      mongodbClient.connect(mongodbURI, function(err,db) {
          if(err) { console.log(err); return; }
          else {
              # save messages in collection 'nxpriot'
              var coll = 'nxpriot';
              collection = db.collection(coll);
              collection.insert(
                 { value:payload, when:new Date() },
                 function(err,docs) {
                    if(err) { console.log("Insert fail" + err); } // Improve error handling
                    else { console.log("Update callback - closing db");
                           db.close();
                    } // end of else block
              });  // end of insert block
          }      // end of mongo  connect else block
      });       // end of mongo connect block
    }          // end of insertEvent


// with 
//   { $push: { "event" : { value:buf.toString(), when:new Date() } } },
// use
// > db.nodes_02E00202_packets.find()[0]["event"].length
// to count entries

// put this in a function we can call on event of going offline
function connectmq() {
   // use YOUR mqtt username and password here
   client=mqtt.connect('mqtt://127.0.0.1',{username:"mqttuser",password:"password"});
}


connectmq();

client.on('connect',function() {
 client.subscribe('/nxpriot');
});

client.on('message',insertEvent);
//client.on('message',showit);

client.on('offline',connectmq);


