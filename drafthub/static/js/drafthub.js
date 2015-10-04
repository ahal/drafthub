var drafted = [];
var positions = {
    'All Positions': ['C', 'LW', 'RW', 'D', 'G'],
    'Forward': ['C', 'LW', 'RW'],
    'Defense': ['D'],
    'Goalie': ['G']
};

function draft(player) {
    player.className = 'taken ' + player.className;

    $('#current-pick').html(parseInt($('#current-pick').html(), 10) + 1);
}

function getColumn(header) {
    var i = $("#players tr th:contains('" + header + "')").index() + 1;
    return $("#players tr:gt(0) td:nth-child(" + i + ")");
}

$(function() {
    $('.player').bind('click', function() {
        drafted.push(this);
        draft(this);
    });

    $('#search').bind('input propertychange', function() {
        var search = $(this).val().toLowerCase();

        // TODO make generic
        getColumn('PLAYER').each(function(index, node) {
            var name = node.innerHTML.toLowerCase();
            var parentNode = $(node.parentNode);

            if (!search || name.indexOf(search) != -1) {
                parentNode.removeClass('filter');
            } else if (name.indexOf(search) == -1) {
                parentNode.addClass('filter');
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
        $('#current-pick').html(parseInt($('#current-pick').html(), 10) - 1);
    });

    $('#position > li > a').bind('click', function() {
        var names = positions[this.innerHTML];
        $('#position-label').html(this.innerHTML);

        // TODO make generic
        getColumn('POS').each(function(index, node) {
            var pos = node.innerHTML;
            var parentNode = $(node.parentNode);

            var found = false;
            for (var i = 0; i < names.length; ++i) {
                var name = names[i];
                if (pos.indexOf(name) != -1) {
                    found = true;
                    break;
                }
            }

            if (!found) {
                parentNode.addClass('filter');
            } else {
                parentNode.removeClass('filter');
            }
        });
    });
});
