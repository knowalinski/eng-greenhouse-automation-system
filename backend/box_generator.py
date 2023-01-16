input_file = {1:[1,[2,3,4,5],[]], 2:[1,[2,3,4,5]], 3:[1,[2,3,4,5]], 4:[1,[2,3,4,5]], 5:[1,[2,3,4,5]], 6:[1,[2,3,4,5]], 7:[1,[2,3,4,5]]}

class BoxGenerator:
    def __init__(self, input_dict):
        self.input_file = input_dict
        self.state = 0
        self.sensor_data = []
        self.sensor_id = 0
        self.html = ''
    def check_state(self):
        if self.state == 1:
            return "activeSensor"
        else:
            return "inactiveSensor"
    
    def state_class(self):
        return f'<div class = "{self.check_state()}"><br>\n'

    def sensorID_label(self):
        return f'<label>sensor_{self.sensor_id}</label>\n'

    def data_labels(self):
        return '<br><label>Air temperature: {}</label><br>\n' \
            '<label>Air humidity: {}</label><br>\n' \
                '<label>Soil temperature: {}</label><br>\n' \
                    '<label>Soil humidity: {}</label><br>\n</div>\n'.format(*self.sensor_data)

    def merge(self):
        a = self.state_class()
        b = self.sensorID_label()
        c = self.data_labels()
        return a+b+c

    def replicate(self):
        # self.html
        for key in self.input_file:
            self.sensor_id = key
            self.state = self.input_file[key][0]
            self.sensor_data = self.input_file[key][1]
            self.html+=self.merge()
    
    def generate(self):
        opener ='<!DOCTYPE html>\n<head>'\
                '\n<title>DASHBOARD</title>'\
                '\n<link rel="stylesheet" href="{{url_for(\'static\', filename=\'css/style.css\')}}">'\
                '\n</head>'\
                '\n<body>'\
                '\n<h2>DASHBOARD <span id="dash-board"></span></h2>'\
                '\n<button id = goto-plotting>plotting</button>\n'
        self.replicate()
        return opener+self.html+'</body>\n</html>'

    def html_dump(self):
            with open('backend/templates/index.html', 'w') as f:
                f.write(self.generate())
                f.close()



# BoxGenerator(input_file).html_dump()