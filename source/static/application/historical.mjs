fetch(`/api/historical/${location.search.split('=')[1]}/`).then(async response => {
    let i = 0
    const json = await response.json()
    const table = document.body.querySelector('table tbody')
    for (let i = 1; i <= json.historical.length; i++) {
        let historic = json.historical[json.historical.length - i]
        let date = new Date(historic.date)
        let tr = document.createElement('tr')
        tr.innerHTML = `
            <td>${json.historical.length - i}</td>
            <td>${date.toLocaleDateString('PT-br', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                // hour: '2-digit',
                // minute: '2-digit',
            })}</td>
            <td>${historic.open}</td>
            <td>${historic.low}</td>
            <td>${historic.high}</td>
            <td>${historic.close}</td>
            <td>${historic.volume}</td>
        `
        table.append(tr)
    }
})