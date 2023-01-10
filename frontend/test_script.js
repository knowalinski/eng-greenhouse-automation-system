const data = [2, 5, 6, 1]
var html_block = '<div class = "sensor">'+
'<label for = "sensor_id">box from js</label><br>' +
'<label for = "">Air temperature:</label><br>' +
'<label for = "">Air humidity:</label><br>' +
'<label for = "">Soil temperature:</label><br>' +
'<label for = "">Soil humidity:</label><br>' +
'</div>'
var html = ''
const boxes = document.querySelector('#boxes')
// display_boxes()

// function display_boxes(){
//     html_block.innerHTML = '<div class = "sensor">'

// }
// for (let i = 0; i < data.length; i++) {
//     html += '<div class = "sensor'+i+'">'
    
// }
// boxes.innerHTML = html_block
boxes.innerHTML = html_block
LoopTest()
function LoopTest() {
    var i=0;
    var stop=5;
    for (i=0;i<5;i++) {  
     var v = document.createElement('output');
     v.type="label";
     v.value="Label " +i;
     document.getElementById('boxes').append(html_block);
  
    }
    }

