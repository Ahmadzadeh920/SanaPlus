src_auth= $('script#Sana').attr('src');
$(document).ready(function(e){
    urls= document.URL;
    tittle=document.title;
    referrer=document.referrer;
    events_URls={
        'urls': urls,
        'tittle':tittle,
        'referrer':referrer,
    }
    $.ajax({
            type: "GET",
            url: 'http://localhost:8009/Events/Page_ranking/',
            data: {
                'src_str': src_auth,
                'json_format': JSON.stringify(events_URls),
            },
            crossDomain: true,

            //jsonp: 'callback',
            //jsonpCallback: 'logResults',

            crossOrigin: true,
            contentType: "application/json",

            success: function (result) {
                console.log(result)
            },
        })

})
