
// Add line-plots of temperature deviations 
var global_temp = {
    x: graphs['global_data']['x'],
    y: graphs['global_data']['y'],
    mode: 'lines',
    line: {
        color: 'rgb(0, 0, 128)',
    },
    name: graphs['global_data']['name'],
};
var northern_temp = {
    x: graphs['northern_data']['x'],
    y: graphs['northern_data']['y'],
    mode: 'lines',
    line: {
        color: 'rgb(230, 138, 0)',
    },
    name: graphs['northern_data']['name'],
};
// add plot of forecast for global temperature deviations
// with confidence interval
var gl_forecast = {
    x: graphs['global_forecast']['index'],
    y: graphs['global_forecast']['mean'],
    mode: 'lines',
    name: graphs['global_forecast']['name'],
    line: {
        color: 'rgb(26, 26, 255)',
    }
};
var gl_forecast_ci_lower = {
    x: graphs['global_forecast']['index'],
    y: graphs['global_forecast']['ci_lower'],
    mode: 'lines',
    name: 'Global forecast 95% CI',
    showlegend: false,
    line: {
        color: 'rgb(159, 159, 223)',
        dash: 'dot',
        width: 1,          
    }
};
var gl_forecast_ci_upper = {
    x: graphs['global_forecast']['index'],
    y: graphs['global_forecast']['ci_upper'],
    mode: 'lines',
    fill: 'tonexty',
    name: 'Global forecast 95% CI',
    line: {
        color: 'rgb(159, 159, 223)',
        alpha: 0.2,
        dash: 'dot',
        width: 1,          
    }
};
// add plot of forecast for northern hemisphere temperature deviations
// with confidence interval
var nh_forecast = {
    x: graphs['northern_forecast']['index'],
    y: graphs['northern_forecast']['mean'],
    mode: 'lines',
    name: graphs['northern_forecast']['name'],
    line: {
        color: 'rgb(250, 194, 5)',
    }
};
var nh_forecast_ci_lower = {
    x: graphs['northern_forecast']['index'],
    y: graphs['northern_forecast']['ci_lower'],
    mode: 'lines',
    name: 'Northern hemisphere forecast 95% CI',
    showlegend: false,
    line: {
        color: 'rgb(255, 194, 102)',
        dash: 'dot',
        width: 1,          
    }
};
var nh_forecast_ci_upper = {
    x: graphs['northern_forecast']['index'],
    y: graphs['northern_forecast']['ci_upper'],
    mode: 'lines',
    fill: 'tonexty',
    name: 'Northern hemisphere forecast 95% CI',
    line: {
        color: 'rgb(255, 194, 102)',
        alpha: 0.2,
        dash: 'dot',
        width: 1,          
    }
};

var data = [nh_forecast, nh_forecast_ci_lower, nh_forecast_ci_upper,
            gl_forecast, gl_forecast_ci_lower, gl_forecast_ci_upper,
            global_temp, northern_temp,];
var layout = {
    title: 'Monthly deviations from 1951-1980 mean temperatures',
    font: {size: 18},
    showlegend: true,
    legend: {
        "orientation": "h"
    },
    height: 600,
    xaxis: {
        range: ['2015-01-01', '2020-02-01']
    },
    yaxis: {
        range: [-0.25, 2]
    },
};

Plotly.newPlot('graph-div', data, layout, {responsive: true});
