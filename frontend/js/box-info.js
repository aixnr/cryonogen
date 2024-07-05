// Fetch box information
const fetchBoxInfo = async () => {
  // get url parameters
  const params = new URLSearchParams(window.location.search)
  const box_id = params.get('box_id')

  // Resolve the request and return data
  try {
    const response = await fetch(`${ ApiUrl }/box/${ box_id }`)
    const payload = await response.json()
    return payload
  } catch (error) {
    console.error(error)
  }
}


// 
const updateBoxInfo = async() => {
  boxInfoParagraph = document.getElementById('box_info')

  fetchBoxInfo().then(payload => {
    data = payload['data'][0]
    boxInfoParagraph.innerHTML = `
      <h2>${ data['BoxID'] }</h2>
      <p>${ data['boxDescription'] }</p>
    `

    document.title = `Cryonogen ${ data['BoxID'] }: ${ data['boxDescription'] }`
  })

}


// -----------------------------------------------------------------------------
// Execution layer!
updateBoxInfo()
