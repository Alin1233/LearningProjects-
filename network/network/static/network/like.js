document.addEventListener('DOMContentLoaded', function(){

     //like button and like function
     let bts = document.getElementsByClassName("like")
     Array.from(bts).forEach(function(bt){
         bt.onclick = function(){
             like(bt)
             
         }
     })
 
     // display  nr of likes
     let posts = document.getElementsByClassName("like_nr")
     Array.from(posts).forEach(function(post){
         like_count(post)
     })
})
function like(bt){
    
    let  id = bt.dataset.id
     fetch('like', {
         method: 'POST',
         body: JSON.stringify({
             id: `${id}`
         })
       })
         .then(response => response.json())
         .then(result => {
         // Print result
         console.log(result);
 
         if(result['message'] == 'redirect'){
             window.location.assign('login') 
         }   

         //update the like count
         post = document.getElementById(`${bt.dataset.id}`)
         like_count(post)
         
         });
      
     
 }
 function like_count(post){
     
     let id = post.dataset.id
     fetch('like/'+id)
     .then(response => response.json())
     .then(data => {
     post.innerHTML = `${data['like_nr']} Like`
 
     if (data['bt_status'] === true ){
         document.getElementById(`bt+${id}`).innerHTML = "Unlike me!" 
     }else{
         document.getElementById(`bt+${id}`).innerHTML = "Like me!" 
     }
     
      
     });
 }