let temp1 = $('#temp1');
let temp2 = $('#temp2');
let temp3 = $('#temp3');
let option = $('#option');
let multiOption = $('#multi-option');
let completion = $('#completion');

option.click(function () {
    $('.typeofquestion').css('display', 'none');
    temp1.css('display', 'block');
})

multiOption.click(function (){
    $('.typeofquestion').css('display', 'none');
    temp2.css('display', 'block');
})

completion.click(function () {
    $('.typeofquestion').css('display', 'none');
    temp3.css('display', 'block');
})