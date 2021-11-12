class BoggleGame {
    constructor(boardId, secs = 60){
        this.secs = secs; //game length
        // this.showTimer();

        this.score = 0; //initial score = 0
        this.words = new Set(); // make empty set for guessed words
        this.board = $("#" + boardId); //select board in html markup

        // every 1000 msec, "tick"
        this.timer = setInterval(this.tick.bind(this), 1000);

        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }

    showWord(word) {
        $('#words').append(`<li>${word}</li>`)
    }

    updateScore() {
        $('#score').text(`Score: ${this.score}`)
    }

    showMessage(msg, cls){
        $('#msg') // select msg paragraph
            .text(msg) // update text of p
            .removeClass() // remove previous class, if any
            .addClass(`msg-${cls}`) // add new class
    }

    async handleSubmit(evt) {
        evt.preventDefault(); //prevent refresh of page
        const $guess = $("#guess", this.board) //jquery select guess input

        let guess = $guess.val() //assign value of input to word variable
        if (!guess) return; // if word is empty, exit
        
        if (this.words.has(guess)) { //if word was already found, show message
            this.showMessage(`You already found this word!`, "err");
            return;
        }

        const resp = await axios.get("/check-word", {params: {guess: guess}}); // store python response to guessed word

        if (resp.data.result === "not-word") { 
            this.showMessage(`${guess} is not a valid English word`, 'err') //if resp says guess is not word, alert user
        } else if (resp.data.result === "not-on-board") {
            this.showMessage(`${guess} is not a valid word on this board`, 'err') //if resp says guess is not on board, alert user
        } else {
            this.showWord(guess);  // add word to html list of accepted words
            this.score += guess.length; // update score
            this.updateScore(); // show new score
            this.words.add(guess); // add word to guessed word set
            this.showMessage(`Scored: ${guess}`, "ok") //alert user
        }

        $guess.val("").focus(); // clear input field
    }

    showTimer() {
        $(".timer", this.board).text(this.secs);
    }

    async tick() {
        this.secs -= 1;
        this.showTimer();
        if (this.secs === 0) {
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }

    async scoreGame() {
        $("#form").hide();
        const resp = await axios.post("/post-score", { score: this.score });
        if (resp.data.brokeRecord) {
          this.showMessage(`New record: ${this.score}`, "ok");
        } else {
          this.showMessage(`Final score: ${this.score}`, "ok");
        }
      }
}

