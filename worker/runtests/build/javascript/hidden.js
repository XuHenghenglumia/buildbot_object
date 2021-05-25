$(document).ready(function(){
    $("#submit").click(function(){
        answerLength=$('input:radio:checked').length
        questionLength=$('div.field').length
        if(answerLength!==questionLength){
            alert("表单不完整，请继续填写")
            return false
        }
    })
})