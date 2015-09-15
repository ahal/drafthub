# fantasy-draft-tracker
Generates an HTML report from a user provided .csv file which can be used to track players during a live draft.

### Installation

    $ git clone https://github.com/ahal/fantasy-draft-tracker
    $ cd fantasy-draft-tracker
    $ python setup.py install

### Usage

Be sure to replace 'example.csv' with whatever data you wish. It can include as many or as few columns as you want. It's recommended to at least have some sort of "Rank" or "Total Fantasy Value" column though. Then run:

   $ generate-fantasy-report --csv example.csv -o fantasy-report.html

Open the resulting HTML file in a web browser. Clicking a player's row will remove the player from the list (this makes it easy to specify that a player got taken). Players can be sorted by any of the columns, so it's handy to have projections for each of the stat categories.

### TODO

* This really needs some kind of 'Undo' button in case you accidentally click the wrong player
* Could use a search box at the top next to the 'Undo' button, but browser search works for now

Pull requests welcome.
