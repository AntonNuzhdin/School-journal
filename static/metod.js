/*
*/

var data = new Array();
function postrgrid(obje) {
    data=[];
    let k=[4,5,6,7,8,9,10];
    var row={};
    for (var i = 0; i < obje.length; i++) {
        //let {...row} = obj[i];
        //console.log(row);
        row = {
            id: i,
            lesson: obje[i].lesson,
            fio: obje[i].fio,
            klass: obje[i].klass,
            mark: obje[i].mark
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
    $("#jqxgrid").jqxGrid(
        {
            filterable: true,
            sortable: true,
            source: dataAdapter,
            editable: true,
            //enabletooltips: true,
            selectionmode: 'multiplecellsadvanced',
            width: '95%',
            columns: [
                {text: 'id', datafield: 'id', width: '15%'},
                {text: 'Урок', datafield: 'lesson', width: '20%'},
                {text: 'ФИО', datafield: 'fio', width: '25%', cellsalign: 'left'},
                {text: 'Буква класса', datafield: 'klass', width: '20%'},
                {text:'Итог', datafield:'mark', width:'20%',columntype: 'dropdownlist', createeditor: function (row, column, editor) {
                        // assign a new data source to the dropdownlist.
                        var list = ['0', '1', '2', '3', '4','5','6','7','8','9','10'];
                        editor.jqxDropDownList({ autoDropDownHeight: true, source: list });
                    }}
            ], height:'430%'
        });
}
function ready(){
    if (this.status == 200) {
        var obj = JSON.parse(this.responseText);
        console.log(obj);
        him.onclick = function() {
            predm.textContent="ХИМИЯ";
            postrgrid(obj.химия);
        };
        inf.onclick = function() {
            predm.textContent="ИНФОРМАТИКА";
            postrgrid(obj.информатика);
        };
        bio.onclick = function() {
            predm.textContent="БИОЛОГИЯ";
            postrgrid(obj.биология);
        };

        $("#jqxgrid").on('cellendedit', function (event) {
            var args = event.args;
            var columnDataField = args.datafield;
            var rowIndex = args.rowindex;
            var cellValue = args.value;//выбранное значение
            var oldValue = args.oldvalue;//старое значение
            //alert(cellValue+'     '+rowIndex+'      '+columnDataField);
            if(columnDataField=='mark') {
                if(predm.textContent=='ХИМИЯ') {lesson='ch';les='химия'}
                if(predm.textContent=='ИНФОРМАТИКА') {lesson='inf';les='информатика';}
                if(predm.textContent=='БИОЛОГИЯ') {lesson='bio';les='биология';}
                id_stud=obj[les][rowIndex].id;
                let req = new XMLHttpRequest();
                req.addEventListener("load", () => {
                    console.log('finished')
                });
                let url = 'https://1502энергия.рф/dotnet?' + cellValue + '&id=' + id_stud+'&lesson='+lesson;
                console.log(url);
                req.open('GET', url, true);
                req.send();
            }
        });

    }
}
var req = new XMLHttpRequest();
req.addEventListener("load", ready);

req.open('GET', '/static/metodist.json ', true);
//req.open('GET', 'http://127.0.0.1:8887/test.json', false);
req.send(null);