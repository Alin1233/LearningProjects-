document.addEventListener('DOMContentLoaded', function() {

   let bts = document.getElementsByClassName("edit")
   Array.from(bts).forEach(function(bt){
        document.getElementById(`textarea+${bt.value}`).style.display = 'none'
        bt.addEventListener('click', function (){
            
            edit(bt)
       })
   })
        
})

function edit(bt){
    
    if (document.getElementById(`textarea+${bt.value}`).style.display == 'none'){
        document.getElementById(`textarea+${bt.value}`).style.display = 'block'
        txt = document.getElementById(`text+${bt.value}`)
        document.getElementById(`textarea+${bt.value}`).innerHTML = `<textarea name="edit+${bt.value}">${txt.innerHTML}</textarea> <button type="submit">Submit</button>` 
    }else {
        document.getElementById(`textarea+${bt.value}`).style.display = 'none'
    }
    
    
}