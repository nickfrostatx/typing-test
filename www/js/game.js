(function() {
    window.Game = function(story) {
        this.story = story;
        this.words = this.story.split(' ');
        this.currentIndex = 0;
    }

    Game.prototype.checkWord = function(word) {
        if (word !== this.words[this.currentIndex])
            return false;
        this.currentIndex += 1;
        return true;
    };

    Game.prototype.playing = function() {
        return this.currentIndex < this.words.length;
    }
})();
