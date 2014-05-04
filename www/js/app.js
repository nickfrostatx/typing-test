(function() {
    var game;
    var wordSpans;

    $('#input').hide();

    $('.start-btn').click(function() {
        api.getStory({}, function(data) {
            $('.start-btn').hide();
            game = new Game(data.story);
            wordSpans = [];
            for (var i = 0; i < game.words.length; i++) {
                wordSpans.push($('<span>' + game.words[i] + ' </span>').appendTo($('#story')));
            }
            wordSpans[0].attr('class', 'current');
            $('#input').show();
            $('#input').focus();
        });
    });

    function checkWithSpace(word, next) {
            return (word.length - 1 == next.length
                && word.substring(word.length - 1, word.length) == ' '
                && game.checkWord(word.substring(0, word.length - 1)))
        }

    $('#input').on('input', function() {
        if (game.playing()) {
            var next = game.words[game.currentIndex];
            var word = $(this).val();

            

            if ((wordSpans.length == 1 && game.checkWord(word)) || checkWithSpace(word, next)) {
                wordSpans[0].attr('class', 'correct');
                wordSpans.shift(1);
                if (game.playing()) {
                    wordSpans[0].attr('class', 'current');
                } else {
                    win();
                }
                $(this).val('');
            } else if (next.substring(0, word.length) !== word) {
                wordSpans[0].attr('class', 'error');
            } else {
                wordSpans[0].attr('class', 'current');
            }
        }
    });

    function win() {
        $('#story').empty();
        $('#input').hide();
        $('.start-btn').show();
    }
})();
