var result =[["2020-03-02", 21], ["2020-03-03", 124], ["2020-03-04", 0], ["2020-03-05", 436], ["2020-03-06", 632], ["2020-03-10", 613], ["2020-03-11", 580], ["2020-03-12", 599], ["2020-03-13", 640], ["2020-03-16", 1386]];
var rod = [["2020-03-01", 1], ["2020-03-02", 1], ["2020-03-03", 90], ["2020-03-04", 0], ["2020-03-05", 175], ["2020-03-06", 234], ["2020-03-07", 0], ["2020-03-08", 0], ["2020-03-09", 0], ["2020-03-10", 212], ["2020-03-11", 209], ["2020-03-12", 214], ["2020-03-13", 233], ["2020-03-14", 0], ["2020-03-15", 1], ["2020-03-16", 412]];
var ORV = [["2020-03-01", 2], ["2020-03-02", 2], ["2020-03-03", 26], ["2020-03-04", 0], ["2020-03-05", 204], ["2020-03-06", 297], ["2020-03-07", 0], ["2020-03-08", 0], ["2020-03-09", 0], ["2020-03-10", 302], ["2020-03-11", 261], ["2020-03-12", 261], ["2020-03-13", 276], ["2020-03-14", 0], ["2020-03-15", 2], ["2020-03-16", 292]];
var grip = [["2020-03-01", 3], ["2020-03-02", 3], ["2020-03-03", 0], ["2020-03-04", 0], ["2020-03-05", 2], ["2020-03-06", 0], ["2020-03-07", 0], ["2020-03-08", 0], ["2020-03-09", 0], ["2020-03-10", 5], ["2020-03-11", 0], ["2020-03-12", 0], ["2020-03-13", 0], ["2020-03-14", 0], ["2020-03-15", 4], ["2020-03-16", 10]];
var other = [["2020-03-01", 0], ["2020-03-02", 4], ["2020-03-03", 8], ["2020-03-04", 0], ["2020-03-05", 51], ["2020-03-06", 96], ["2020-03-07", 0], ["2020-03-08", 0], ["2020-03-09", 0], ["2020-03-10", 85], ["2020-03-11", 103], ["2020-03-12", 116], ["2020-03-13", 124], ["2020-03-14", 0], ["2020-03-15", 2], ["2020-03-16", 108]];
var school = [["2020-03-01", 0], ["2020-03-02", 5], ["2020-03-03", 0], ["2020-03-04", 0], ["2020-03-05", 0], ["2020-03-06", 0], ["2020-03-07", 0], ["2020-03-08", 0], ["2020-03-09", 0], ["2020-03-10", 1], ["2020-03-11", 1], ["2020-03-12", 1], ["2020-03-13", 1], ["2020-03-14", 0], ["2020-03-15", 4], ["2020-03-16", 1]];
var notsch = [["2020-03-01", 0], ["2020-03-02", 6], ["2020-03-03", 0], ["2020-03-04", 0], ["2020-03-05", 2], ["2020-03-06", 3], ["2020-03-07", 0], ["2020-03-08", 0], ["2020-03-09", 0], ["2020-03-10", 5], ["2020-03-11", 5], ["2020-03-12", 5], ["2020-03-13", 5], ["2020-03-14", 0], ["2020-03-15", 2], ["2020-03-16", 8]];
var und = [["2020-03-01", 0], ["2020-03-02", 0], ["2020-03-03", 0], ["2020-03-04", 0], ["2020-03-05", 2], ["2020-03-06", 2], ["2020-03-07", 0], ["2020-03-08", 0], ["2020-03-09", 0], ["2020-03-10", 3], ["2020-03-11", 1], ["2020-03-12", 2], ["2020-03-13", 1], ["2020-03-14", 0], ["2020-03-15", 3], ["2020-03-16", 6]];
var dist = [["2020-03-01", 0], ["2020-03-02", 0], ["2020-03-03", 0], ["2020-03-04", 0], ["2020-03-05", 0], ["2020-03-06", 0], ["2020-03-07", 0], ["2020-03-08", 0], ["2020-03-09", 0], ["2020-03-10", 0], ["2020-03-11", 0], ["2020-03-12", 0], ["2020-03-13", 0], ["2020-03-14", 0], ["2020-03-15", 3], ["2020-03-16", 549]];

