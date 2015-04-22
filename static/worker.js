importScripts('BigInteger.min.js');
self.addEventListener('message', function(e) {
    var first = bigInt(e.data[0]);
    var second = bigInt(e.data[1]);
    var Flag = false;
    while(!Flag && bigInt(first).compare(second) == -1) {
        if(first.isPrime()) {
            self.postMessage(first.toString());
            Flag = true;
        }
        first = first.add(1);
    }
    if(!Flag) {
        self.postMessage(0);
    }
}, false);