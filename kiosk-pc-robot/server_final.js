

var express = require('express'),
app = express(),
port = 3000,
bodyParser = require('body-parser');
const fs = require('fs');


//var path = __dirname + '/views/';
var path = __dirname + "/";

app.use(bodyParser.json({limit: '50mb'})); //Set the limited maximum data amount included in a request. The default is '100kb'
app.use(bodyParser.urlencoded({limit: '50mb', extended: true})); //extended - True: use querystring module to decode the url string; False： use qs module instead

// middleware to use for all requests
app.use(function(req, res, next) {
	res.header("Access-Control-Allow-Origin", "*");
	res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");

    next(); // make sure we go to the next routes and don't stop here
});


// API ROUTES -------------------
// we'll get to these in a second
// get an instance of the router for api routes
var apiRoutes = express.Router(); 

// route to show a random message (GET http://localhost:8080/api/)
apiRoutes.get('/', function(req, res) {
  res.json({ message: 'Welcome to API server!' });
});

apiRoutes.get('/data', async function(req, res) {

	res.json({"host_name": "host_name",
	"host_email": "host_email",
	"meeting_venue": "meeting_venue",
	"visitor_name": "visitor_name",
	"visitor_picture":"visitor_picture"
	});
});



apiRoutes.post('/save', async function(req, res) {

	var host_name = req.body.host_name;
	var host_email = req.body.host_email;
	var meeting_venue = req.body.meeting_venue;
	var visitor_name = req.body.visitor_name;
    var visitor_picture = req.body.visitor_picture;

	var object =
	{
		host_name: host_name ,
		host_email: host_email ,
		meeting_venue: meeting_venue ,
		visitor_name: visitor_name,
		visitor_picture : visitor_picture
	};

	//create new file based on the timeline
	
	const fs = require('fs');

	var t1 = Date.now();
    var t2 = new Date().getTime();

    //console.log(t1);
    //console.log(t2);
    var path = __dirname + "/files/";

    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth()+1;
    var day = date.getDate();
    var hour = date.getHours();
    var minute = date.getMinutes();
    var second = date.getSeconds();
    date_info = year+'-'+month+'-'+day+'-'+hour+'-'+minute;
    //console.log(date_info);

	/*fs.rename(path+'/test.txt',date_info+'.txt', function(err){
		if(err){
		 throw err;
		}
		console.log('done!');
	   })
	*/
	
    
	//console.log(object);
	filename = object["visitor_name"];
	
	fs.writeFile(path +date_info + '_' + filename+'.json', JSON.stringify(object), function(err) { 

		if(err) {
			return console.log(err);
		}

		console.log("The time now is " + date_info + ".\nThe information of " + filename + " was saved.");
	});
	

	//console.log("id:" + id);
	//console.log("name:" + name);
	//console.log("email:" + email);
    var data = visitor_picture.replace(/^data:image\/\w+;base64,/, "");
    var buf = new Buffer(data, 'base64');
    fs.writeFile(path + filename+'.png', buf,(error) => { /* handle error */ });



	
	res.json({host_name ,host_email ,meeting_venue ,visitor_name,visitor_picture});
});

// apply the routes to our application with the prefix /api
app.use('/api', apiRoutes);

// =======================
// start the server ======
// =======================
app.listen(port);


console.log('Server http://localhost:'+ port);