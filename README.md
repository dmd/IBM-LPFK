# IBM-LPFK
Some games and a bare bones Python driver for the [IBM LPFK](https://www.brutman.com/IBM_LPFK/IBM_LPFK.html).

Sorry, I haven't really documented this.
It's basically a series of games I wrote for my (then, in 2016 or so) young children to play on the LPFK,
like:

* `wamole` - wack-a-mole, turns some lights on, every time you turn one off, another turns on
* `toggler` - just lets you turn lights on and off
* `blackout` - pressing a key inverts that key's row and column. hit a bunch and then challenge someone to undo what you did.

To quit a game when running `games` you enter the ["sentinel sequence" 0,1,2,3,31](https://github.com/dmd/IBM-LPFK/blob/master/lpfk.py#L58)

### See Also

Phil Pemberton has [written a driver for the LPFK](https://wiki.philpem.me.uk/code/liblpfk).

![IMG_6009](https://user-images.githubusercontent.com/41439/150862696-934adcca-abfb-4889-ade0-4b677693231d.jpeg)
