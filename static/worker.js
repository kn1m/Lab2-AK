self.addEventListener('message', function(e) {
    var n = e.data[0];
    search: while (true) {
      n += 1;
        if( n <= e.data[1]) {
            for (var i = 2; i <= Math.sqrt(n); i += 1)
                if (n % i == 0)
                    continue search;
            self.postMessage(n);
            break;
        }
        self.postMessage(0);
    }
}, false);