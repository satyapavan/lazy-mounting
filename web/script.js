function createTable (tableData) {
  var table = document.createElement('table')
  table.classList.add('table')
  table.classList.add('table-striped')
  table.classList.add('table-bordered')
  table.classList.add('table-hover')

  var tableBody = document.createElement('tbody')
  var tableHead = document.createElement('thead')

  var headRow = true
  tableData.forEach(function (rowData) {
    var row = document.createElement('tr')
    if (headRow) {
      row.classList.add('table-primary')

      rowData.forEach(function (cellData) {
        var cell = document.createElement('th')
        cell.appendChild(document.createTextNode(cellData))
        row.appendChild(cell)
      })

      tableHead.appendChild(row)

      headRow = false
    } else {
      rowData.forEach(function (cellData) {
        var cell = document.createElement('td')
        cell.appendChild(document.createTextNode(cellData))
        row.appendChild(cell)
      })

      tableBody.appendChild(row)
    }
  })

  table.appendChild(tableHead)
  table.appendChild(tableBody)

  document.getElementById('data-container').appendChild(table)
  document.getElementById('data-container').appendChild(document.createElement('hr'))
}

function processFetchResponse (data) {
  console.log('Inside processResponse()', data)
  createTable(data);
}

function processLogsResponse (data) {
  console.log('Inside processResponse()', data)

  var boolNoRecordFound = true
    var pre = document.createElement("pre");

	var temp = '';
	for(itr in data) {
		temp = temp + data[itr];
	}
    pre.textContent = temp;

  document.getElementById('data-container').appendChild(pre);
  //document.getElementById('data-container').appendChild(document.createTextNode(data))

    document.getElementById('data-container').classList.add('mx-0')
}

function fetchApi () {
  console.log('Entering into fetchApi')

  async function getData () {
    const response = await fetch('/fetch')
    const data = await response.json()
    return data
  }

  getData().then(data => processFetchResponse(data))
}

document.getElementById('btn-home').addEventListener('click', function () {
  console.log('Entered into btn-home')
  fetchApi();
})

document.getElementById('btn-logs').addEventListener('click', function () {
  console.log('Entered into btn-logs')

  async function getData () {
    const response = await fetch('/logs')
    const data = await response.json()
    return data
  }

  getData().then(data => processLogsResponse(data))
})

