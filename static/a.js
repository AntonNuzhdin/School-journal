var data = new Array();
var zdanie;
var obje;
var us_id;
//          0                               1                   2                               3                                         4                                         5           6                   7
//  физико-математическое   информационно-технологическое   инженерное      естественнонаучное: физико-химическое     естественнонаучное: химико-биологическое    экономико-математическое  универсальное       не выбран
function input(event){
    //alert('Проверка');
    //console.log(event);
    //console.log(event.target.value);
    zdanie=event.target.value;
    console.log(event.target);
    postrgrid();
    var filtergroup = new $ .jqx.filter ();
    var filtervalue = zdanie;
    var filtercondition = 'equal';
    var filter1 = filtergroup.createfilter('stringfilter', filtervalue, filtercondition);
    filtergroup.addfilter (1, filter1);
    $("#jqxgrid").jqxGrid('addfilter', event.target.id, filtergroup);
// apply the filters.
    $("#jqxgrid").jqxGrid('applyfilters');
    if(filtervalue=='all'){
        $ ( "#jqxgrid" ). jqxGrid ( 'clearfilters' );
    }

}
function postrgrid(ob) {
    for (var i = 0; i < ob; i++) {
        //let {...row} = obj[i];
        //console.log(row);
        var row = {
            num: i,
            fio: obje[i].ФИО,
            buk: obje[i].класс,
            pr1: obje[i].приоритет1,
            pr2: obje[i].приоритет2/*.направление*/,
            pr3: obje[i].приоритет3/*.направление*/,
            zd:obje[i].территория,
            itog:bud_klass[i]
        };
        /* row["num"] = i;
         row["fio"] = FIO[i];
         row["buk"]=;*/
        data[i] = row;

    }
    var source =
        {
            localdata: data,
            datatype: "array"
        };
    var dataAdapter = new $.jqx.dataAdapter(source,
        /* {
             loadComplete: function (data) { },
             loadError: function (xhr, status, error) { }
         }*/);
    var cellsrenderer = function (row, columnfield, value, defaulthtml, columnproperties) {
        if (value=='не выбран' || obje[row].приоритет1=='не выбран') {
            return '<span style="margin: 4px; float: ' + columnproperties.cellsalign + '; color: rgb(1000,0,0);">' + value + '</span>';
        }
        else {
            return '<span title="Достаточный потенциал для обучения в физмате" style="margin: 4px; float: ' + columnproperties.cellsalign + '; color: rgb(0,0,0);">' + value + '</span>'
            //return '<span style="margin: 4px; float: ' + columnproperties.cellsalign + '; color: #008000;">' + value + '</span>';
        }

    };
    $("#jqxgrid").jqxGrid(
        {
            filterable:true,
            sortable: true,
            source: dataAdapter,
            //editable: true,
            //enabletooltips: true,
            selectionmode: 'multiplecellsadvanced',
            width: '95%',
            columns: [
                {text: '№', datafield: 'num', width: '5%', cellsrenderer: cellsrenderer}, //ширина колонок
                {text: 'ФИО', datafield: 'fio', width: '22%', cellsalign: 'right', cellsrenderer: cellsrenderer},
                {text: 'Буква класса', datafield: 'buk', width: '10%'},
                {text: 'Приоритет 1', datafield: 'pr1', width: '19%', cellsalign: 'right', cellsformat: 'c2'},
                {text: 'Приоритет 2', datafield: 'pr2', width: '19%', cellsalign: 'right', cellsformat: 'c2'},
                {text: 'Приоритет 3', datafield: 'pr3', width: '19%', cellsalign: 'right', cellsformat: 'c2'},
                {text: 'Здание', datafield: 'zd', width: '6%', cellsalign: 'right', columntype: 'textbox'}
                //{text:'Итог', datafield:'itog', width:'5%',columntype: 'dropdownlist'}
            ], height:'95%'
        });
}
//          0                    1                               2                   3                              4                                         5                                     6               7               8
//        заполнено  физико-математическое   информационно-технологическое   инженерное      естественнонаучное: физико-химическое     естественнонаучное: химико-биологическое    экономико-математическое  универсальное       не выбран

