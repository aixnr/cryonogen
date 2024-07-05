import Fuse from './mod/fuse.esm.js'

const fetchVialData = async () => {
  try {
    const response = await fetch(`${ ApiUrl }/vials`)
    const data = await response.json()
    return data.data
  } catch (error) {
    console.error(error)
  }
}


const searchVial = async() => {
  // Search result element
  let vialList = document.getElementById('vial_list')

  // Read all vialData
  const vialData = await fetchVialData()

  // Instantiate a Fuse instance
  const fuse = new Fuse(vialData, {
    keys: ['shortName', 'longName', 'vialOrigin']
  })

  // Listen to catch-result event
  document.addEventListener("catch-search", (event) => {
    const fuseResult = fuse.search(event.detail)
    // console.log(fuseResult)

    // Update vial list with the output
    if (fuseResult.length > 0) {
      // Placeholder for the result div

      // Loop and add results to the searchListHTML
      let searchListHTML = ''
      for (const result of fuseResult) {
        searchListHTML += `
          <div class="searchListIndividual">
            <div class="result_vial_name">${ result.item.longName }</div>
            <div>
              <span class="result_field_title">Location</span>
              ${ result.item.BoxID }, ${ result.item.Position }
            </div>
            <div class="result_meta_extra">
              <span class="result_field_title">Depositor</span>
              ${result.item.vialDepositor } on ${ result.item.dateDeposited }
              <span class="result_field_title">Origin</span>
              ${ result.item.vialOrigin }
            </div>
          </div>
        `
      }

      // Now, put that searchListHTML here
      vialList.innerHTML = searchListHTML

    } else {
      // Maybe come up with something fun here later
      vialList.innerHTML = 'No vials :('
    }
  })
}


const emptySearch = () => {
  // Clear search result if search box is empty
  document.addEventListener("empty-search", () => {
    document.getElementById('vial_list').innerHTML = ''
  })
}


// Execution layer!
// -----------------------------------------------------------------------------
searchVial()
emptySearch()
