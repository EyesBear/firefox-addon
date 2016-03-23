// Listen for the "show" event being sent from the
// main add-on code. It means that the panel's about
// to be shown.
//
self.port.on("show", function onShow(data) {
  $('body').html(data);
 });