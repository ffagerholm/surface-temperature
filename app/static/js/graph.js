
window.mobilecheck = function() {
    var check = false;
    (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
    return check;
};

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
        color: 'rgb(255, 254, 64)',
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

if (window.mobilecheck()) {
    fontsize = 22;
    height = 700;
} else {
    fontsize = 18;
    height = 600;
}

var layout = {
    title: 'Monthly deviations from mean temperatures',
    font: {size: fontsize},
    showlegend: true,
    legend: {
        "orientation": "h"
    },
    height: height,
    xaxis: {
        range: ['2015-01-01', '2020-02-01']
    },
    yaxis: {
        range: [-0.25, 2]
    },
};

Plotly.newPlot('graph-div', data, layout, {responsive: true});
