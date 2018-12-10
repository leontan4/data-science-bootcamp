// from data.js
var tableData = data;

// YOUR CODE HERE!
// console.log(tableData);

tableData.forEach(items => {
    var row = d3.select("tbody").append("tr");

    Object.entries(items).forEach(([key, value]) => {
        var info = row.append("td");
        info.text(value);
    });
});

// var row = d3.select("tbody").append("tr");

// var datas = row.append("td").text(dates);