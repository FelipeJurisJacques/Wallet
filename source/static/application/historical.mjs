fetch(`/api/historical/${location.search.split('=')[1]}/`).then(async response => {
    let i = 0
    const json = await response.json()
    const table = document.body.querySelector('table tbody')
    for (let i = 1; i <= json.historical.length; i++) {
        let historic = json.historical[json.historical.length - i]
        let tr = document.createElement('tr')
        tr.innerHTML = `
            <td>${i++}</td>
            <td>${historic.date}</td>
            <td>${historic.open}</td>
            <td>${historic.low}</td>
            <td>${historic.high}</td>
            <td>${historic.close}</td>
            <td>${historic.volume}</td>
        `
        table.append(tr)
    }
})