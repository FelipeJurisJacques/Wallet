fetch('/api/stocks').then(async response => {
    let i = 0
    const json = await response.json()
    const table = document.body.querySelector('table tbody')
    for (let stock of json.stocks) {
        let tr = document.createElement('tr')
        tr.innerHTML = `
            <td>${i++}</td>
            <td>${stock.symbol}</td>
            <td>${stock.name}</td>
            <td>${stock.currency}</td>
            <td>
                <a href="historical.html?stock=${stock.id}"><i class="fa-solid fa-table"></i></a>
            </td>
        `
        table.append(tr)
    }
})