fetch(`/api/prophesy/${location.search.split('=')[1]}/`).then(async response => {
    const json = await response.json()
    const table = document.body.querySelector('table tbody')
    for (let i = 1; i <= json.prophesied.length; i++) {
        let prophesy = json.prophesied[json.prophesied.length - i]
        let date = new Date(prophesy.date)
        let tr = document.createElement('tr')
        tr.innerHTML = `
            <td>${json.prophesied.length - i}</td>
            <td>${date.toLocaleDateString('PT-br', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
            })}</td>
            <td>${prophesy.yhat}</td>
        `
        table.append(tr)
    }
})