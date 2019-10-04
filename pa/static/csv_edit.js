let globalAccountData = {};

Handlebars.registerHelper('if_eq', function (a, b, opts) {
    if (a == b) {
        return opts.fn(this);
    } else {
        return opts.inverse(this);
    }
});

Handlebars.registerHelper('formatDate', function (dateString) {
    return new Handlebars.SafeString(
        dateString.toLocaleDateString()
    );
});

function deleteRow(rowId) {
    "use strict";
    document.getElementById(rowId).remove();
    let toDelete = rowId.split(':');
    globalAccountData[toDelete[0]].splice(toDelete[1], 1);
}

function renderPage() {
    "use strict";
    $('div').remove();
    Object.entries(globalAccountData).forEach(function (element) {
        let key = element[0];

        let source = document.getElementById('df-template').innerHTML;
        let template = Handlebars.compile(source);
        let context = {'df_name': key, 'df_data': globalAccountData[key], 'filesnames': Object.keys(globalAccountData)};
        let html = template(context);

        $('body').append(html);
    });
    $('body').append('<div class="container-fluid">' +
        '<div class="row  text-center" onclick="sendData()">' +
        '<button type="button" class="btn btn-success text-center col-12 p-2 rounded-0">' +
        'Save Data' +
        '</button>' +
        '</div>' +
        '</div>'
    )
    ;
}

function mergeAccounts(fromAccountId, toAccountId) {
    "use strict";

    function swap(items, leftIndex, rightIndex) {
        var temp = items[leftIndex];
        items[leftIndex] = items[rightIndex];
        items[rightIndex] = temp;
    }

    function partition(items, left, right) {
        var pivot = items[Math.floor((right + left) / 2)].date, //middle element
            i = left, //left pointer
            j = right; //right pointer
        while (i <= j) {
            while (items[i].date < pivot) {
                i++;
            }
            while (items[j].date > pivot) {
                j--;
            }
            if (i <= j) {
                swap(items, i, j); //sawpping two elements
                i++;
                j--;
            }
        }
        return i;
    }

    function quickSort(items, left, right) {
        var index;
        if (items.length > 1) {
            index = partition(items, left, right); //index returned from partition
            if (left < index - 1) { //more elements on the left side of the pivot
                quickSort(items, left, index - 1);
            }
            if (index < right) { //more elements on the right side of the pivot
                quickSort(items, index, right);
            }
        }
        return items;
    }

    let toSortItems = [...Object.values(globalAccountData[fromAccountId]),
        ...Object.values(globalAccountData[toAccountId])];
    delete globalAccountData[fromAccountId];
    globalAccountData[toAccountId] = quickSort(toSortItems, 0, toSortItems.length - 1);
    renderPage();
}

function saveData(data, sendDataUrl, redirectUrl) {
    "use strict";
    sessionStorage.setItem('saveDataUrl', sendDataUrl);
    sessionStorage.setItem('redirectUrl', redirectUrl);
    data.forEach(function (element) {
            let df = JSON.parse(element);
            let id = Object.keys(df)[0];
            globalAccountData[id] = [];

            let rawData = JSON.parse(df[id]);
            Object.keys(rawData.amount).forEach(function (key) {
                globalAccountData[id].push({
                    date: new Date(rawData.date[key]),
                    amount: rawData.amount[key],
                    category: rawData.category[key]
                });
            });
        }
    );
    renderPage();
}

function sendData() {
    $.ajax({
        type: "POST",
        url: sessionStorage.getItem('saveDataUrl'),
        data: {'data': JSON.stringify(globalAccountData)}
    }).always(function (data, status, error) {
        $().alert();
        // window.location.replace(sessionStorage.getItem('redirectUrl'));
    });
}
