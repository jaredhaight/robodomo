
function chartData(stat) {
/*Takes a stats list ({date:value]) and separates it into two lists of dates and values*/
        var times = [];
        var values = [];
        console.log("client.js stat: "+stat)
        $.each(stat, function(key, val) {
            times.push(key);
            values.push(val);
        });
        return [times, values];
    }