var lab = []; var lab1 = []; var lab2 = []; var lab3 = []; var lab4 = []; var lab5 = []; var lab6 = []; var lab7 = []; var lab8 = [];
var dat=[]; var dat1=[]; var dat2=[]; var dat3=[]; var dat4=[]; var dat5=[]; var dat6=[]; var dat7=[]; var dat8=[];

function getarray(per1, per2, name){
	for (let i = 0; i < eval(name).length; i++) {
		let a = eval(name)[i][0];
		let b = eval(name)[i][1];
		eval(per1).push(a);
		eval(per2).push(b);
	}
}
getarray("lab", "dat", "rod");
getarray("lab1", "dat1", "ORV");
getarray("lab2", "dat2", "grip");
getarray("lab3", "dat3", "other");
getarray("lab4", "dat4", "school");
getarray("lab5", "dat5", "notsch");
getarray("lab6", "dat6", "und");
getarray("lab7", "dat7", "dist");
getarray("lab8", "dat8", "result");
/*instead of function
for(let i =0; i<rod.length; i++){
	lab.push(rod[i][0]);
	dat.push(rod[i][1]);
}
*/
var ctx = document.getElementById('rod').getContext('2d');
var chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: lab,
        datasets: [{
            label: "решение родителей",
            backgroundColor: 'green',
            data: dat
        }]
    },
    options: {}
});

var ctx1 = document.getElementById('ORV').getContext('2d');
var chart1 = new Chart(ctx1, {
    type: 'line',
    data: {
        labels: lab1,
        datasets: [{
            label: "ОРВИ",
            backgroundColor: 'red',
            data: dat1
        }]
    },
    options: {}
});

var ctx2 = document.getElementById('grip').getContext('2d');
var chart = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: lab2,
        datasets: [{
            label: "Грипп",
            backgroundColor: 'blue',
            data: dat2
        }]
    },
    options: {}
});

var ctx3 = document.getElementById('other').getContext('2d');
var chart3 = new Chart(ctx3, {
    type: 'line',
    data: {
        labels: lab3,
        datasets: [{
            label: "Другое заболевание",
            backgroundColor: 'blue',
            data: dat3
        }]
    },
    options: {}
});

var ctx4 = document.getElementById('sch').getContext('2d');
var chart4 = new Chart(ctx4, {
    type: 'line',
    data: {
        labels: lab4,
        datasets: [{
            label: "травма в школе",
            backgroundColor: 'blue',
            data: dat4
        }]
    },
    options: {}
});

var ctx5 = document.getElementById('nsch').getContext('2d');
var chart5 = new Chart(ctx5, {
    type: 'line',
    data: {
        labels: lab5,
        datasets: [{
            label: "травма не в школе",
            backgroundColor: 'blue',
            data: dat5
        }]
    },
    options: {}
});

var ctx6 = document.getElementById('und').getContext('2d');
var chart6 = new Chart(ctx6, {
    type: 'line',
    data: {
        labels: lab6,
        datasets: [{
            label: "Неизвестно",
            backgroundColor: 'blue',
            data: dat6
        }]
    },
    options: {}
});
var ctx7 = document.getElementById('dist').getContext('2d');
var chart7 = new Chart(ctx7, {
    type: 'line',
    data: {
        labels: lab7,
        datasets: [{
            label: "Дистанционное обучение",
            backgroundColor: 'blue',
            data: dat7
        }]
    },
    options: {}
});

var ctx8 = document.getElementById('res').getContext('2d');
var chart8 = new Chart(ctx8, {
    type: 'line',
    data: {
        labels: lab8,
        datasets: [{
            label: "результат",
            backgroundColor: 'red',
            data: dat8
        }]
    },
    options: {}
});
//очистка кэша
