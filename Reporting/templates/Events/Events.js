src_auth= $('script#Sana').attr('src');
now_start=new Date();
time_events=new Date().getSeconds();
var data_events = {clicks:[],dbclicks:[],blur:[], submit:[], onkeyup: [], mousemove:[] , video:[], audio:[] ,drag_drop:[], img_load:[] };
white_list_tag=["P","A","SPAN" ,"VIDEO","AUDIO","DIV","IMG"];


var startTime = new Date().getTime();
$(window).on('load', function(){
    var startTime = new Date().getTime();

    for (k = 0; k < $('img').length; k++) {
        var img = new Image();
        img.src = $('img')[k].src;
        img.onload = function(e)
        {
            var endTime = new Date().getTime();
            diff=endTime-startTime
            load_img = {
                  "TagName": e.target.tagName,
                   "ID_Name": e.target.id,
                   "time": diff,
              };
            data_events.img_load.push(load_img)
        };
}
});

//_________________________________________clicks Events
$(window).click(function (e) {
    if(jQuery.inArray(e.target.tagName, white_list_tag)!== -1) {
        click_event = {
            "TagName": e.target.tagName,
            "ID_Name": e.target.id,
        }
        data_events.clicks.push(click_event);
        time_events=new Date().getSeconds();
        check_time()
    }

    console.log(data_events);

    });
//_____________________________________dbClicks Events
$(window).dblclick(function (e) {
    if(jQuery.inArray(e.target.tagName, white_list_tag)!== -1) {
        dbclick_event = {
            "TagName": e.target.tagName,
            "ID_Name": e.target.id,
        }
        data_events.dbclicks.push(dbclick_event);
        time_events=new Date().getSeconds();
        check_time()
    }

    console.log(data_events);

    });

//________________________________Blur Events

$(window).blur(function (e) {
    if(jQuery.inArray(e.target.tagName, white_list_tag)!== -1) {
        blur_event = {
            "TagName": e.target.tagName,
            "ID_Name": e.target.id,
        }
        data_events.blur.push(blur_event);
        time_events=new Date().getSeconds();
        check_time()
    }

    console.log(data_events);

    });


//________________________________________________Submited Events:


$(window).submit(function (e) {
    if(jQuery.inArray(e.target.tagName, white_list_tag)!== -1) {
        submit_event = {
            "TagName": e.target.tagName,
            "ID_Name": e.target.id,
        }
        data_events.submit.push(submit_event);
        time_events=new Date().getSeconds();
        check_time()

    }

    console.log(data_events);

    });

//_____________________________________________________Mouser Over

$(window).mouseenter(function (e_over) {
    if(jQuery.inArray(e_over.target.tagName, white_list_tag)!== -1) {
        start_over=new Date().getTime();
      $(this).mouseleave(function(e_out){
           if(jQuery.inArray(e_out.target.tagName, white_list_tag)!== -1) {
               end_mouse = new Date().getTime();
               var diff = end_mouse - start_over; // Returns the number of milliseconds
               mouseenter_event = {
                   "TagName": e_out.target.tagName,
                   "ID_Name": e_out.target.id,
                   "time": diff,
               };
               data_events.mousemove.push(mouseenter_event);
               check_time();
           }
      })

    }

})




//----------------------------------------------Close windows Detect


$(document).mousemove(function(e) {
    if(e.pageY <= 5)
    {
        time_events=new Date().getSeconds();
        check_time();
    }
  });

//--------------------------------Video Pause and Start


 $("body video").on('play',function(){
     start_over_video=new Date().getTime();
      $(this).on('pause',function(e_out){
        if(jQuery.inArray(e_out.target.tagName, white_list_tag)!== -1) {
            end_pause = new Date().getTime();
            var diff = end_pause - start_over_video; // Returns the number of milliseconds
            video_events = {
                "TagName": e_out.target.tagName,
                "ID_Name": e_out.target.id,
                "time": diff,
            };
            data_events.video.push(video_events);
            check_time();
        }

      });


});
//------------------------------------audio

 $("body audio").on('play',function(){
     start_over_audio=new Date().getTime();
      $(this).on('pause',function(e_out){
        if(jQuery.inArray(e_out.target.tagName, white_list_tag)!== -1) {
            end_pause = new Date().getTime();
            var diff = end_pause - start_over_audio; // Returns the number of milliseconds
            audio_events = {
                "TagName": e_out.target.tagName,
                "ID_Name": e_out.target.id,
                "time": diff,
            };
        data_events.audio.push(audio_events);
        check_time();
        }

        });
    });

//--------------------------------------drag and drop
$(window).on("dragstart",function(){
     start_drag=new Date().getTime();
     $(this).on('drop',function(e_out){
         if(jQuery.inArray(e_out.target.tagName, white_list_tag)!== -1) {
             end_drop = new Date().getTime();
            var diff = end_drop - start_drag; // Returns the number of milliseconds
              drag_drop_events = {
                  "TagName": e_out.target.tagName,
                  "ID_Name": e_out.target.id,
                  "time": diff,
              };
          data_events.drag_drop.push(drag_drop_events);
          check_time();
  }

  });

    });


//------------------------------------IMG loading time





//------------------------------------------------------ Script for record data base

function record_db(){
     $.ajax({
            type: "GET",
            url: 'http://localhost:8009/Events/reloads/',
            data: {
                'json_format': JSON.stringify(data_events),
                'src_str': src_auth,
            },
            crossDomain: true,
            dataType: "json",
            //jsonp: 'callback',
            //jsonpCallback: 'logResults',

            crossOrigin: true,
            contentType: "application/json",

            success: function (result) {
                console.log(result)
            },
        })


}

function check_time() {
    duration = time_events - now_start.getSeconds();

    if(duration >5){
        record_db();
        now_start=new Date();
        data_events=now_start.getSeconds();
       data_events = {clicks:[],dbclicks:[],blur:[], submit:[], onkeyup: [], mousemove:[] , video:[], audio:[] ,drag_drop:[], img_load:[]};
    }
}

//----------------------------------------Events on Video
