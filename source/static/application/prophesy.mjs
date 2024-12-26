//import * as d3 from "./d3.mjs"
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm"

const margin = { top: 20, right: 20, bottom: 30, left: 40 },
    width = 500 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom

const parseDate = d3.timeParse("%Y-%m-%d")

const x = d3.scaleTime()
    .range([0, width])

const y = d3.scaleLinear()
    .range([height, 0])

const line = d3.line()
    .x(function (d) { return x(d.date); })
    .y(function (d) { return y(d.value); })


function set_period(period) {
    fetch(`/api/dashboard/prophesy/?PeriodId=${period}`).then(async response => {
        const prophesied = await response.json()
        if (prophesied.length > 1) {
            const end = new Date(prophesied[prophesied.length - 1].date)
            end.setDate(end.getDate() + 15)
            const first = new Date(prophesied[0].date)
            first.setDate(first.getDate() - 15)
            fetch(`/api/dashboard/historic/?StockId=${stock}&StartDate=${first.toISOString()}&EndDate=${end.toISOString()}`).then(async response => {
                const historical = await response.json()

                const element = document.body.querySelector('svg')
                if (element) {
                    element.remove()
                }

                const svg = d3.select("body")
                    .append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

                let data = []
                for (let prophesy of prophesied) {
                    let date = new Date(prophesy.date)
                    data[data.length] = {
                        date: parseDate(`${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`),
                        value: prophesy.close,
                    }
                }
                x.domain(d3.extent(data, function (d) { return d.date; }));
                y.domain([0, d3.max(data, function (d) { return d.value; })]);
                svg.append("path")
                    .datum(data)
                    .attr("class", "line")
                    .attr("d", line)
                    .style('stroke', 'yellow')
                    .style("stroke-width", "2px")
                    .style("fill", "none")

                data = []
                for (let historic of historical) {
                    let date = new Date(historic.date)
                    data[data.length] = {
                        date: parseDate(`${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`),
                        value: historic.close,
                    }
                }
                x.domain(d3.extent(data, function (d) { return d.date; }));
                y.domain([0, d3.max(data, function (d) { return d.value; })]);
                svg.append("path")
                    .datum(data)
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
        element.innerHTML = `${item.period} - ${date.getDay()}/${date.getMonth()}/${date.getFullYear()}`
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