function getarray(obj, pr) {
    let arr=[];
    let a={};
    let col=[0,0,0,0,0,0,0,0,0];
    for(let i=0; i<obj.length; i++){

        if(obj[i][pr]=='физико-математическое'){
            //alert('te');
            col[1]=col[1]+1;
        }
        if(obj[i][pr]=='информационно-технологическое'){
            col[2]++;
        }
        if(obj[i][pr]=='инженерное'){
            col[3]++;
        }
        if(obj[i][pr]=='естественнонаучное: физико-химическое'){
            col[4]++;
        }
        if(obj[i][pr]=='естественнонаучное: химико-биологическое'){
            col[5]++;
        }
        if(obj[i][pr]=='экономико-математическое'){
            col[6]++;
        }
        if(obj[i][pr]=='универсальное'){
            col[7]++;
        }
        if(obj[i][pr]!='не выбран'){
            col[0]++;
        }else {col[8]++;}
    }
    arr.push({
        col1:col[0],
        name1:'заполнено'});
    arr.push({
        col:col[1],
        name:'физико-математическое'});
    arr.push({
        col:col[2],
        name:'информационно-технологическое'});
    arr.push({
        col:col[3],
        name:'инженерное'});
    arr.push({
        col:col[4],
        name:'естественнонаучное: физико-химическое'});
    arr.push({
        col:col[5],
        name:'естественнонаучное: химико-биологическое'});
    arr.push({
        col:col[6],
        name:'экономико-математическое'});
    arr.push({
        col:col[7],
        name:'универсальное'});
    arr.push({
        col:col[8],
        name:'не выбран'});
    arr.push({
        col1:col[8],
        name1:'не выбран'});
    return(arr);
}
function ready(){
    if (this.status == 200) {
        var obj = JSON.parse(this.responseText);
        // console.log(obje);
        //var obj=stud;//НА КРАЙНИЙ СЛУЧАЙ
        obje=obj;
        //zd.addEventListener('change',input);
        //buk.addEventListener('change',input);
        //pr1.addEventListener('change',input);
        //pr2.addEventListener('change',input);
        //pr3.addEventListener('change',input);
        // document.querySelector('.zdanie')
        // ...........///////////////////////////////////////////////
        $(document).ready(function () {
            var sampleData=getarray(obje, "приоритет1");
            var settings = {
                title: "Диаграма первого приоритета",
                description: " ",
                showLegend: true,
                //padding: { left: 5, top: 5, right: 5, bottom: 5 },
                titlePadding: { left: 90, top: 0, right: 0, bottom: 10 },
                source: sampleData,
                categoryAxis:
                    {
                        dataField: 'Day',
                        showGridLines: true
                    },
                //colorScheme: 'scheme01',
                seriesGroups:
                    [
                        {
                            type: 'pie',
                            //columnsGapPercent: 50,
                            showLabels: true,
                            series:
                                [
                                    {
                                        dataField: 'col',
                                        displayText: 'name',
                                        //color:'color',
                                        labelRadius: 100,
                                        initialAngle: 15,
                                        radius: 80,
                                        centerOffset: 0
                                        //formatSettings: { sufix: '%', decimalPlaces: 1 }
                                    }
                                ]
                        }
                    ]
            };
            $('#chartContainer').jqxChart(settings);
            //alert('новый график');
            sampleData=getarray(obje, "приоритет2");
            settings = {
                title: "Диарграма второго приоритета",
                description: " ",
                showLegend: true,
                padding: { left: 5, top: 5, right: 5, bottom: 5 },
                titlePadding: { left: 90, top: 0, right: 0, bottom: 10 },
                source: sampleData,
                categoryAxis:
                    {
                        dataField: 'Day',
                        showGridLines: true
                    },
                //colorScheme: 'scheme01',
                seriesGroups:
                    [
                        {
                            type: 'pie',
                            //columnsGapPercent: 50,
                            showLabels: true,
                            series:
                                [
                                    {
                                        dataField: 'col',
                                        displayText: 'name',
                                        //color:'color',
                                        labelRadius: 100,
                                        initialAngle: 15,
                                        radius: 80,
                                        centerOffset: 0,
                                        //formatSettings: { sufix: '%', decimalPlaces: 1 }
                                    }
                                ]
                        }
                    ]
            };
            $('#chartContainer2').jqxChart(settings);
            sampleData=getarray(obje, "приоритет3");
            //console.log(sampleData);
            settings = {
                title: "Диаграма третьего приоритета",
                description: " ",
                showLegend: true,
                padding: { left: 5, top: 5, right: 5, bottom: 5 },
                titlePadding: { left: 90, top: 0, right: 0, bottom: 10 },
                source: sampleData,
                categoryAxis:
                    {
                        dataField: 'Day',
                        showGridLines: true
                    },
                //colorScheme: 'scheme01',
                seriesGroups:
                    [
                        {
                            type: 'pie',
                            //columnsGapPercent: 50,
                            showLabels: true,
                            series:
                                [
                                    {
                                        dataField: 'col',
                                        displayText: 'name',
                                        //color:'color',
                                        labelRadius: 100,
                                        initialAngle: 15,
                                        radius: 80,
                                        centerOffset: 0,
                                        //formatSettings: { sufix: '%', decimalPlaces: 1 }
                                    }
                                ]
                        }
                    ]
            };
            $('#chartContainer3').jqxChart(settings);
            //$('#chartContainer').jqxChart({backgroundColor:'Gray'});
        });
//============================================================
        $( ".zdanie" ).change(function() {
            //alert( "Handler for .change() called." );
            zdanie = $(this).val();
            //console.log(zdanie);
        });
        //zdanie=$(this).val();
        ob=obj.length;
        //alert('hello');
        postrgrid(ob);
        /*  $("#jqxgrid").bind('bindingcomplete', function () {
              var localizationobj = {};
              filterstringcomparisonoperators = ['empty', 'not empty', 'contains', 'contains(match case)',
                  'does not contain', 'does not contain(match case)', 'starts with', 'starts with(match case)',
                  'ends with', 'ends with(match case)', 'equal', 'equal(match case)', 'null', 'not null'];
              filternumericcomparisonoperators = ['equal', 'not equal', 'less than', 'less than or equal', 'greater than', 'greater than or equal', 'null', 'not null'];
              filterdatecomparisonoperators = ['equal', 'not equal', 'less than', 'less than or equal', 'greater than', 'greater than or equal', 'null', 'not null'];
              filterbooleancomparisonoperators = ['equal', 'not equal'];
              localizationobj.filterstringcomparisonoperators = filterstringcomparisonoperators;
              localizationobj.filternumericcomparisonoperators = filternumericcomparisonoperators;
              localizationobj.filterdatecomparisonoperators = filterdatecomparisonoperators;
              localizationobj.filterbooleancomparisonoperators = filterbooleancomparisonoperators;
              // apply localization.
              $("#jqxgrid").jqxGrid('localizestrings', localizationobj);
          });*/
    }
    else{
        console.log('Неудалось получить json2');
    }
}
/*function getar(obj){
    //console.log(obj);
    //console.log([...obj]);
    for(let i=0; i<obj.length;i++){
        FIO.push(obj[i].ФИО);
        BUKVA.push();
        console.log(obj[i].klass);
        pr1.push();
        pr2.push();
        pr3.push();
    }
}*/

var req = new XMLHttpRequest();
req.addEventListener("load", ready);
req.open('GET', '../static/otchet_students.json', true);
//req.open('GET', 'http://127.0.0.1:8887/test.json', false);
req.send(null);
