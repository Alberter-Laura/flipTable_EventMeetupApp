
$(document).ready(function(){

    $('[data-spy="scroll"]').each(function(){
        var $spy = $(this).scrollspy('refresh');
    }); 
    $("body").scrollspy({
        target: "#myNavbar",
        offset: 70
    }) 


});

// $(function(){
//     alert("js working");

//     var userName = prompt ("Who demands to enter this dungeon??");
//     console.log(userName);

// // alert for the delete button
//     $("#btn-click").click(function() {
//         alert("You did it!");
//     })

// // toggle text
//     $("#btn-toggle").click(function() {
//         $("#toggle-hide").toggle("slow");
//     })

// // This will ADD a class to something. Could use for changing CSS maybe??
//     $("#btn-add-class").click(function() { 
//         $("#addClass").addClass("purple");
//     })

//     // This will CHANGE a class to something else. Could use for changing CSS maybe??
//     $("#btn-change-class").click(function() {
//         $("#attr").attr("class", "green");
//     })

// // Change the text of something
//     $("#btn-change-text").click(function(){
//         $("#changeText").text("Hello There")
//     })
// })



