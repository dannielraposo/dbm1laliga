const express = require('express');
const app = express();
const router = express.Router();
const { Client } = require('pg')

const path = __dirname + '/views/';
const port = 7070;
app.use(express.urlencoded());
app.use(express.json());

router.use(function (req, res, next) { console.log('/' + req.method); next(); });
router.get('/', function (req, res) { res.sendFile(path + 'index.html'); });
router.get('/fixedqueries', function (req, res) { res.sendFile(path + 'fixedqueries.html'); });
router.get('/newquery', function (req, res) { res.sendFile(path + 'newquery.html'); });


const client = new Client({
    user: 'postgres',
    host: 'postgres', //because we are in docker
    database: 'laliga18',
    password: 'postgres',
    port: 5432,
})
client.connect(function (err) {
    if (err) throw err;
    console.log("Connected!");
});

app.post("/sqlquery", (req, res) => {
    client.query(req.body.query, function (err, result) {
        if (err) res.send(500)
        res.send(result)
    })
});

app.use(express.static(path));
app.use('/', router);

app.listen(port, function () {
    console.log("HMI server has started listening on port " + port)
})