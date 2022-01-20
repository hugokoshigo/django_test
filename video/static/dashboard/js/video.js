
var videoEreaStatic = false;
var videoEditArea = $('#video-edit-area');

$('#open-form-btn').click(function(){
    if (!videoEreaStatic){
    videoEditArea.show();
    videoEreaStatic = true;
    }else{
    videoEditArea.hide();
    videoEreaStatic = false;
    }
});