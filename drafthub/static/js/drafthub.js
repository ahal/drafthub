var drafted = [];
var positions = {
    'All': ['C', 'LW', 'RW', 'D', 'G'],
    'Forward': ['C', 'LW', 'RW'],
    'Defense': ['D'],
    'Goalie': ['G']
};

function draft(player) {
    player.className = 'taken ' + player.className;

    $('#current-pick').html(parseInt($('#current-pick').html(), 10) + 1);
}

$(function() {
    $('.player').bind('click', function() {
        drafted.push(this);
        draft(this);
    });

    $('#search').bind('input propertychange', function() {
        var search = $(this).val();

        $('td.name').each(function(index, node) {
            var name = node.innerHTML;
            var parentNode = node.parentNode;

            if (!search || name.indexOf(search) != -1) {
                parentNode.className = parentNode.className.replace('filter', '');
            } else if (name.indexOf(search) == -1 && parentNode.className.indexOf('filter') == -1) {
                parentNode.className = 'filter ' + parentNode.className;
            }
        });
    });

    $('#refresh').bind('click', function() {
        $.getJSON($SCRIPT_ROOT + '/_refresh', null, function(data) {
            var picks = data['picks'];
            console.log(picks);
            $('td.name').each(function(index, node) {
                var name = node.innerHTML;

                if (picks.indexOf(name) > -1) {
                    draft(node.parentNode);
                }
            });
        });
    });

    $('#undo').bind('click', function() {
        if (drafted.length == 0) {
            return;
        }
        var player = drafted.pop();
        player.className = player.className.replace('taken', '');

    });

    $('#position > li > span').bind('click', function() {
        var names = positions[this.innerHTML];


    });
});
