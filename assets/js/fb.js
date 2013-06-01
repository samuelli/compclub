function dateFromUTC( dateAsString, ymdDelimiter ){
  var pattern = new RegExp( "(\\d{4})" + ymdDelimiter + "(\\d{2})" + ymdDelimiter + "(\\d{2})T(\\d{2}):(\\d{2}):(\\d{2})" );
  var parts = dateAsString.match( pattern );

  return new Date(
      parseInt( parts[1] )
    , parseInt( parts[2], 10 ) - 1
    , parseInt( parts[3], 10 )
    , parseInt( parts[4], 10 )
    , parseInt( parts[5], 10 )
    , parseInt( parts[6], 10 )
    , 0
  );
}

function getFbEvents(){
  access_token = "AAAECJC0TVB4BAIOEFFCqGjH6VfrZA7Tcqnwzsu2cfg6gyep8eKntNZA1QipxPqslQhh2KoKLZAegyK5ZBbzLYG7jiuHAG7PpXamdeqlYtAZDZD";
  $.getJSON("https://graph.facebook.com/2509117190/events",
    {
      "access_token": access_token,
      "limit": "3"
    },
    function(group_events) {
       $.each(group_events.data, function(i,item){
         $('#carousel-inner').html('');
         $.getJSON("https://graph.facebook.com/" + item.id,
           {
             "access_token": access_token
           },
           function(event_details){
              //var a = dateFromUTC(event_details.start_time,"-");
               
              $('#carousel-inner').append(
              'testing'
              );
           }
         );
       });
       $('.carousel').carousel();
     }
   );
}

