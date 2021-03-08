
    

//get number of rounds
let rounds = document.getElementById('rounds');
rounds.onclick = () => {

    let nr_rounds = document.getElementById('nr').value;

    //display you are playing x rounds and score
    let display = document.getElementById('display');
    display.innerHTML = `You are playing ${nr_rounds} rounds`;
    let current_round = document.getElementById('current_round');
    current_round.innerHTML = `Round 1 of ${nr_rounds} Score 0-0`;

    //play the game    
    game(nr_rounds,current_round);
    document.getElementById('final_score').innerHTML ='';
    
    
    

}

function game(nr_rounds,current_round){

    //human score
    let score_x = 0;
    //pc score
    let score_y = 0;
    //tie score
    let tie = 0;

    //round counter
    let round_counter = 0;
    let humanPlay = -1;
    nr_rounds = Number(nr_rounds) ;
    //get all buttons and play a round on every button click
    const buttons = document.querySelectorAll('button');
    buttons.forEach((button) => {
        button.onclick =() =>{


            //rock = 0 paper = 1 scissors = 2
            
            switch(button.id){
                case 'rock':
                    humanPlay = 0;
                case 'paper':
                    humanPlay = 1;
                case 'scissors':
                    humanPlay = 2;

                }

                //a round cand go on only if it is not the last round
                console.log(round_counter,nr_rounds)
                if (round_counter  != nr_rounds ){
                    round_counter++;

                //get cpu play
                let computerPlay = Math.floor(Math.random() * 3);
                //play rounds and determine a winer
                let round = playRound(humanPlay,computerPlay);
                if (round.search("Tie") != -1){  
                    tie++;
                    current_round.innerHTML = `Round ${round_counter} of ${nr_rounds} Score ${score_x}-${score_y}`;
                }
                if (round.search("Win") != -1){
                    score_x++;
                    current_round.innerHTML = `Round ${round_counter} of ${nr_rounds} Score ${score_x}-${score_y}`;
                }
                if (round.search("Lost") != -1){
                    score_y++;
                    current_round.innerHTML = `Round ${round_counter} of ${nr_rounds} Score ${score_x}-${score_y}`; 
                }
                console.log(round);

                }
                
                let final = document.getElementById('final_score');
                //display score
                if(round_counter === nr_rounds){
                    console.log(round_counter,nr_rounds)
                    if ( score_x > score_y ){
                        
                        final.innerHTML = `Game Over!You win,with a score of ${score_x} to ${score_y}.`;
                    }
                    if (score_x == score_y){
                        final.innerHTML = `Game Over!It is a tie,${score_x} to ${score_y}.`;
                            
                    }else if (score_x < score_y){
                        final.innerHTML = `Game Over!You lose,with a score of ${score_x} to ${score_y}.`;
                           
                    }
                    } 
        }            
    })                               
}

function playRound(playerSelection,computerSelection){
    let x = playerSelection;
    let y = computerSelection;
    if ( x == 0)
    {
        switch (y){
            case 0:
                return ("Tie,Rock can not smash Rock");
            case 1:
                return("You Lost,Rock is wraped by Paper");
            case 2:
                return("You Win,Rock smashes Scisors")
        }
    }
    if ( x == 1)
    {
        switch (y){
            case 0:
                return ("You Win,Paper wraps Rock");
            case 1:
                return("Tie,Paper can not wrap Paper");
            case 2:
                return("You Lost,Paper is cut by Scisors")
        }
    }
    if ( x == 2)
    {
        switch (y){
            case 0:
                return ("You Lost,Scisors is smashed by Rock");
            case 1:
                return("You Win,Scisors cuts Paper");
            case 2:
                return("Tie,Scisors can not cut Scisors")
        }
    }
}










