// @TODO: YOUR CODE HERE!
var svgWidth = 1200;
var svgHeight = 500;

var margin = {
    top: 20,
    right: 40,
    bottom: 80,
    left: 100
  };
  
var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;


var svg = d3.select("#scatter")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);

var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

var chosenXAxis = "poverty";
var chosenYAxis = "healthcare";

d3.csv("/assets/data/data.csv").then(function(healthData) {

    healthData.forEach(function(data) {
        data.poverty= +data.poverty;
        // data.povertyMoe = +data.povertyMoe;
        // data.age = +data.age;
        // data.ageMoe = +data.ageMoe;
        // data.income = +data.income;
        // data.incomeMoe = +data.incomeMoe;
        data.healthcare = +data.healthcare;
        // data.healthcareLow = +data.healthcareLow;
        // data.healthcareHigh = +data.healthcareHigh;
        // data.obesity = +data.obesity;
        // data.obesityLow = +data.obesityLow;
        // data.obesityHigh = +data.obesityHigh;
        // data.smokes = +data.smokes;
        // data.smokesLow = +data.smokesLow;
        // data.smokesHigh = +data.smokesHigh;

    });

    var xLinearScale = d3.scaleLinear()
        .domain([d3.min(healthData, d => d[chosenXAxis]) * 0.9,
        d3.max(healthData, d => d[chosenXAxis]) * 1.2])
        .range([0, width]);

    var yLinearScale = d3.scaleLinear()
        .domain([4, d3.max(healthData, d => d[chosenYAxis])*0.9])
        .range([height, 0]);

    var bottomAxis = d3.axisBottom(xLinearScale);
    var leftAxis = d3.axisLeft(yLinearScale);

    chartGroup.append("g")
        .classed("x-axis", true)
        .attr("transform", `translate(0, ${height})`)
        .style("font-size", "18px")
        .call(bottomAxis);

    chartGroup.append("g")
        .style("font-size", "18px")
        .call(leftAxis);

    var circlesGroup = chartGroup.selectAll("circle")
        .data(healthData)
        .enter()
        .append("circle")
        .attr("cx", d => xLinearScale(d.poverty), 100)
        .attr("cy", d => yLinearScale(d.healthcare), 100)
        .attr("r", 15)
        .attr("fill", "lightblue")
        .attr("opacity", ".8");

    
    var labelsGroup = chartGroup.append("g")
        .attr("transform", `translate(${width / 2}, ${height + 20})`);

    var textCircle = chartGroup.selectAll("text.text-circles")
        .data(healthData)
        .enter()
        .append("text")
        .classed("text-cricles", true)
        .text(d => d.abbr)
        .attr("x", d => xLinearScale(d.poverty))
        .attr("y", d => yLinearScale(d.healthcare))
        .attr("dy",5)
        .attr("text-anchor","middle")
        .attr("font-size","12px");
    
    // append y axis
    var healthLabel = chartGroup.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (height / 1.5))
        .attr("dy", "1em")
        .classed("axis-text", true)
        .text("Lacks of HealthCare (%)");

    var povertyLabel = labelsGroup.append("text")
        .attr("x", 0)
        .attr("y", 40)
        .attr("value", "poverty") // value to grab for event listener
        .classed("axis-text", true)
        .text("In Poverty (%)");

    circlesGroup.on("mouseover", function() {
        d3.select(this)
            .transition()
            .duration(1000)
            .attr("r", 30)
            .attr("fill", "red");
        })
        .on("mouseout", function() {
            d3.select(this)
            .transition()
            .duration(1000)
            .attr("r", 15)
            .attr("fill", "lightblue");
        });
        
        // transition on page load
        chartGroup.selectAll("circle")
        .transition()
        .duration(1000)
        .attr("cx", (d, i) => xScale(i))
        .attr("cy", d => yScale(d));

});

