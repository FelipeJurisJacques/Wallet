//import * as d3 from "./d3.mjs"
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm"

const margin = { top: 20, right: 20, bottom: 30, left: 40 },
    width = 1000 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom

const parseDate = d3.timeParse("%Y-%m-%d")

const x = d3.scaleTime()
    .range([0, width])

const y = d3.scaleLinear()
    .range([height, 0])

const line = d3.line()
    .x(function (d) { return x(d.date); })
    .y(function (d) { return y(d.value); })

function get_prophesied(period) {
    return new Promise(async (resolve, reject) => {
        let response = await fetch(`/api/dashboard/prophesy/?PeriodId=${period}`)
        resolve(await response.json())
    })
}

function get_historical(prophesied) {
    return new Promise(async (resolve, reject) => {
        if (prophesied.length > 1) {
            const end = new Date(prophesied[prophesied.length - 1].date)
            end.setDate(end.getDate() + 15)
            const first = new Date(prophesied[0].date)
            first.setDate(first.getDate() - 15)
            const response = await fetch(`/api/dashboard/historic/?StockId=${stock}&StartDate=${first.toISOString()}&EndDate=${end.toISOString()}`)
            resolve(await response.json())
        } else {
            resolve([])
        }
    })
}

function is_equal_date(date1, date2) {
    const time = date1.getTime()
    const end = time + 43200000
    const start = time - 43200000
    const comparator = date2.getTime()
    return comparator >= start && comparator <= end
}

function get_data(period) {
    return new Promise(async (resolve, reject) => {
        const result = []
        const prophesied = await get_prophesied(period)
        const historical = await get_historical(prophesied)
        for (let historic of historical) {
            let date = new Date(historic.date)
            result[result.length] = {
                date: date,
                historic_close: historic.close,
                prophesy_close: 0.0,
            }
        }
        for (let prophesy of prophesied) {
            let date = new Date(prophesy.date)
            let contains = false
            for (let item of result) {
                if (is_equal_date(item.date, date)) {
                    item.prophesy_close = prophesy.close
                    contains = true
                    break
                }
            }
            if (!contains && date.getTime() > result[result.length - 1].date.getTime()) {
                result[result.length] = {
                    date: date,
                    historic_close: 0.0,
                    prophesy_close: prophesy.close,
                }
            }
        }
        resolve(result)
    })
}

function set_period(period) {
    get_data(period).then(data => {
        const element = document.body.querySelector('svg')
        if (element) {
            element.remove()
        }
        const table = document.body.querySelector('table tbody')
        let html = ''
        const historic_line = []
        const prophesy_line = []
        for (let item of data) {
            html += `<tr><td>${item.date.getDate()}/${item.date.getMonth() + 1}/${item.date.getFullYear()}</td><td>${item.historic_close}</td><td>${item.prophesy_close}</td></tr>`
            historic_line[historic_line.length] = {
                date: parseDate(`${item.date.getFullYear()}-${item.date.getMonth() + 1}-${item.date.getDate()}`),
                value: item.historic_close,
            }
            prophesy_line[prophesy_line.length] = {
                date: parseDate(`${item.date.getFullYear()}-${item.date.getMonth() + 1}-${item.date.getDate()}`),
                value: item.prophesy_close ? item.prophesy_close : 0.0,
            }
        }
        table.innerHTML = html

        const svg = d3.select("body")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

        x.domain(d3.extent(prophesy_line, function (d) { return d.date; }))
        // y.domain([0, d3.max(data, function (d) { return d.value; })])
        y.domain(d3.extent(prophesy_line, function (d) { return d.value; }))
        svg.append("path")
            .datum(prophesy_line)
            .attr("class", "line")
            .attr("d", line)
            .style('stroke', 'yellow')
            .style("stroke-width", "2px")
            .style("fill", "none")

        x.domain(d3.extent(historic_line, function (d) { return d.date; }))
        y.domain(d3.extent(historic_line, function (d) { return d.value; }))
        svg.append("path")
            .datum(historic_line)
            .attr("class", "line")
            .attr("d", line)
            .style('stroke', 'blue')
            .style("stroke-width", "2px")
            .style("fill", "none")

        svg.append("g")
            .attr("class", "axis axis--x")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        svg.append("g")
            .attr("class", "axis axis--y")
            .call(d3.axisLeft(y));
    })
}

const stock = location.search.split('=')[1]
fetch(`/api/dashboard/periods/${stock}/`).then(async response => {
    const json = await response.json()
    const periods = document.body.querySelector('select#periods')
    let id = null
    for (let item of json) {
        if (!id) {
            id = item.id
        }
        let date = new Date(item.max_prophesied_date)
        let element = document.createElement('option')
        element.value = item.id
        element.innerHTML = `${item.period} - ${date.getDay()}/${date.getMonth() + 1}/${date.getFullYear()}`
        periods.append(element)
    }
    if (id) {
        set_period(id)
    }
})

document.body.addEventListener('change', event => {
    if (event.target && event.target.id === 'periods') {
        set_period(event.target.value)
    }
})

// fetch(`/api/prophesy/${location.search.split('=')[1]}/`).then(async response => {
//     const json = await response.json()
//     const table = document.body.querySelector('table tbody')
//     for (let i = 1; i <= json.prophesied.length; i++) {
//         let prophesy = json.prophesied[json.prophesied.length - i]
//         let date = new Date(prophesy.date)
//         let tr = document.createElement('tr')
//         tr.innerHTML = `
//             <td>${json.prophesied.length - i}</td>
//             <td>${date.toLocaleDateString('PT-br', {
//                 weekday: 'long',
//                 year: 'numeric',
//                 month: 'long',
//                 day: 'numeric',
//             })}</td>
//             <td>${prophesy.yhat}</td>
//         `
//         table.append(tr)
//     }
// })