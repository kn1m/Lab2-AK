self.addEventListener('message', function(e) {
    var n = e.data;
    search: while (true) {
      n += 1;
      for (var i = 2; i <= Math.sqrt(n); i += 1)
        if (n % i == 0)
         continue search;
      // found a prime!
      self.postMessage(n);
        break;
    }
}, false);