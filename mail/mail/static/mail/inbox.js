document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view_email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view_email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/'+mailbox)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    
    let l = emails.length 
    // ... do something else with emails ...
    for (i = 0; i < l; i++ ){
     const email_div = document.createElement('div');
      email_div.style.border ="thick solid #000000";
      email_div.style.padding = "10px" ;
      

      from = document.createElement('span');
      sender = document.createElement('span');
      sender.classList.add("email_span");

      subject = document.createElement('span');
      sub = document.createElement('span');
      subject.classList.add("email_span");

      time = document.createElement('span');
      timestamp = document.createElement('span');
      timestamp.classList.add("email_span");

      from.innerHTML = "From: "
      sender.innerHTML = emails[i].sender;
      email_div.append(from);
      email_div.append(sender);

      sub.innerHTML = "Subject: "
      subject.innerHTML = emails[i].subject;
      email_div.append(sub);
      email_div.append(subject);

      time.innerHTML = "Timestamp: "
      timestamp.innerHTML = emails[i].timestamp;
      email_div.append(time);
      email_div.append(timestamp);

      //color
      let def = '';
      if (emails[i].read === true){
        email_div.style.backgroundColor = 'gray';
        def = email_div.style.backgroundColor;
      }else {
        email_div.style.backgroundColor = 'white';
        def = email_div.style.backgroundColor;
      }
      email_div.addEventListener('mouseover', () =>{
        email_div.style.backgroundColor = 'red';
      })
      email_div.addEventListener('mouseleave', () =>{
        email_div.style.backgroundColor = def;
      })
      
      let id = emails[i].id;
      email_div.addEventListener('click', () => view_email(id));
      
      document.querySelector('#emails-view').append(email_div);
    }

});

}

function send_mail(){
  
  let destination = document.querySelector('#compose-recipients').value;
  let subject =  document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: destination,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      document.querySelector('#sent').click();
  });
  
}

function view_email(id){

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view_email').style.display = 'block';


  from = document.querySelector('#from');
  subject = document.querySelector('#subject');
  time = document.querySelector('#time');
  body = document.querySelector('#body');
  bt = document.querySelector("#bt");

  let user = document.querySelector("#user").innerHTML
  

  fetch('/emails/'+id)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);
    from.innerHTML = email.sender;
    subject.innerHTML = email.subject;
    time.innerHTML = email.timestamp;
    body.innerHTML = email.body;
    

    //replay function
    document.querySelector("#rep").onclick = function(){
      compose_email();
      
      if (email.subject.includes("Re: ")){
        document.querySelector('#compose-subject').value = email.subject;
      }else{
        document.querySelector('#compose-subject').value = "Re: "+email.subject;
      }

      document.querySelector('#compose-recipients').value = email.sender;
      
      document.querySelector('#compose-body').value = "On" +" " + email.timestamp+" "+ email.sender + " wrote: " + email.body;
    }

    // archive/unarchive function
    if ( user == email.sender){
      bt.style.visibility = "hidden";
    }
    else if (email.archived == true){
      bt.style.visibility = "visible";
      bt.innerHTML = 'Unarchive';
      bt.onclick = function(){
        
        update_mail(email.id,email.archived).then( () => {
          document.querySelector('#inbox').click();
      });
        
      }
    }else{
      bt.style.visibility = "visible";
      bt.innerHTML = 'Archive';
      bt.onclick = function(){
        
        update_mail(email.id,email.archived).then( () => {
          document.querySelector('#archived').click();
      });
       
      }
    }
    
  
});
  //mark email as read
  fetch('/emails/'+id, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}

//updates archived status
function update_mail (id, archive_status){
  return fetch('/emails/'+id, {
    method: 'PUT',
    body: JSON.stringify({
        archived: (archive_status !== true)
    })
  });
}











