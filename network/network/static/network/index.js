

document.addEventListener('DOMContentLoaded', function() {

    //hide the make post form
    document.querySelector('#new_post').style.display = 'none';
    //show the make post form
    document.querySelector('#bt_post').onclick = function(){
        toggle_make_post()
    }

    
    

    
    

})

function toggle_make_post(){
    if (document.querySelector('#new_post').style.display == 'block')
        {
            document.querySelector('#new_post').style.display = 'none';
        }
        else {
            document.querySelector('#new_post').style.display = 'block';
        }
}
