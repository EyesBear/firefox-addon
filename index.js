var data = require("sdk/self").data;
var pageMod = require("sdk/page-mod");
var self = require("sdk/self");
var response_data = ""
var selection = require("sdk/selection");

// Construct a panel, loading its content from the "text-entry.html"
// file in the "data" directory, and loading the "get-text.js" script
// into it.
var popup = require("sdk/panel").Panel({
  width:600,
  height:800,
  contentURL: data.url("text-entry.html"),
  contentScriptFile: [data.url("jquery.js"),data.url("get-text.js")]
});

// Create a button
require("sdk/ui/button/action").ActionButton({
  id: "show-panel",
  label: "Show Panel",
  icon: {
    "16": "./icon-16.png",
    "32": "./icon-32.png",
    "64": "./icon-64.png"
  },
  onClick: handleClick
});

// Show the panel when the user clicks the button.
function handleClick(state) {
  popup.show();
}

function myListener() {
  console.log("A selection has been made.");
  if (selection.text){
    var Request = require("sdk/request").Request;
    Request({
      url: "http://159.203.7.49/"+selection.text.replace(/ /g, "+"),
      onComplete: function (response) {
        response_data = JSON.parse(response.json);
        popup.show();
      }
    }).get();
  }
}

selection.on('select', myListener);

popup.on("show", function() {
  var item_list = "";
  for (item in response_data){
    item_list = item_list + "<p><a target='_blank'  href='"+response_data[item]['product_url']+"'><img src='"+response_data[item]['img_url']+"'></a> "+response_data[item]['title']+": "+response_data[item]['price']+"</p>";
  };
  popup.port.emit("show",item_list);
});