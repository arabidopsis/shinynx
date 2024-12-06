const count_el = document.getElementById("count")
const status_el = document.getElementById("status")
const source_el = document.getElementById("source")
source_el.textContent = document.cookie
let count = 0
async function check_url() {
    count_el.textContent = `${++count}`
    try {
        const resp = await fetch(URL)
        if (!resp.ok) {
            status_el.textContent = "Failure!"
            status_el.style.color = "red"
            return
        } else {
            status_el.textContent = "In progress"
        }
    } catch (e) {
        status_el.textContent = "Failure!"
        status_el.style.color = "red"
        return
    }

    if (count === 100) {
        status_el.textContent = "Test complete"
        status_el.style.color = "green"
        return
    }

    setTimeout(check_url, 10)
}
check_url()
