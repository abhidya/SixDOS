queue()
    .defer(d3.json, "http://localhost:5000/data/visualization")
    .await(makeGraphs);

function makeGraphs(error, projectsJson, statesJson) {

    //Clean projectsJson data
    var project = projectsJson;
    var dateFormat = d3.time.format("%Y-%d-%m %H:%M:%S.%L");
    project.forEach(function (d) {
        d["date"] = dateFormat.parse(d["date"]);
    });


    //Create a Crossfilter instance
    var ndx = crossfilter(project);

    //Define Dimensions
    var dateDim = ndx.dimension(function (d) {
        return d["date"];
    });

    var SpeciesTypeDim = ndx.dimension(function (d) {
        return d["species"];
    });
    var LocationLevelDim = ndx.dimension(function (d) {
        return d["location"];
    });


    //Calculate metrics
    var numProjectsByDate = dateDim.group();
    var numProjectsBySpeciesType = SpeciesTypeDim.group();
    var totalentriesByLocation = LocationLevelDim.group();

    var all = ndx.groupAll();

    var minDate = dateDim.bottom(1)[0]["date"];
    var maxDate = dateDim.top(1)[0]["date"];

    //Charts
    var timeChart = dc.barChart("#time-chart");
    var SpeciesTypeChart = dc.pieChart("#resource-type-row-chart");
    var LocationLevelChart = dc.rowChart("#poverty-level-row-chart");
    var numberProjectsND = dc.numberDisplay("#number-projects-nd");

    numberProjectsND
        .formatNumber(d3.format("d"))
        .valueAccessor(function (d) {
            return d;
        })
        .group(all);


    timeChart
        .width(600)
        .height(160)
        .margins({top: 10, right: 50, bottom: 30, left: 50})
        .dimension(dateDim)
        .group(numProjectsByDate)
        .transitionDuration(500)
        .x(d3.time.scale().domain([minDate, maxDate]))
        .elasticY(true)
        .xAxisLabel("Year")
        .yAxis().ticks(4);


    SpeciesTypeChart
        .width(300)
        .height(250)
        .slicesCap(4)
        .innerRadius(100)
        .dimension(SpeciesTypeDim)
        .group(numProjectsBySpeciesType)
        .legend(dc.legend())
        // workaround for #703: not enough data is accessible through .label() to display percentages
        .on('pretransition', function (chart) {
            chart.selectAll('text.pie-slice').text(function (d) {
                return d.data.key + ' ' + dc.utils.printSingleValue((d.endAngle - d.startAngle) / (2 * Math.PI) * 100) + '%';
            })
        });


    LocationLevelChart
        .width(300)
        .height(250)
        .dimension(LocationLevelDim)
        .group(totalentriesByLocation)
        .xAxis().ticks(4);


    dc.renderAll();

};